import os
from utils import session

from unittest.mock import MagicMock, patch


@patch("utils.session.delete")
def test_delete_cookie_deletes_cookie(mock_delete):
    mock_request = MagicMock()
    mock_request.cookies = {"_sessionID": "session_id"}
    mock_response = MagicMock()
    session.delete_cookie(mock_request, mock_response)
    mock_delete.assert_called_once_with("session_id")
    mock_response.delete_cookie.assert_called_once_with(key="_sessionID")


@patch("utils.session.delete")
def test_delete_cookie_does_not_delete_cookie_if_cookie_does_not_exist(mock_delete):
    mock_request = MagicMock()
    mock_request.cookies = {}
    mock_response = MagicMock()
    mock_delete.side_effect = Exception("Should not be called")
    session.delete_cookie(mock_request, mock_response) == mock_response
    mock_response.delete_cookie.assert_called_once_with(key="_sessionID")


@patch("utils.session.create")
def test_set_cookie_returns_false_if_session_could_not_be_created(mock_create):
    mock_create.return_value = False
    mock_response = MagicMock()
    assert session.set_cookie(mock_response, "session_data") is False
    mock_response.set_cookie.assert_not_called()


@patch("utils.session.create")
def test_set_cookie_returns_response_if_session_was_created(mock_create):
    mock_create.return_value = True
    mock_response = MagicMock()
    assert session.set_cookie(mock_response, "session_data") == mock_response
    mock_response.set_cookie.assert_called_once()


@patch("utils.session.read")
def test_validate_cookie_returns_false_if_session_does_not_exist(mock_read):
    mock_read.return_value = False
    mock_request = MagicMock()
    mock_request.cookies = {"_sessionID": "session_id"}
    assert session.validate_cookie(mock_request) is False


@patch("utils.session.read")
def test_validate_cookie_returns_false_if_session_id_does_not_exist(mock_read):
    mock_read.return_value = False
    mock_request = MagicMock()
    mock_request.cookies = {}
    assert session.validate_cookie(mock_request) is False


@patch("utils.session.read")
def test_validate_cookie_returns_session_data_if_session_exists(mock_read):
    mock_read.return_value = "session_data"
    mock_request = MagicMock()
    mock_request.cookies = {"_sessionID": "session_id"}
    assert session.validate_cookie(mock_request) == "session_data"


@patch.dict(os.environ, {"CYPRESS_CI": "1"}, clear=True)
def test_validate_cookie_returns_true_if_cypress_ci_is_set():
    mock_request = MagicMock()
    assert session.validate_cookie(mock_request) is True
