from typing import Optional
import datetime
import enum

from sqlalchemy import Enum, ForeignKeyConstraint, Index, Integer, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import ENUM, TINYINT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class AnimalGender(str, enum.Enum):
    MALE = 'male'
    FEMALE = 'female'


class AnimalSpecies(str, enum.Enum):
    DOG = 'dog'
    CAT = 'cat'


class Animal(Base):
    __tablename__ = 'animal'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100, 'utf8mb4_unicode_ci'), nullable=False)
    species: Mapped[AnimalSpecies] = mapped_column(Enum(AnimalSpecies, values_callable=lambda cls: [member.value for member in cls]), nullable=False)
    gender: Mapped[AnimalGender] = mapped_column(Enum(AnimalGender, values_callable=lambda cls: [member.value for member in cls]), nullable=False)
    breed: Mapped[Optional[str]] = mapped_column(String(100, 'utf8mb4_unicode_ci'))
    age_years: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("'0'"))
    age_months: Mapped[Optional[int]] = mapped_column(Integer, server_default=text("'0'"))
    is_neutered: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'0'"))
    is_vaccinated: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'0'"))
    personality: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    story: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    adopter_responsibilities: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    is_available: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'1'"))
    cover_photo_url: Mapped[Optional[str]] = mapped_column(String(700, 'utf8mb4_unicode_ci'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    adoption_request: Mapped[list['AdoptionRequest']] = relationship('AdoptionRequest', back_populates='animal')
    animal_photos: Mapped[list['AnimalPhotos']] = relationship('AnimalPhotos', back_populates='animal')
