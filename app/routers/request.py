from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import models, schemas
from database import get_db
from routers import auth
from typing import List
import logging


router = APIRouter(prefix="/request", tags=["request"])

async def notify_handyman(handyman_id, service_request_id):
    db_handyman = db.query(models.Handyman).filter(models.Handyman.id == handyman_id).first()
    
    if not db_handyman:
        raise HTTPException(s_code=404, details="Handyman not found")
    
    message = f"You have been selected for a service request ID:{service_request_id}"
    logging.info(f"notification to handyman {handyman_id}:{message}")
 

@router.post("/create", response_model=schemas.ServiceRequest)
async def create_service_request(request: schemas.ServiceRequestCreate, db: Session = Depends(get_db)):
    db_service_request = models.ServiceRequest(**request.dict())
    db.add(db_service_request)
    db.commit()
    db.refresh(db_service_request)
    return db_service_request

@router.get("/my-requests", response_model=List[schemas.ServiceRequest])
async def get_my_service_requests(current_user: models.User = Depends(auth.read_users_me), db: Session = Depends(get_db)):
    service_requests = db.query(models.ServiceRequest).filter(models.ServiceRequest.user_id == current_user.id).all()
    
    if not service_requests:
        raise HTTPException(status_code=404, detail="No service requests found")
    
    return service_requests

@router.get("/all-requests", response_model=List[schemas.ServiceRequest])
async def get_all_service_requests(current_user: models.User = Depends(auth.read_users_me), db: Session = Depends(get_db)):
    # Check if the current user is a handyman
    if current_user.user_type != "handyman":
        raise HTTPException(status_code=403, detail="Access forbidden: Only handymen can view all service requests.")
    
    service_requests = db.query(models.ServiceRequest).all()
    
    if not service_requests:
        raise HTTPException(status_code=404, detail="No service requests found")
    
    return service_requests

@router.put("/edit/{request_id}")
async def update_service_request(service_id:int, current_user:models.User = Depends(auth.read_users_me), db:Session = Depends(get_db)):
    request_id = db.query(models.ServiceRequest).filter(models.ServiceRequest.user_id == current_user.id).first()
    
    if not request_id:
        raise HTTPException(status_code=404, detail="Service request not found")
    
    
    request_id.make = request.car_make
    return request_id

@router.delete("/delete/{request_id}")
async def delete_request(request_id:int, current_user:models.User = Depends(auth.read_users_me), db:Session = Depends(get_db)):
    request_id = db.query(models.ServiceRequest).filter(models.ServiceRequest.user_id == current_user.id and models.ServiceRequest.id== request_id).first()
    
    if not request_id:
        raise HTTPException(status_code=404, detail="Service request not found")
    
    db.delete(request_id)
    db.commit()
    return {"details":"Service request deleted successfully"}



@router.post("/decline_service/{request_id}")
async def decline_request(request_id:int, current_user: models.User = Depends(auth.read_users_me), db: Session = Depends(get_db)):
    service_request = db.query(models.ServiceRequest).filter(models.ServiceRequest.user_id == current_user.id and models.ServiceRequest.id== request_id).first()
    
    if not service_request:
        raise HTTPException(status_code=404, detail="Service request not found")
    
    if service_request.status != "Accepted":
        raise HTTPException(status_code=404, detail="Only accepts request can be declined")
    
    service_request.status="Pending"
    db.commit()
    await notify_handyman(service_request.handyman_id, service_request.id)
    
    return {"status":"Service request declined", "request_id":request_id}