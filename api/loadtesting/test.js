import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  duration: '1m',
  vus: 20,
  thresholds: {
    'http_req_failed{name:redirectPage}': ['rate<0.01'], // http errors should be less than 1%
    'http_req_duration{name:redirectPage}': ['p(95)<500'], // 95 percent of response times must be below 500ms
    'http_req_failed{name:createShortUrl}': ['rate<0.01'], // http errors should be less than 1%
    'http_req_duration{name:createShortUrl}': ['p(95)<750'], // 95 percent of response times must be below 750ms
  },
};

export default function () {
  http.get('http://0.0.0.0:8000/foobared', { tags: { name: 'redirectPage' } });

  sleep(1);

  const data = JSON.stringify({ "original_url": "https://digital.canada.ca" })
  const params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer auth_token_app'
    },
    tags: { name: 'createShortUrl' }
  }

  http.post('http://0.0.0.0:8000/v1', data, params);
  sleep(1);
};