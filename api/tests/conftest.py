import os
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from database.db import get_db_session
from models import Base

from main import app

db_engine = create_engine(os.environ.get("DATABASE_TEST_URL"))
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


def get_test_db_session() -> Session:
    connection = db_engine.connect()
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()
        connection.close()


@pytest.fixture(scope="session")
def setup_test_database():
    Base.metadata.bind = db_engine
    Base.metadata.create_all()
    yield
    Base.metadata.drop_all()


@pytest.fixture(scope="session")
def client(setup_test_database) -> TestClient:
    app.dependency_overrides[get_db_session] = get_test_db_session
    client = TestClient(app)
    yield client
