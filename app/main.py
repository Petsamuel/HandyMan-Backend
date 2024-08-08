from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
import subprocess
from database import engine, database
from routers import users,auth,handyman
from models.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to the database
    
    try:
        Base.metadata.create_all(engine)   
        await database.connect()
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        
    except Exception as e:
        print(f"Error initializing database: {e}")
    
    yield
    # Shutdown: disconnect from the database
    await database.disconnect()
    
    

app = FastAPI(lifespan=lifespan)
@app.get("/")
async def root():
    return {"message": "Welcome to the Car Repair Handyman API "}

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(handyman.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)
