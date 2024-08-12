# This project uses FastAPI 
# Author: samuel peter
# Source: https://github.com/Petsamuel/HandyMan-Backend

from fastapi import FastAPI 
from models.models import Base
from contextlib import asynccontextmanager
import uvicorn
import subprocess
# import websockets
from database import engine, database
from routers import users,auth,handyman, service, request, payment
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to the database
    
    try:
        Base.metadata.create_all(engine)   
        await database.connect()
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("running...")
        
        
        
    except Exception as e:
        print(f"Error initializing database: {e}")
    
    yield
    # Shutdown: disconnect from the database
    await database.disconnect()
    
    

app = FastAPI(lifespan=lifespan)
# app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    print("inside testing...")
    return {"message": "Welcome to the Car Repair Handyman API "}

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(handyman.router)
app.include_router(request.router)
app.include_router(service.router)
app.include_router(payment.router)



if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)
