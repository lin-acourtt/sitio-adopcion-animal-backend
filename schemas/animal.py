from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime
from schemas.animal_photos import PhotoOut

class SpeciesEnum(str, Enum):
    dog = "dog"
    cat = "cat"

class GenderEnum(str, Enum):
    male = "male"
    female = "female"

class AnimalBase(BaseModel):
    name: str = Field(...,
                    min_length=3, 
                    max_length=100,
                    example="Rocky")
    species: SpeciesEnum
    breed: Optional[str] = Field(None,
                                min_length=3, 
                                max_length=100,
                                example="Pinscher")
    age_years: int = Field(..., 
                            ge=0,
                            le=30,
                            example=3)
    age_months: int = Field(...,
                            ge=0,
                            le=11,
                            example=6)
    gender: GenderEnum
    is_neutered: bool = False
    is_vaccinated: bool = False
    personality: Optional[str] = Field(None,
                                    example="Cariñoso y juguetón.")
    story: Optional[str] = Field(None,
                                example="Rescatado de la calle, busca un hogar amoroso.")
    adopter_responsibilities: Optional[str] = Field(None,
                                                example="Castración, vacunas al día, paseos diarios y mucho amor.")
    is_available: bool = True


class AnimalCreate(AnimalBase):
    pass


class AnimalUpdate(BaseModel):
    name: Optional[str] = Field(None,
                            min_length=3, 
                            max_length=100)
    species: Optional[SpeciesEnum] = None
    breed: Optional[str] = Field(None,
                                min_length=3, 
                                max_length=100)
    age_years: Optional[int] = Field(None, 
                                    ge=0,
                                    le=30)
    age_months: Optional[int] = Field(None,
                                        ge=0,
                                        le=11,
                                        example=6)
    gender: Optional[GenderEnum] = None
    is_neutered: Optional[bool] = None
    is_vaccinated: Optional[bool] = None
    personality: Optional[str] = None
    story: Optional[str] = None
    adopter_responsibilities: Optional[str] = None
    is_available: Optional[bool] = None

class AnimalPhotoOut(AnimalBase):
    id: int
    name: str
    cover_photo_url: Optional[str] = None
    photos: Optional[List[PhotoOut]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AnimalResponse(BaseModel):
    id: int
    name: str
    species: SpeciesEnum
    breed: Optional[str] = None
    age_years: int
    age_months: int
    gender: GenderEnum
    is_neutered: bool
    is_vaccinated: bool
    is_available: bool
    personality: Optional[str] = None
    story: Optional[str] = None
    adopter_responsibilities: Optional[str] = None
    cover_photo_url: Optional[str] = None

    class Config:
        from_attributes = True

