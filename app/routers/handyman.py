from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import models, schemas
from database import get_db
from services import services

router = APIRouter(prefix="/handymen", tags=["handymen"])

@router.post("/", response_model=schemas.Handyman)
async def create_handyman(handyman: schemas.HandymanCreate, db: Session = Depends(get_db)):
    db_handyman = models.Handyman(**handyman.dict())
    db.add(db_handyman)
    db.commit()
    db.refresh(db_handyman)
    return db_handyman

@router.get("/{handyman_id}", response_model=schemas.Handyman)
async def read_handyman(handyman_id: int, db: Session = Depends(get_db)):
    db_handyman = db.query(models.Handyman).filter(models.Handyman.id == handyman_id).first()
    if db_handyman is None:
        raise HTTPException(status_code=404, detail="Handyman not found")
    return db_handyman


@router.get("/nearby_handymen/", response_model=schemas.Handyman)
def get_nearby_handymen(request_id: int, db: Session = Depends(get_db)):
    request = db.query(models.ServiceRequest).filter(models.ServiceRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    nearby_handymen = services.find_nearby_handymen(request, db)
    return nearby_handymen
