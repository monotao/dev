// airtable_data_get_test.js

const fetch = require('node-fetch');
const fs = require('fs');

const authData = JSON.parse(fs.readFileSync('/Users/lena/pass/authorization.json'));
const AIRTABLE_API_KEY = authData.airtable_pizza;
const BASE_ID = 'appFIyuKLcuwB9jmV';
const TABLE_NAME = 'order';

const fetchTableData = async () => {
  try {
    const response = await fetch(`https://api.airtable.com/v0/${BASE_ID}/${TABLE_NAME}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${AIRTABLE_API_KEY}`,
        'Content-Type': 'application/json'
      }
    });

    if (response.ok) {
      const data = await response.json();
      data.records.forEach(record => {
        console.log('Record ID:', record.id);
        console.log('Fields:', record.fields);
      });
      return data;
    } else {
      const errorData = await response.json();
      console.error('데이터 가져오기에 실패했습니다:', errorData);
    }
  } catch (error) {
    console.error('Error:', error);
    console.error('데이터 가져오는 중 오류가 발생했습니다.');
  }
};

fetchTableData();