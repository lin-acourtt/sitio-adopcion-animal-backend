from typing import Optional
import datetime
import enum

from sqlalchemy import Enum, ForeignKeyConstraint, Index, Integer, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import ENUM, TINYINT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Admin(Base):
    __tablename__ = 'admin'
    __table_args__ = (
        Index('username', 'username', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100, 'utf8mb4_unicode_ci'), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
