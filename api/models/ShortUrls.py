import datetime
import uuid

from models import Base
from sqlalchemy import DateTime, Column, String
from sqlalchemy.dialects.postgresql import UUID


class ShortUrls(Base):
    __tablename__ = "short_urls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_url = Column(String, nullable=False)
    short_url = Column(String, nullable=False)
    # click_count = Column(Integer, nullable=False, default=0)
    # service = Column(String, nullable=False)
    created = Column(
        DateTime,
        index=False,
        unique=False,
        nullable=False,
        default=datetime.datetime.utcnow,
    )
