import http from 'k6/http';
import { sleep } from 'k6';


const ENVIROMENT = __ENV.ENV || 'dev';

const profiles = {
  ci: {
    host: 'http://0.0.0.0:8000/',
    createShortUrlVus: 10,
    duration_p95_createShortUrl: '3000',
    redirectPageVus: 100,
    duration_p95_redirectPage: '500',
  },
  dev: {
    host: 'http://127.0.0.1:8000/',
    createShortUrlVus: 25,
    duration_p95_createShortUrl: '1000',
    redirectPageVus: 100,
    duration_p95_redirectPage: '500',
  },
  staging: {
    host: 'https://url-shortener.cdssandbox.xyz/',
    createShortUrlVus: 50,
    duration_p95_createShortUrl: '1000',
    redirectPageVus: 100,
    duration_p95_redirectPage: '500',
  },
}

export const options = {
  discardResponseBodies: true,
  scenarios: {
    createShortUrl: {
      executor: 'constant-vus',
      exec: 'createShortUrl',
      vus: profiles[ENVIROMENT].createShortUrlVus,
      duration: '30s',
      gracefulStop: '0s',
    },
    redirectPage: {
      executor: 'constant-vus',
      exec: 'redirectPage',
      vus: profiles[ENVIROMENT].redirectPageVus,
      duration: '30s',
      gracefulStop: '0s',
      startTime: '30s',
    },
  },
  thresholds: {
    'http_req_failed{name:redirectPage}': ['rate<0.01'], // http errors should be less than 1%
    'http_req_duration{name:redirectPage}': [`p(95)<${profiles[ENVIROMENT].duration_p95_redirectPage}`],
    'http_req_failed{name:createShortUrl}': ['rate<0.01'], // http errors should be less than 1%
    'http_req_duration{name:createShortUrl}': [`p(95)<${profiles[ENVIROMENT].duration_p95_createShortUrl}`],
  },
};

console.log(`Running load test against ${ENVIROMENT} environment`)

export function redirectPage() {
  http.get(`${profiles[ENVIROMENT].host}abcdefgh`, { tags: { name: 'redirectPage' } });
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

  http.post(`${profiles[ENVIROMENT].host}v1`, data, params);
  sleep(1);
}