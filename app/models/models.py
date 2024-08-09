from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name=Column(String, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone=Column(String,unique=True, index=True)
    user_type=Column(String)
    hashed_password = Column(String)
    service_requests = relationship("ServiceRequest", back_populates="user")

class Handyman(Base):
    __tablename__ = "handymen"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name=Column(String, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone=Column(String,unique=True, index=True)
    latitude=Column(Float)
    longitude=Column(Float)
    hashed_password = Column(String)
    user_type=Column(String)
    specialization = Column(String)
    rating = Column(Float)
    service_requests = relationship("ServiceRequest", back_populates="handyman")

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
    latitude=Column(Float)
    longitude=Column(Float)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    status = Column(String, default="pending")
    user = relationship("User", back_populates="service_requests")
    handyman = relationship("Handyman", back_populates="service_requests")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service_request_id = Column(Integer, ForeignKey("service_requests.id"))
    amount = Column(Float)
    status = Column(String, default="pending")
    timestamp = Column(DateTime)
    user = relationship("User")
    service_request = relationship("ServiceRequest")
