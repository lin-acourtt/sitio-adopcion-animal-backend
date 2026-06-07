from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class HousingTypeEnum(str, Enum):
    house = "house"
    apartment = "apartment"
    farm = "farm"
    other = "other"


class RequestStatusEnum(str, Enum):
    pending = "pending"
    contacted = "contacted"
    approved = "approved"
    rejected = "rejected"

class AdoptionRequestCreate(BaseModel):
    animal_id: int
    # animal_name: Optional[str] = None
    full_name: str = Field(...,
                    min_length=3, 
                    max_length=200,
                    example="Lindsey Acourtt")
    email: EmailStr
    phone: str = Field(...,
                    min_length=3, 
                    max_length=50,
                    example="3116859378")
    city: str = Field(...,
                    min_length=3, 
                    max_length=100,
                    example="Barranquilla")
    housing_type: HousingTypeEnum
    has_yard: bool = False
    has_other_pets: bool = False
    other_pets_description: Optional[str] = None
    has_children: bool = False
    children_ages: Optional[str] = Field(None,
                                    min_length=1, 
                                    max_length=200)
    previous_pet_experience: Optional[str] = None
    reason_for_adoption: Optional[str] = None
    hours_alone_per_day: Optional[int] = None
    agrees_to_responsibilities: bool = True


class AdoptionRequestOut(AdoptionRequestCreate):
    """
    Schema for the output of an adoption request.
    All attributes from AdoptionRequestCreate are inherited, plus:
    * id: The unique identifier of the adoption request.
    * animal_name: The name of the animal being adopted.
    * status: The current status of the adoption request (pending, contacted, approved, rejected).
    * created_at: The timestamp when the adoption request was created.
    """
    id: int
    # animal_id: Inherited from AdoptionRequestCreate
    animal_name: str = Field(...,
                    min_length=3, 
                    max_length=100,
                    example="Rocky")
    # full_name: Inherited from AdoptionRequestCreate
    # email: Inherited from AdoptionRequestCreate
    # phone: Inherited from AdoptionRequestCreate
    # city: Inherited from AdoptionRequestCreate
    # housing_type: Inherited from AdoptionRequestCreate
    # has_yard: Inherited from AdoptionRequestCreate
    # has_other_pets: Inherited from AdoptionRequestCreate
    # other_pets_description: Inherited from AdoptionRequestCreate
    # has_children: Inherited from AdoptionRequestCreate
    # children_ages: Inherited from AdoptionRequestCreate
    # previous_pet_experience: Inherited from AdoptionRequestCreate
    # reason_for_adoption: Inherited from AdoptionRequestCreate
    # hours_alone_per_day: Inherited from AdoptionRequestCreate
    # agrees_to_responsibilities: Inherited from AdoptionRequestCreate
    status: RequestStatusEnum
    created_at: datetime

    class Config:
        from_attributes = True

class AdoptionStatusUpdate(BaseModel):
    status: RequestStatusEnum

