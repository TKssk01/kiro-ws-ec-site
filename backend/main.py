import sqlite3
import os
import time
import math
import random

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DB_PATH = os.path.join(os.path.dirname(__file__), "products.db")

app = FastAPI(title="EC Site API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# --- Products ---

@app.get("/api/products")
def list_products():
    conn = get_db()
    rows = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    return dict(row)


# --- Cart (server-side session-less: validate stock) ---

class CartItem(BaseModel):
    product_id: int
    quantity: int


@app.post("/api/cart/validate")
def validate_cart(items: list[CartItem]):
    conn = get_db()
    result = []
    for item in items:
        row = conn.execute("SELECT * FROM products WHERE id = ?", (item.product_id,)).fetchone()
        if not row:
            continue
        p = dict(row)
        p["requested_quantity"] = item.quantity
        p["available"] = item.quantity <= p["stock"]
        result.append(p)
    conn.close()
    return result


# --- Orders ---

class OrderItemIn(BaseModel):
    product_id: int
    quantity: int
    price: int


class ShippingInfo(BaseModel):
    name: str
    postal_code: str
    address: str
    phone: str


class OrderIn(BaseModel):
    items: list[OrderItemIn]
    shipping: ShippingInfo


def generate_order_number():
    ts = int(time.time() * 1000)
    rand = random.randint(0, 999)
    return f"ORD-{ts}-{rand:03d}"


@app.post("/api/orders")
def create_order(order: OrderIn):
    conn = get_db()
    order_number = generate_order_number()
    total = sum(i.price * i.quantity for i in order.items)

    cur = conn.execute(
        "INSERT INTO orders (order_number, name, postal_code, address, phone, total) VALUES (?, ?, ?, ?, ?, ?)",
        (order_number, order.shipping.name, order.shipping.postal_code, order.shipping.address, order.shipping.phone, total),
    )
    order_id = cur.lastrowid

    for item in order.items:
        conn.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
            (order_id, item.product_id, item.quantity, item.price),
        )
        conn.execute(
            "UPDATE products SET stock = stock - ? WHERE id = ? AND stock >= ?",
            (item.quantity, item.product_id, item.quantity),
        )

    conn.commit()
    conn.close()
    return {"order_number": order_number, "total": total, "status": "confirmed"}


@app.get("/api/orders/{order_number}")
def get_order(order_number: str):
    conn = get_db()
    row = conn.execute("SELECT * FROM orders WHERE order_number = ?", (order_number,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="注文が見つかりません")
    order = dict(row)
    items = conn.execute(
        """SELECT oi.*, p.name, p.image FROM order_items oi
           JOIN products p ON oi.product_id = p.id
           WHERE oi.order_id = ?""",
        (order["id"],),
    ).fetchall()
    conn.close()
    order["items"] = [dict(i) for i in items]
    return order
