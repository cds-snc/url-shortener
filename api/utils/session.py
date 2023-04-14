import os
import uuid

from fastapi import HTTPException, status, Request
from models.Session import create, read, delete

COOKIE_NAME = "_sessionID"


def delete_cookie(request, response):
    try:
        delete(request.cookies[COOKIE_NAME])
    except KeyError:
        pass
    response.delete_cookie(key=COOKIE_NAME)
    return response


def set_cookie(response, session_data):
    session_id = uuid.uuid4()
    if create(session_id, session_data):
        response.set_cookie(
            key=COOKIE_NAME,
            value=session_id,
            httponly=True,
            max_age=60 * 60 * 2,  # 2 hours
            expires=60 * 60 * 2,  # 2 hours
            samesite="lax",
        )
        return response
    else:
        return False


def validate_cookie(request):
    if "CYPRESS_CI" in os.environ:
        return True
    if COOKIE_NAME in request.cookies:
        session_id = request.cookies[COOKIE_NAME]
        session_data = read(session_id)
        if session_data:
            return session_data
        else:
            return False
    else:
        return False


def validate_user_email(request: Request):
    """
    Validates the user's email address exists in the cookie session
    data.  If it is not found, a 401 Unauthorized error is raised as this
    method is used as a dependency for routes that require a logged in user.
    """
    user_email = None
    session_data = validate_cookie(request)

    if session_data and session_data.get("session_data"):
        user_email = session_data["session_data"].get("S")

    if not user_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user_email
