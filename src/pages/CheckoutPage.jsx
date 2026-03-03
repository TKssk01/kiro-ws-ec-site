import { useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { CheckoutForm } from '../components/checkout/CheckoutForm';
import { OrderSummary } from '../components/checkout/OrderSummary';
import { api } from '../utils/api';
import './CheckoutPage.css';

export const CheckoutPage = () => {
  const navigate = useNavigate();
  const { cart, cartTotal, clearCart } = useCart();

  if (cart.length === 0) {
    navigate('/cart');
    return null;
  }

  const handleSubmit = async ({ shippingInfo }) => {
    const result = await api.createOrder(cart, shippingInfo);
    clearCart();
    navigate(`/order-confirmation/${result.order_number}`, {
      state: {
        orderDetails: {
          orderNumber: result.order_number,
          items: cart,
          subtotal: cartTotal,
          shippingFee: 0,
          total: cartTotal,
          shippingInfo,
          orderDate: new Date(),
          status: result.status,
        },
      },
    });
  };

  const handleCancel = () => {
    navigate('/cart');
  };

  return (
    <div className="checkout-page">
      <h1 className="page-title">チェックアウト</h1>
      
      <div className="checkout-content">
        <div className="checkout-form-section">
          <CheckoutForm onSubmit={handleSubmit} onCancel={handleCancel} />
        </div>
        
        <div className="checkout-summary-section">
          <OrderSummary items={cart} total={cartTotal} />
        </div>
      </div>
    </div>
  );
};
