// src/components/Order.js
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Order.css';
import authData from '../config/authorization.json'; // JSON 파일을 import

const AIRTABLE_API_KEY = authData.airtable_pizza;

let lastOrderNo = parseInt(localStorage.getItem('lastOrderNo') || '0', 10);

const Order = ({ cartItems, clickCount }) => {
  const totalAmount = cartItems.reduce((total, item) => total + item.price * item.quantity, 0);
  const [internalClickCount, setInternalClickCount] = useState(clickCount);
  const navigate = useNavigate();

  useEffect(() => {
    if (internalClickCount === 5) {
      console.log('localStorage has been cleared from Order component.');
      alert('localStorage has been cleared.');
      localStorage.clear();
      lastOrderNo = 0; // Reset the lastOrderNo in memory
      localStorage.setItem('lastOrderNo', lastOrderNo);
      setInternalClickCount(0); // reset the internal click count after clearing
    }
  }, [internalClickCount]);

  useEffect(() => {
    setInternalClickCount(clickCount);
  }, [clickCount]);

  const handleOrder = async () => {
    try {
      const orderNo = lastOrderNo + 1;
      const response = await fetch('https://api.airtable.com/v0/appFIyuKLcuwB9jmV/order', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${AIRTABLE_API_KEY}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          records: cartItems.map((cartItem) => ({
            fields: {
              order_no: orderNo,
              item_id: cartItem.id,
              item: cartItem.name,
              quantity: cartItem.quantity,
              price: cartItem.price,
              status: '주문'
            }
          }))
        })
      });
      
      if (response.ok) {
        console.log('주문이 성공적으로 적재되었습니다!');
        lastOrderNo = orderNo;
        localStorage.setItem('lastOrderNo', lastOrderNo);
        navigate('/payment'); // 주문 성공 시 새로운 페이지로 이동
      } else {
        const errorData = await response.json();
        console.error('주문 적재에 실패했습니다:', errorData);
      }
    } catch (error) {
      console.error('Error:', error);
      console.error('주문 적재 중 오류가 발생했습니다.');
    }
  };

  return (
    <div className="order">
      <button className="checkout-button" onClick={handleOrder}>
        {totalAmount.toLocaleString()}원 결제하기
      </button>
    </div>
  );
};

export default Order;