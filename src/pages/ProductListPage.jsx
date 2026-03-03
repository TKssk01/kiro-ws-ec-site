import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { ProductGrid } from '../components/product/ProductGrid';
import { Message } from '../components/common/Message';
import { api } from '../utils/api';
import './ProductListPage.css';

export const ProductListPage = () => {
  const navigate = useNavigate();
  const { addToCart } = useCart();
  const [message, setMessage] = useState(null);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getProducts()
      .then(setProducts)
      .catch(() => setMessage({ type: 'error', text: '商品の取得に失敗しました' }))
      .finally(() => setLoading(false));
  }, []);

  const handleAddToCart = (product) => {
    addToCart(product, 1);
    setMessage({
      type: 'success',
      text: `${product.image} ${product.name}をカートに追加しました`
    });
  };

  const handleProductClick = (productId) => {
    navigate(`/product/${productId}`);
  };

  if (loading) {
    return <div style={{ textAlign: 'center', padding: '2rem' }}>読み込み中...</div>;
  }

  return (
    <div className="product-list-page">
      {message && (
        <Message
          type={message.type}
          message={message.text}
          onClose={() => setMessage(null)}
        />
      )}
      
      <h1 className="page-title">商品一覧</h1>
      
      <ProductGrid
        products={products}
        onAddToCart={handleAddToCart}
        onProductClick={handleProductClick}
      />
    </div>
  );
};
