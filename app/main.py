from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from models.models import Base
from contextlib import asynccontextmanager
import uvicorn
import subprocess
import websockets
from database import engine, database
from routers import users,auth,handyman, serviceRequest
from fastapi.responses import HTMLResponse



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



@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    await websocket.send_text("WebSocket connected")
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast location data to other users
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print(f"Client {user_id} disconnected")


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(handyman.router)
app.include_router(serviceRequest.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5000, reload=True)
