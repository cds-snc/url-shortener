import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  duration: '1m',
  vus: 20,
  thresholds: {
    http_req_failed: ['rate<0.01'], // http errors should be less than 1%
    http_req_duration: ['p(95)<500'], // 95 percent of response times must be below 500ms
  },
};

export default function () {
  const get_resp = http.get('http://127.0.0.1:8000/foobar');
  sleep(1);
  const data = JSON.stringify({ "original_url": "https://digital.canada.ca" })
  const post_resp = http.post('http://127.0.0.1:8000/v1', data, { headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer auth_token_app' } });
  sleep(1);
}