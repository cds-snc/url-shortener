from fastapi import status


def test_unknown_shorturl_returns_404(client):
    response = client.get("/doesnotexist")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_GET_homepage_returns_200(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK


def test_POST_homepage_returns_200(client):
    response = client.post("/", data={"original_url": "https://www.canada.ca"})
    assert response.status_code == status.HTTP_200_OK


def test_creating_a_valid_shortlink(client):
    response = client.post("/shorten", json={"original_url": "https://www.canada.ca"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["status"] == "OK"


def test_known_shorturl_redirects_to_original_url(client):
    response = client.post("/shorten", json={"original_url": "https://www.canada.ca"})
    shorturl = response.json()["short_url"]

    # See https://github.com/tiangolo/fastapi/issues/790
    # For discussion of the allow_redirect = False
    response = client.get(f"/{shorturl}", allow_redirects=False)
    assert response.headers["location"] == "https://www.canada.ca"
    assert response.status_code == status.HTTP_302_FOUND
