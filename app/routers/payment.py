# This project uses FastAPI 
# Author: samuel peter
# Source: https://github.com/Petsamuel/HandyMan-Backend
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import models, schemas
from database import get_db
from services import services
from routers import auth
from passlib.context import CryptContext




router = APIRouter(prefix="/payment", tags=["payment"])

@router.post("/service/{service_id}/payment")
async def process_payment(service_id: int, request: schemas.PaymentBase, current_user:models.User = Depends(auth.read_users_me), db: Session = Depends(get_db)):
    service_request = db.query(models.ServiceRequest).filter(models.ServiceRequest.id == service_id).first()
    
    if not service_request:
        raise HTTPException(status_code=404, detail="Service request not found")

    # Process payment (this is a placeholder; integrate with a payment gateway)
    # For example, you might call an external payment API here.

    service_request.payment_status = "paid"
    service_request.amount_paid = request.amount
    db.commit()
    
    
    return {
        "status": "Payment processed",
        "service_id": service_id,
        "amount": request.amount
    }
