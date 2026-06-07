from pydantic import BaseModel, Field
from typing import Optional

class PhotoBase(BaseModel):
    "Base model for photo creation and updates"
    "* animal_id: ID of the associated animal (required)"
    "* photo_url: URL of the photo (required)"
    "* caption: Optional caption or description for the photo"
    "* order_index: Optional index to determine the order of photos (default is 0)"
    animal_id: int
    photo_url: str = Field(..., 
                           min_length=3,
                           max_length=700,
                           example="https://example.com/photos/1.jpg")
    caption: Optional[str] = Field(None, 
                           min_length=0,
                           max_length=255,
                           example="A cute dog playing in the park.")
    order_index: Optional[int] = Field(0, 
                                      ge=0, 
                                      example=1)
    
class PhotoCreate(PhotoBase):
    pass

class PhotoUpdate(BaseModel):
    "Base model for photo updates (all fields optional)"
    "Can only modify the following fields:"
    "* photo_url: URL of the photo"
    "* caption: Optional caption or description for the photo"
    "* order_index: Optional index to determine the order of photos (default is 0)"
    
    photo_url: Optional[str] = Field(None, 
                           min_length=3,
                           max_length=700,
                           example="https://example.com/photos/1.jpg")
    caption: Optional[str] = Field(None, 
                           min_length=0,
                           max_length=255,
                           example="A cute dog playing in the park.")
    order_index: Optional[int] = Field(0, 
                                      ge=0, 
                                      example=1)

class PhotoOut(BaseModel):
    "Shows photo details when retrieving animal information"
    "* id: Unique identifier for the photo"
    "* photo_url: URL of the photo"
    "* caption: Optional caption or description for the photo"
    "* order_index: Index to determine the order of photos"
    id: int
    photo_url: str = Field(..., 
                           min_length=3,
                           max_length=700,
                           example="https://example.com/photos/1.jpg")
    caption: Optional[str] = Field(None, 
                           min_length=0,
                           max_length=255,
                           example="A cute dog playing in the park.")
    order_index: int

    class Config:
        from_attributes = True