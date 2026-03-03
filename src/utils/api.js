const API_BASE = "http://localhost:8000/api";

export const api = {
  async getProducts() {
    const res = await fetch(`${API_BASE}/products`);
    if (!res.ok) throw new Error("商品の取得に失敗しました");
    return res.json();
  },

  async getProduct(id) {
    const res = await fetch(`${API_BASE}/products/${id}`);
    if (!res.ok) throw new Error("商品が見つかりません");
    return res.json();
  },

  async validateCart(items) {
    const res = await fetch(`${API_BASE}/cart/validate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(
        items.map((item) => ({
          product_id: item.id,
          quantity: item.quantity,
        }))
      ),
    });
    if (!res.ok) throw new Error("カートの検証に失敗しました");
    return res.json();
  },

  async createOrder(items, shippingInfo) {
    const res = await fetch(`${API_BASE}/orders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        items: items.map((item) => ({
          product_id: item.id,
          quantity: item.quantity,
          price: item.price,
        })),
        shipping: {
          name: shippingInfo.name,
          postal_code: shippingInfo.postalCode,
          address: shippingInfo.address,
          phone: shippingInfo.phone,
        },
      }),
    });
    if (!res.ok) throw new Error("注文の作成に失敗しました");
    return res.json();
  },
};
