import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

if os.environ.get("CI"):
    connection_string = os.environ.get("SQLALCHEMY_DATABASE_TEST_URI")
else:
    connection_string = os.environ.get("SQLALCHEMY_DATABASE_URI")
# Timeout is set to 10 seconds
#db_engine = create_engine(connection_string, connect_args={"connect_timeout": 10})
db_engine = create_engine("postgresql://dev:dev@db:5432/dev", connect_args={"connect_timeout": 10})
db_session = sessionmaker(bind=db_engine)


def get_db_session():
    session = db_session()
    try:
        yield session
    finally:
        session.close()


def get_db_version(session):
    query = "SELECT version_num FROM alembic_version"
    full_name = session.execute(query).fetchone()[0]
    return full_name
