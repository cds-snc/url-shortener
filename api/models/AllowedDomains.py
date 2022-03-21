import datetime
import uuid

from models import Base
from sqlalchemy import DateTime, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

"""
Class AllowedDomains
	table = allowed domains
	primary key, id - UUID type
	domain - property in the table to indicate a domain (Example is www.canada.ca)
	created - the date and time the entry was created in the database
"""
class AllowedDomains(Base):
	__tablename__ = "allowed_domains"

	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	domain = Column(String, nullable=False)
	created = Column(
		DateTime,
		index=False,
		unique=False,
		nullable=False,
		default=datetime.datetime.utcnow,
	)
