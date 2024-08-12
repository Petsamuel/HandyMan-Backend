# This project uses FastAPI 
# Author: samuel peter
# Source: https://github.com/Petsamuel/HandyMan-Backend
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import models, schemas
from app.database import get_db
from app.routers import auth
from typing import List
import logging


router = APIRouter(prefix="/service", tags=["Service "])


@router.put("/edit/{request_id}")
async def update_service_request(request_id:int, current_user:models.User = Depends(auth.read_users_me), db:Session = Depends(get_db)):
    service_request = db.query(models.ServiceRequest).filter(models.ServiceRequest.user_id == current_user.id).first()
    
    if not service_request:
        raise HTTPException(status_code=404, detail="Service request not found")
    
    
    service_request.make = request.car_make
    return service_request

@router.delete("/delete/{request_id}")
async def delete_service_request(request_id:int, current_user:models.User = Depends(auth.read_users_me), db:Session = Depends(get_db)):
    service_request = db.query(models.ServiceRequest).filter(models.ServiceRequest.user_id == current_user.id and models.ServiceRequest.id== request_id).first()
    
    if not service_request:
        raise HTTPException(status_code=404, detail="Service request not found")
    
    db.delete(service_request)
    db.commit()
    return {"details":"Service request deleted successfully"}

@router.patch("/{request_id}/status")
async def update_service_status(request_id: int, request: schemas.UpdateServiceStatusRequest, current_user: models.User = Depends(auth.read_users_me), db: Session = Depends(get_db)):
    service_request = db.query(models.ServiceRequest).filter(models.ServiceRequest.id == request_id).first()
    
    if not service_request:
        raise HTTPException(status_code=404, detail="Service request not found")

    # Update the service status
    service_request.status = request.status
    db.commit()
    
    return {
        "status": "Service status updated",
        "service_id": service_id,
        "new_status": request.status
    }


@router.post("/{service_id}/complete")
async def complete_service(service_id: int, request: schemas.CompleteServiceRequest, db: Session = Depends(get_db)):
    service_request = db.query(models.ServiceRequest).filter(models.ServiceRequest.id == service_id).first()
    
    if not service_request:
        raise HTTPException(status_code=404, detail="Service request not found")

    # Update the service status to "completed"
    service_request.status = "completed"
    service_request.end_time = request.end_time
    service_request.final_cost = request.final_cost

    db.commit()
    
    return {
        "status": "Service completed",
        "service_id": service_id,
        "handyman_id": request.handyman_id,
        "end_time": request.end_time,
        "final_cost": request.final_cost
    }



@router.post("/{service_id}/feedback")
async def submit_feedback(service_id: int, request: schemas.Rating, db: Session = Depends(get_db)):
    service_request = db.query(models.ServiceRequest).filter(models.ServiceRequest.id == service_id).first()
    
    if not service_request:
        raise HTTPException(status_code=404, detail="Service request not found")

    # Save feedback to the database (assuming you have a Feedback model)
    feedback = models.Rating(
        service_request_id=service_id,
        user_id=request.user_id,
        rating=request.rating,
        comments=request.comments
    )
    db.add(feedback)
    db.commit()
    
    return {
        "status": "Feedback submitted",
        "service_id": service_id,
        "user_id": request.user_id,
        "rating": request.rating,
        "comments": request.comments
    }
    
