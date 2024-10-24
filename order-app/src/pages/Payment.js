// src/pages/Payment.js
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHome } from '@fortawesome/free-solid-svg-icons';
import './Payment.css';

const Payment = () => {
  const navigate = useNavigate();

  const handleHomeButtonClick = () => {
    navigate('/');
  };

  return (
    <div className="payment-page">
      <button className="home-button" onClick={handleHomeButtonClick}>
        <FontAwesomeIcon icon={faHome} />
      </button>
      <h1>결제 수단</h1>
      <p>결제가 어려우신 경우 직원에게 문의부탁드립니다.</p>
      <div className="payment-images">
        <div className="payment-card">
          <div className="payment-card-title">카카오 QR 코드</div>
          <img src="/images/qr_kakao.jpg" alt="qr_kakao" className="payment-image" />
        </div>
        <div className="payment-card">
          <div className="payment-card-title">네이버 QR 코드</div>
          <img src="/images/qr_naver.jpg" alt="qr_naver" className="payment-image" />
        </div>
        <div className="payment-card">
          <div className="payment-card-title">카카오 오픈채팅</div>
          <img src="/images/kakao_openchat.jpg" alt="kakao_openchat" className="payment-image" />
          <div className="payment-card-description">피자가 완성되면 알려드려요</div>
        </div>
      </div>
    </div>
  );
};

export default Payment;