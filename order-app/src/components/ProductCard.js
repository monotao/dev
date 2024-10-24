// src/components/ProductCard.js
import React from 'react';
import './ProductCard.css';

const ProductCard = ({ product, onProductClick }) => {
  return (
    <div className="product-card" onClick={() => onProductClick(product)}>
      <img src={product.image} alt={product.name} />
      <h3 className="product-name">{product.name}</h3>
      <p className="product-price">{product.price.toLocaleString()}원</p>
    </div>
  );
};

export default ProductCard;