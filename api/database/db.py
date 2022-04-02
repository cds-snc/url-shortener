import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Base = declarative_base()
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    session = DBSession()
    try:
        yield session
    finally:
        session.close()


def get_db_version(session):
    query = "SELECT version_num FROM alembic_version"
    full_name = session.execute(query).fetchone()[0]
    return full_name
