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
    response = client.post("/v1", json={"original_url": "https://www.canada.ca"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["status"] == "OK"


def test_creating_a_blocked_shortlink(client):
    response = client.post("/v1", json={"original_url": "https://www.example.ca"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_creating_a_blocked_shortlink_with_ending_match(client):
    response = client.post("/v1", json={"original_url": "https://www.examplegc.ca"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response = client.post("/v1", json={"original_url": "https://www.examplecanada.ca"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_known_shorturl_displays_original_url(client):
    response = client.post(
        "/v1",
        json={
            "original_url": "https://www.canada.ca/en/services/jobs/opportunities.html"
        },
    )
    shorturl = response.json()["short_url"].split("/")[-1]

    response = client.get(f"/{shorturl}")
    assert "https://www.canada.ca/en/services/jobs/opportunities.html" in response.text
    assert response.status_code == status.HTTP_200_OK
