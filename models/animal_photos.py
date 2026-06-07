from typing import Optional
import datetime
import enum

from sqlalchemy import Enum, ForeignKeyConstraint, Index, Integer, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import ENUM, TINYINT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .animal import Animal

class AnimalPhotos(Base):
    __tablename__ = 'animal_photos'
    __table_args__ = (
        ForeignKeyConstraint(['animal_id'], ['animal.id'], ondelete='CASCADE', name='animal_photos_ibfk_1'),
        Index('animal_id', 'animal_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    animal_id: Mapped[int] = mapped_column(Integer, nullable=False)
    photo_url: Mapped[str] = mapped_column(String(700, 'utf8mb4_unicode_ci'), nullable=False)
    caption: Mapped[Optional[str]] = mapped_column(String(255, 'utf8mb4_unicode_ci'))
    order_index: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("'0'"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    animal: Mapped['Animal'] = relationship('Animal', back_populates='animal_photos')
