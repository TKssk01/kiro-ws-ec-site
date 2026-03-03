import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "products.db")

PRODUCTS = [
    (1, "ノートパソコン", 89800, "💻", 10, "electronics"),
    (2, "ワイヤレスマウス", 2980, "🖱️", 25, "accessories"),
    (3, "キーボード", 5980, "⌨️", 15, "accessories"),
    (4, "モニター", 24800, "🖥️", 8, "electronics"),
    (5, "ヘッドフォン", 12800, "🎧", 20, "audio"),
    (6, "Webカメラ", 8900, "📷", 12, "electronics"),
    (7, "スマートフォン", 78000, "📱", 5, "electronics"),
    (8, "タブレット", 45000, "📲", 7, "electronics"),
    (9, "スマートウォッチ", 32000, "⌚", 10, "wearables"),
    (10, "ワイヤレスイヤホン", 18000, "🎵", 18, "audio"),
    (11, "プリンター", 15800, "🖨️", 6, "electronics"),
    (12, "USBメモリ", 1980, "💾", 30, "storage"),
    (13, "外付けHDD", 9800, "💿", 14, "storage"),
    (14, "ゲームコントローラー", 6800, "🎮", 22, "gaming"),
    (15, "スピーカー", 22000, "🔊", 9, "audio"),
]


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS products")
    c.execute("DROP TABLE IF EXISTS orders")
    c.execute("DROP TABLE IF EXISTS order_items")
    c.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            image TEXT NOT NULL,
            stock INTEGER NOT NULL,
            category TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            postal_code TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            total INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'confirmed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    c.executemany(
        "INSERT INTO products (id, name, price, image, stock, category) VALUES (?, ?, ?, ?, ?, ?)",
        PRODUCTS,
    )
    conn.commit()
    conn.close()
    print(f"Database initialized: {DB_PATH}")


if __name__ == "__main__":
    init_db()
