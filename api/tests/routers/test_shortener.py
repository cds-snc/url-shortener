from fastapi import status

from unittest.mock import patch


def test_unknown_shorturl_returns_404(client):
    response = client.get("/doesnotexist")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@patch("routers.shortener.validate_cookie")
def test_GET_homepage_returns_307_if_not_logged_in(mock_validate_cookie, client):
    mock_validate_cookie.return_value = False
    response = client.get("/", follow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT


@patch("routers.shortener.validate_cookie")
def test_GET_homepage_returns_200_if_logged_in(mock_validate_cookie, client):
    mock_validate_cookie.return_value = True
    response = client.get("/", follow_redirects=False)
    assert response.status_code == status.HTTP_200_OK


@patch("routers.shortener.validate_cookie")
def test_POST_homepage_returns_200_if_logged_in(mock_validate_cookie, client):
    mock_validate_cookie.return_value = True
    response = client.post("/", data={"original_url": "https://www.canada.ca"})
    assert response.status_code == status.HTTP_200_OK


def test_POST_homepage_returns_401_if_not_logged_in(client):
    response = client.post("/", data={"original_url": "https://www.canada.ca"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_GET_login_returns_200(client):
    response = client.get("/login")
    assert response.status_code == status.HTTP_200_OK


@patch("routers.shortener.create_magic_link")
def test_POST_login_returns_200_with_success_message_if_in_domain_list(
    mock_create_magic_link, client
):
    mock_create_magic_link.return_value = {"success": "Success!"}
    response = client.post("/login", data={"email": "foo@canada.ca"})
    assert response.status_code == status.HTTP_200_OK
    assert "Success!" in response.text
    mock_create_magic_link.assert_called_once()


@patch("routers.shortener.create_magic_link")
def test_POST_login_returns_200_with_error_message_if_not_in_domain_list(
    mock_create_magic_link, client
):
    response = client.post("/login", data={"email": "foo@bar.com"})
    assert response.status_code == status.HTTP_200_OK
    mock_create_magic_link.assert_not_called()


@patch("routers.shortener.create_magic_link")
def test_POST_login_returns_200_with_error_message_if_magic_link_fails(
    mock_create_magic_link, client
):
    mock_create_magic_link.return_value = {"error": "Error!"}
    response = client.post("/login", data={"email": "foo@canada.ca"})
    assert response.status_code == status.HTTP_200_OK
    assert "Error!" in response.text
    mock_create_magic_link.assert_called_once()


@patch("routers.shortener.create_magic_link")
def test_POST_login_returns_200_with_error_message_if_email_is_invalid(
    mock_create_magic_link, client
):
    mock_create_magic_link.return_value = {"error": "Error!"}
    response = client.post("/login", data={"email": "foo"})
    assert response.status_code == status.HTTP_200_OK
    assert "Not a valid email address" in response.text
    mock_create_magic_link.assert_not_called()


@patch("routers.shortener.delete_cookie")
def test_GET_logout_returns_307(mock_delete_cookie, client):
    response = client.get("/logout", follow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    mock_delete_cookie.assert_called_once()


@patch("routers.shortener.validate_magic_link")
@patch("routers.shortener.set_cookie")
def test_GET_magic_link_returns_307_if_valid_and_sets_cookie(
    mock_set_cookie, mock_validate_magic_link, client
):
    mock_validate_magic_link.return_value = {"success": "Success!"}
    response = client.get(
        "/magic_link?guid=123&email=foo@canada.ca", follow_redirects=False
    )
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    mock_set_cookie.assert_called_once()
    mock_validate_magic_link.assert_called_once()


@patch("routers.shortener.validate_magic_link")
@patch("routers.shortener.set_cookie")
def test_GET_magic_link_returns_200_if_invalid_and_does_not_set_cookie(
    mock_set_cookie, mock_validate_magic_link, client
):
    mock_validate_magic_link.return_value = {"error": "Error!"}
    response = client.get(
        "/magic_link?guid=123&email=foo@canada.ca", follow_redirects=False
    )
    assert response.status_code == status.HTTP_200_OK
    assert "Error!" in response.text
    mock_set_cookie.assert_not_called()
    mock_validate_magic_link.assert_called_once()


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

    response = client.get(f"/{shorturl}", follow_redirects=False)
    assert "https://www.canada.ca/en/services/jobs/opportunities.html" in response.text
    assert response.status_code == status.HTTP_200_OK
