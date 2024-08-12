# This project uses FastAPI 
# Author: samuel peter
# Source: https://github.com/Petsamuel/HandyMan-Backend
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import models, schemas


router = APIRouter()

@router.post("/api/match_handymen", response_model=List[HandymanOut])
async def match_handymen(request: ServiceRequestCreate, db: Session = Depends(get_db)):
    # Find nearby handymen based on the user's location and service request details
    nearby_handymen = db.query(Handyman).filter(
        # Assuming you have a distance calculation function
        calculate_distance(Handyman.latitude, Handyman.longitude, request.latitude, request.longitude) < SOME_RADIUS
    ).order_by(Handyman.rating.desc()).all()

    if not nearby_handymen:
        raise HTTPException(status_code=404, detail="No available handymen found")

    return nearby_handymen
