from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json

app = FastAPI()

# Dictionary to store connected clients
active_connections: Dict[str, WebSocket] = {}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    active_connections[user_id] = websocket  # Store the connection

    try:
        await websocket.send_text("WebSocket connected")

        while True:
            # Receive location data from the handyman
            location_data = await websocket.receive_text()
            # Broadcast the location data to other clients
            await broadcast_location(user_id, location_data)

    except WebSocketDisconnect:
        print(f"Client {user_id} disconnected")
        del active_connections[user_id]  # Remove the connection

async def broadcast_location(sender_id: str, location_data: str):
    # Send the location data to all connected clients except the sender
    message = f"Handyman {sender_id} location: {location_data}"
    for user_id, connection in active_connections.items():
        if user_id != sender_id:
            await connection.send_text(message)

# Optional: Add a method to get active connections (for debugging or management)
def get_active_connections() -> List[str]:
    return list(active_connections.keys())