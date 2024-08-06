from fastapi import FastAPI
import uvicorn
from app.routers import users



app = FastAPI()

@app.on_event("startup")
async def startup_event():
    return {"message":"started..."}
# Include routers
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Car Repair Handyman API"}




if __name__ == "__main__":
 uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
