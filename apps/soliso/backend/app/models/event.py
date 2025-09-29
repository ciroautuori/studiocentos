from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.sql import expression
from sqlalchemy.dialects.postgresql import JSONB
from app.core.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    location = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    additional_images = Column(
        JSONB, default=list, nullable=False)  # Array di immagini
    is_featured = Column(
        Boolean, server_default=expression.false(), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(),
                        onupdate=func.now(), nullable=False)
