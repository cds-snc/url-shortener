import pytest
from fastapi import status

def test_unknown_shorturl_returns_404(client):
    response = client.get("/doesnotexist")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_creating_a_valid_shortlink(client):
    response = client.post("/shorten", json={"original_url": "http://example.com"})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['status'] == 'OK'

def test_known_shorturl_redirects_to_original_url(client):
    create_response = client.post("/shorten", json={"original_url": "http://example.com"})
    shorturl = create_response.json()['short_url']

    # See https://github.com/tiangolo/fastapi/issues/790
    # For discussion of the allow_redirect = False
    response = client.get(f"/{shorturl}", allow_redirects = False)
    assert response.headers['location'] == 'http://example.com'
    assert response.status_code == status.HTTP_301_MOVED_PERMANENTLY
