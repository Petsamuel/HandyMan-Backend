# This project uses FastAPI 
# Author: samuel peter
# Source: https://github.com/Petsamuel/HandyMan-Backend
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import models, schemas
from app.database import get_db
from app.services import services
from passlib.context import CryptContext
from typing import List
import logging
import bcrypt
from geopy.distance import geodesic

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/handymen", tags=["Handymen"])


def match_handymen(request: schemas.ServiceRequestCreate, db: Session = Depends(get_db)):
    # Find nearby handymen based on the user's location and service request details
    nearby_handymen = db.query(Handyman).filter(
        # Assuming you have a distance calculation function
        calculate_distance(Handyman.latitude, Handyman.longitude, request.latitude, request.longitude) < SOME_RADIUS
    ).order_by(Handyman.rating.desc()).all()

    if not nearby_handymen:
        raise HTTPException(status_code=404, detail="No available handymen found")

    return nearby_handymen

def find_nearby_handymen(request: models.ServiceRequest, db: Session, radius: float = 10.0):
    # Fetch all active handymen from the database
    # handymen = db.query(Handyman).filter(Handyman.is_active == True).all()
    handymen = db.query(models.Handyman).all()
    nearby_handymen = []
    
    # Loop through all handymen and calculate the distance from the user's location
    for handyman in handymen:
        distance = geodesic((request.latitude, request.longitude), (handyman.latitude, handyman.longitude)).km
        if distance <= radius:
            nearby_handymen.append(handyman)
            
    # nearby_handymen.sort(key=lambda x: (x["distance"], -x["rating"]))
    return 


async def notify_handyman(handyman_id, service_request_id):
    db_handyman = db.query(models.Handyman).filter(models.Handyman.id == handyman_id).first()
    
    
    if not db_handyman:
        raise HTTPException(s_code=404, details="Handyman not found")
    
    message = f"You have been selected for a service request ID:{service_request_id}"
    logging.info(f"notification to handyman {handyman_id}:{message}")

@router.post("/", response_model=schemas.Handyman)
async def create_handyman(handyman: schemas.HandymanCreate, db: Session = Depends(get_db)):
    db_handyman = models.Handyman(username=handyman.username, email=handyman.email, first_name=handyman.first_name, last_name=handyman.last_name, phone=handyman.phone, hashed_password = pwd_context.hash(handyman.password),specialization=handyman.specialization, rating=handyman.rating)
    db.add(db_handyman)
    db.commit()
    db.refresh(db_handyman)
    return db_handyman

@router.get("/{handyman_id}", response_model=schemas.Handyman)
async def get_handyman_by_id(handyman_id: int, db: Session = Depends(get_db)):
    db_handyman = db.query(models.Handyman).filter(models.Handyman.id == handyman_id).first()
    if db_handyman is None:
        raise HTTPException(status_code=404, detail="Handyman not found")
    return db_handyman


@router.get("/nearby_handymen/", response_model=List[schemas.Handyman])
async def get_nearby_handymen(request_id: int, db: Session = Depends(get_db)):
    # Step 1: Retrieve the service request
    request = db.query(models.ServiceRequest).filter(models.ServiceRequest.id == request_id).first()
    
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    # Step 2: Find nearby handymen
    nearby_handymen = find_nearby_handymen(request, db)
    
    if not nearby_handymen:
        raise HTTPException(status_code=404, detail="No nearby handymen found")
    
    # Step 3: Match handymen (optional, depending on how you handle selection)
    matched_handymen = match_handymen(nearby_handymen, request)
    
    return matched_handymen  # or return nearby_handymen if no matching is required


@router.post("/select_handyman/{handyman_id}")
async def select_handyman(handyman_id: int, request_id: int, db: Session = Depends(get_db)):
    handyman = db.query(models.Handyman).filter(models.Handyman.id == handyman_id).first()
    if not handyman:
        raise HTTPException(status_code=404, detail="Handyman not found")

    service_request = db.query(models.ServiceRequest).filter(models.ServiceRequest.id == request_id).first()
    if not service_request:
        raise HTTPException(status_code=404, detail="Service request not found")

    if service_request.status != "Pending":
        raise HTTPException(status_code=404, detail="Only Pending requests can be Acepted")
    
    # Update the service request with the selected handyman
    service_request.handyman_id = handyman_id
    service_request.status = "Accepted"
    db.commit()

    # Notify the handyman (this could be through WebSocket, push notifications, etc.)
    notify_handyman(handyman_id, service_request.id)

    return {"status": "Handyman selected", "handyman_id": handyman_id}

