from typing import Optional
import datetime
import enum

from sqlalchemy import Enum, ForeignKeyConstraint, Index, Integer, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import ENUM, TINYINT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .animal import Animal

class AdoptionRequestHousingType(str, enum.Enum):
    HOUSE = 'house'
    APARTMENT = 'apartment'
    FARM = 'farm'
    OTHER = 'other'


class AdoptionRequestStatus(str, enum.Enum):
    PENDING = 'pending'
    CONTACTED = 'contacted'
    APPROVED = 'approved'
    REJECTED = 'rejected'

class AdoptionRequest(Base):
    __tablename__ = 'adoption_request'
    __table_args__ = (
        ForeignKeyConstraint(['animal_id'], ['animal.id'], ondelete='CASCADE', name='adoption_request_ibfk_1'),
        Index('animal_id', 'animal_id')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    animal_id: Mapped[int] = mapped_column(Integer, nullable=False)
    full_name: Mapped[str] = mapped_column(String(200, 'utf8mb4_unicode_ci'), nullable=False)
    email: Mapped[str] = mapped_column(String(200, 'utf8mb4_unicode_ci'), nullable=False)
    phone: Mapped[str] = mapped_column(String(50, 'utf8mb4_unicode_ci'), nullable=False)
    city: Mapped[str] = mapped_column(String(100, 'utf8mb4_unicode_ci'), nullable=False)
    housing_type: Mapped[AdoptionRequestHousingType] = mapped_column(Enum(AdoptionRequestHousingType, values_callable=lambda cls: [member.value for member in cls]), nullable=False)
    #animal_name: Mapped[Optional[str]] = mapped_column(String(100, 'utf8mb4_unicode_ci'))
    has_yard: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'0'"))
    has_other_pets: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'0'"))
    other_pets_description: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    has_children: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'0'"))
    children_ages: Mapped[Optional[str]] = mapped_column(String(200, 'utf8mb4_unicode_ci'))
    previous_pet_experience: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    reason_for_adoption: Mapped[Optional[str]] = mapped_column(Text(collation='utf8mb4_unicode_ci'))
    hours_alone_per_day: Mapped[Optional[int]] = mapped_column(Integer)
    agrees_to_responsibilities: Mapped[Optional[int]] = mapped_column(TINYINT(1), server_default=text("'1'"))
    status: Mapped[Optional[AdoptionRequestStatus]] = mapped_column(Enum(AdoptionRequestStatus, values_callable=lambda cls: [member.value for member in cls]), server_default=text("'pending'"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    animal: Mapped["Animal"] = relationship("Animal", back_populates="adoption_request")


