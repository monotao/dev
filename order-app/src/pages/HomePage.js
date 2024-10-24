// src/pages/HomePage.js
import React, { useState } from 'react';
import ProductList from '../components/ProductList';
import Cart from '../components/Cart';
import Order from '../components/Order';
import './HomePage.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHome, faCreditCard } from '@fortawesome/free-solid-svg-icons';
import { useNavigate } from 'react-router-dom';

const products = [
  { id: 1, name: '페퍼로니피자(1조각)', price: 2500, image: '/images/pepperoni_pizza_slice.jpg' },
  { id: 2, name: '어니언피자(1조각)', price: 3000, image: '/images/onion_pizza_slice.jpg' },
  { id: 3, name: '페퍼로니피자', price: 11000, image: '/images/pepperoni_pizza.jpg' },
  { id: 4, name: '어니언피자', price: 13900, image: '/images/onion_pizza.jpg' },
];

const HomePage = () => {
  const [cartItems, setCartItems] = useState([]);
  const [clickCount, setClickCount] = useState(0);
  const [lastClickTime, setLastClickTime] = useState(0);
  const navigate = useNavigate();

  const handleProductClick = (product) => {
    const existingItem = cartItems.find((item) => item.id === product.id);
    if (existingItem) {
      setCartItems(
        cartItems.map((item) =>
          item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
        )
      );
    } else {
      setCartItems([...cartItems, { ...product, quantity: 1 }]);
    }
  };

  const handleHomeButtonClick = () => {
    const currentTime = Date.now();
    if (currentTime - lastClickTime < 1000) {
      setClickCount((prevCount) => {
        const newCount = prevCount + 1;
        if (newCount === 5) {
          console.log('localStorage has been cleared.');
          localStorage.clear();
          setClickCount(0);
        }
        return newCount;
      });
    } else {
      setClickCount(1);
    }
    setLastClickTime(currentTime);
  };

  const handlePaymentButtonClick = () => {
    navigate('/payment');
  };

  return (
    <div className="home-page">
      <button className="home-button" onClick={handleHomeButtonClick}>
        <FontAwesomeIcon icon={faHome} />
      </button>
      <button className="payment-button" onClick={handlePaymentButtonClick}>
        <FontAwesomeIcon icon={faCreditCard} />
      </button>
      <h1 className="home-title">크게될피자</h1>
      <div className="product-list-section">
        <ProductList products={products} onProductClick={handleProductClick} />
      </div>
      <div className="cart-and-order-container">
        <div className="cart-container">
          <Cart cartItems={cartItems} setCartItems={setCartItems} />
        </div>
        <div className="order-container">
          <Order cartItems={cartItems} clickCount={clickCount} />
        </div>
      </div>
    </div>
  );
};

export default HomePage;