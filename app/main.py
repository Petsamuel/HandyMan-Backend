# This project uses FastAPI 
# Author: samuel peter
# Source: https://github.com/Petsamuel/HandyMan-Backend

from fastapi import FastAPI 
from models.models import Base
from contextlib import asynccontextmanager
import uvicorn
import subprocess
from database import engine, database
from routers import users, auth, handyman, service, request, payment
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):
#     # Startup: connect to the database
    
    try:
        Base.metadata.create_all(engine)   
        await database.connect()
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        
    except Exception as e:
        print(f"Error initializing database: {e}")
    
    yield
    # Shutdown: disconnect from the database
    await database.disconnect()

app = FastAPI(title="Oga-HandyMan.NG",description="handyman services made for Nigerians", version="1.0.0", contact={"name":"Peter Samuel 😎", "email":"petsamuel4@gmail.com", "linkedIn":"linkedin.com/in/bieefilled"}, lincense_info={"name":"","url":""}, lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],   
)


@app.get("/")
async def root():
   
    return {"name": "Handyman.NG", "versions":"1.0.0", "description":"api for handyman in nigeria", "contact":{"name":"peter samue","email":"petsamuel4@gmail.com"}}

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(handyman.router)
app.include_router(request.router)
app.include_router(service.router)
app.include_router(payment.router)







# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000,  reload=True)


