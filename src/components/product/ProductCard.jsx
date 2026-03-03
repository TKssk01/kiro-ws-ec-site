import { memo } from 'react';
import { Button } from '../common/Button';
import { formatPrice } from '../../utils/formatters';
import './ProductCard.css';

export const ProductCard = memo(({ product, onAddToCart, onClick }) => {
  const handleAddToCart = (e) => {
    e.stopPropagation();
    onAddToCart(product);
  };

  return (
    <div className="product-card" onClick={() => onClick(product.id)}>
      <div className="product-image">{product.image}</div>
      <div className="product-info">
        <h3 className="product-name">{product.name}</h3>
        <div className="product-footer">
          <span className="product-price">{formatPrice(product.price)}</span>
          <Button variant="primary" onClick={handleAddToCart}>
            カートに追加
          </Button>
        </div>
      </div>
    </div>
  );
});

ProductCard.displayName = 'ProductCard';
