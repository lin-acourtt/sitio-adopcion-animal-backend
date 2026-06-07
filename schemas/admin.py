from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AdminBase(BaseModel):
    username: str = Field(...,
                          min_length=3, 
                          max_length=100,
                          example="myadmin")
    password: str = Field(..., 
                          min_length=6,
                          example="mypassword")

class AdminCreate(AdminBase):
    pass

class AdminLogin(AdminBase):
    pass

class AdminResponse(BaseModel):
    id: int
    username: str = Field(...,
                          min_length=3, 
                          max_length=100,
                          example="myadmin")
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str