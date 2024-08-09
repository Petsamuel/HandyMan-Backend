from pydantic import BaseModel, EmailStr, constr, validator, Field
from typing import Optional, List
from enum import Enum

class UserType(str, Enum):
    USER = "user"
    HANDYMAN = "handyman"

class ServiceStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr  
    phone: constr(min_length=10, max_length=15) = Field(..., pattern=r'^\+?\d{10,15}$')

class UserCreate(UserBase):
    user_type: Optional[UserType] = UserType.USER
    password: str

class User(UserBase):
    id: int

    class Config:
        form_attributes = True  # Use form_attributes for SQLAlchemy integration

class HandymanBase(UserBase):
    latitude: Optional[float] = None  # Use float for latitude/longitude
    longitude: Optional[float] = None
    specialization: str
    rating: Optional[float] = None

class HandymanCreate(HandymanBase):
    user_type: Optional[UserType] = UserType.HANDYMAN
    password: str

class Handyman(HandymanBase):
    id: int

    class Config:
        form_attributes = True
        
class UpdateServiceStatusRequest(BaseModel):
    status: str
class ServiceRequestBase(BaseModel):
    user_id: int
    car_make: str
    car_model: str
    car_year: str
    issue_description: str
    location: str
    latitude: float
    longitude: float
    status: Optional[ServiceStatus] = ServiceStatus.PENDING

class ServiceRequestCreate(ServiceRequestBase):
    pass

class ServiceRequest(ServiceRequestBase):
    id: int
    handyman_id: Optional[int] = None

    class Config:
        form_attributes = True

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
        form_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: Optional[User]  # Ensure User is defined before this line
    user_type: Optional[UserType]

    class Config:
        form_attributes = True

class Rating(BaseModel):
    user_id: str
    rating: int
    comments: str
    service_id: int

class CompleteServiceRequest(BaseModel):
    handyman_id: str
    end_time: str
    final_cost: float