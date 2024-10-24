// airtable_data_test.js

const fetch = require('node-fetch');
const fs = require('fs');

// Load API key from JSON file
const authData = JSON.parse(fs.readFileSync('/Users/lena/pass/authorization.json'));
const AIRTABLE_API_KEY = authData.airtable_pizza;

const cartItems = [
  { id: 1, name: '페퍼로니피자(1조각)', quantity: 2, price: 2500 },
  { id: 2, name: '어니언피자(1조각)', quantity: 1, price: 3000 },
];

// Load last order number from local file or set it to 0
const orderNoFilePath = '/Users/lena/dev/order-app/src/components/last_order_no.json';
let lastOrderNo = 0;
if (fs.existsSync(orderNoFilePath)) {
  const orderData = JSON.parse(fs.readFileSync(orderNoFilePath));
  lastOrderNo = orderData.lastOrderNo || 0;
}

const testAirtableDataInsertion = async () => {
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
      // Save the last order number to the local file
      fs.writeFileSync(orderNoFilePath, JSON.stringify({ lastOrderNo: orderNo }));
    } else {
      const errorData = await response.json();
      console.error('주문 적재에 실패했습니다:', errorData);
    }
  } catch (error) {
    console.error('Error:', error);
    console.error('주문 적재 중 오류가 발생했습니다.');
  }
};

testAirtableDataInsertion();