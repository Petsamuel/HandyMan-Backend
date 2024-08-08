from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    first_name:str
    last_name:str
    username: str
    email: str
    phone:str

class UserCreate(UserBase):
    user_type:Optional[str] = "user"
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class HandymanBase(UserBase):

    specialization: str
    rating: Optional[float] = None

class HandymanCreate(HandymanBase):
    user_type:Optional[str] = "handyman"
    password: str

class Handyman(HandymanBase):
    id: int

    class Config:
        from_attributes = True

class ServiceRequestBase(BaseModel):
    user_id: int
    car_make: str
    car_model: str
    car_year: str
    issue_description: str
    location: str
    status: Optional[str] = "pending"

class ServiceRequestCreate(ServiceRequestBase):
    pass

class ServiceRequest(ServiceRequestBase):
    id: int
    handyman_id: Optional[int] = None

    class Config:
        from_attributes = True

class PaymentBase(BaseModel):
    user_id: int
    service_request_id: int
    amount: float
    status: Optional[str] = "pending"

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user:Optional["User"] or None = None

# class TokenData(BaseModel):
#     user:Optional["User"] or None = None