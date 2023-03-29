import uuid

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
    if COOKIE_NAME in request.cookies:
        session_id = request.cookies[COOKIE_NAME]
        session_data = read(session_id)
        if session_data:
            return session_data
        else:
            return False
    else:
        return False
