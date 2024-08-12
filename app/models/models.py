# This project uses FastAPI 
# Author: samuel peter
# Source: https://github.com/Petsamuel/HandyMan-Backend
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()

class UserType(str, Enum):
    USER = "user"
    HANDYMAN = "handyman"

class ServiceStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    user_type = Column(String, default=UserType.USER.value)
    hashed_password = Column(String)
    
    # Relationships
    service_requests = relationship("ServiceRequest", back_populates="user")
    ratings = relationship("Rating", back_populates="user")

class Handyman(Base):
    __tablename__ = "handymen"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    hashed_password = Column(String)
    user_type = Column(String, default=UserType.HANDYMAN.value)
    specialization = Column(String)
    rating = Column(Float, default=0.0)  # Default rating can be set to 0
    
    # Relationships
    service_requests = relationship("ServiceRequest", back_populates="handyman")
    ratings = relationship("Rating", back_populates="handyman")

class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    handyman_id = Column(Integer, ForeignKey("handymen.id"), nullable=True)
    car_make = Column(String)
    car_model = Column(String)
    car_year = Column(String)
    issue_description = Column(String)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Automatically update on modification
    status = Column(String, default=ServiceStatus.PENDING.value)

    # Relationships
    user = relationship("User", back_populates="service_requests")
    handyman = relationship("Handyman", back_populates="service_requests")
    rating = relationship("Rating", back_populates="service_request", uselist=False)

class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    handyman_id = Column(Integer, ForeignKey("handymen.id"))
    service_request_id = Column(Integer, ForeignKey("service_requests.id"))
    rating = Column(Float)
    comments = Column(String)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="ratings")
    handyman = relationship("Handyman", back_populates="ratings")
    service_request = relationship("ServiceRequest", back_populates="rating")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service_request_id = Column(Integer, ForeignKey("service_requests.id"))
    amount = Column(Float)
    status = Column(String, default="pending")
    timestamp = Column(DateTime, default=func.now())  # Default to current time

    # Relationships
    user = relationship("User")
    service_request = relationship("ServiceRequest")
