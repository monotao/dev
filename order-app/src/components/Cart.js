// src/components/Cart.js
import React from 'react';
import './Cart.css';

const Cart = ({ cartItems, setCartItems }) => {
  const handleIncrease = (item) => {
    setCartItems(
      cartItems.map((cartItem) =>
        cartItem.id === item.id ? { ...cartItem, quantity: item.quantity + 1 } : cartItem
      )
    );
  };

  const handleDecrease = (item) => {
    if (item.quantity === 1) {
      setCartItems(cartItems.filter((cartItem) => cartItem.id !== item.id));
    } else {
      setCartItems(
        cartItems.map((cartItem) =>
          cartItem.id === item.id ? { ...cartItem, quantity: item.quantity - 1 } : cartItem
        )
      );
    }
  };

  const handleRemove = (item) => {
    setCartItems(cartItems.filter((cartItem) => cartItem.id !== item.id));
  };

  const handleClearCart = () => {
    setCartItems([]);
  };

  return (
    <div className="cart">
      <h2 className="cart-title">
        Cart
        {cartItems.length > 0 && (
          <button className="clear-cart-button" onClick={handleClearCart}>전체 삭제</button>
        )}
      </h2>
      {cartItems.length === 0 ? (
        <p className="cart-empty">피자를 담아주세요 :D</p>
      ) : (
        <ul className="cart-list">
          {cartItems.map((item) => (
            <li key={item.id} className="cart-item">
              <button className="remove-button" onClick={() => handleRemove(item)}>x</button>
              <span className="item-name">{item.name}</span>
              <div className="item-controls">
                <button className="cart-button" onClick={() => handleDecrease(item)}>-</button>
                <span className="item-quantity">{item.quantity}개</span>
                <button className="cart-button" onClick={() => handleIncrease(item)}>+</button>
              </div>
              <span className="item-price">{(item.price * item.quantity).toLocaleString()}원</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Cart;
