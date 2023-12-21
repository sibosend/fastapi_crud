from .database import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean, Integer
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
# from uuid import UUID
# from sqlalchemy.dialects.postgresql import UUID


class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, index=True,
                autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    category = Column(String, nullable=True)
    published = Column(Boolean, nullable=False, default=True)
    createdAt = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=func.now())
    updatedAt = Column(TIMESTAMP(timezone=True),
                       default=None, onupdate=func.now())


class Jobs(Base):
    __tablename__ = 'jobs'
    id = Column(String, primary_key=True, nullable=False)
    img_name = Column(String, nullable=False)
    img_path = Column(String, nullable=False)
    img_rgb = Column(String, nullable=True)
    img_prompt = Column(String, nullable=False)
    step = Column(Integer, nullable=False, default=0)
    d3_path = Column(String, nullable=True)
    createdAt = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=func.now())
    updatedAt = Column(TIMESTAMP(timezone=True),
                       default=None, onupdate=func.now())
