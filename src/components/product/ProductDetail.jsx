import { useState } from 'react';
import { Button } from '../common/Button';
import { formatPrice } from '../../utils/formatters';
import './ProductDetail.css';

export const ProductDetail = ({ product, onAddToCart, onBack }) => {
  const [quantity, setQuantity] = useState(1);

  const handleQuantityChange = (e) => {
    const value = parseInt(e.target.value);
    if (value > 0 && value <= product.stock) {
      setQuantity(value);
    }
  };

  const handleAddToCart = () => {
    onAddToCart(product, quantity);
  };

  return (
    <div className="product-detail">
      <Button variant="secondary" onClick={onBack} className="back-button">
        ← 戻る
      </Button>
      
      <div className="product-detail-content">
        <div className="product-detail-image">{product.image}</div>
        
        <div className="product-detail-info">
          <h1 className="product-detail-name">{product.name}</h1>
          <p className="product-detail-price">{formatPrice(product.price)}</p>
          
          <div className="product-detail-stock">
            在庫: {product.stock > 0 ? `${product.stock}個` : '在庫切れ'}
          </div>
          
          {product.stock > 0 && (
            <div className="product-detail-actions">
              <div className="quantity-selector">
                <label htmlFor="quantity">数量:</label>
                <input
                  id="quantity"
                  type="number"
                  min="1"
                  max={product.stock}
                  value={quantity}
                  onChange={handleQuantityChange}
                />
              </div>
              <Button variant="primary" onClick={handleAddToCart}>
                カートに追加
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
