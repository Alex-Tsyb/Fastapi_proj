from pydantic import BaseModel, Field, EmailStr, AllowInfNan
from datetime import date
from typing import Optional
from datetime import datetime


class ContactResponse(BaseModel):
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    email: EmailStr = Field(max_length=250)
    phone: str = Field(max_length=20)
    birthday: date = Field()
    additional: str|None = Field(default=None)
    
    class Config:
        from_attributes = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    # email: str
    email: EmailStr = Field(max_length=250)
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    # email: str
    email: EmailStr = Field(max_length=250)
    created_at: datetime
    avatar: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"