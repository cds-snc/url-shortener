import http from 'k6/http';
import { sleep } from 'k6';

const HOST = __ENV.SHORTENER_DOMAIN || 'http://0.0.0.0:8000/';

export const options = {
  discardResponseBodies: true,
  scenarios: {
    createShortUrl: {
      executor: 'constant-vus',
      exec: 'createShortUrl',
      vus: 50,
      duration: '30s',
      gracefulStop: '0s',
    },
    redirectPage: {
      executor: 'constant-vus',
      exec: 'redirectPage',
      vus: 100,
      duration: '30s',
      gracefulStop: '0s',
      startTime: '30s',
    },
  },
  thresholds: {
    'http_req_failed{name:redirectPage}': ['rate<0.01'], // http errors should be less than 1%
    'http_req_duration{name:redirectPage}': ['p(95)<500'], // 95 percent of response times must be below 500ms
    'http_req_failed{name:createShortUrl}': ['rate<0.01'], // http errors should be less than 1%
    'http_req_duration{name:createShortUrl}': ['p(95)<2500'], // 95 percent of response times must be below 2000ms
  },
};


export function redirectPage() {
  http.get(`${HOST}abcdefgh`, { tags: { name: 'redirectPage' } });
  sleep(1);
}

export function createShortUrl() {
  const data = JSON.stringify({ "original_url": "https://digital.canada.ca" })
  const params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer auth_token_app'
    },
    tags: { name: 'createShortUrl' }
  }

  http.post(`${HOST}v1`, data, params);
  sleep(1);
}