# Basic fast api

from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

# ConnectionClosedError
from websockets.exceptions import ConnectionClosedError

from colorama import Fore, Back, Style
from pydantic import BaseModel
from uuid import uuid4
import json

# Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket, uid: str):
        await websocket.accept()
        websocket.client_id = uid
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    def get_websocket(self, uid: str):
        # Note: the uid should equal the client id
        for connection in self.active_connections:
            if connection.client_id == uid:
                return connection
            
    # Wait for a socket response with a message
    async def receive(self, websocket: WebSocket):
        message = await websocket.receive_text()
        return message


manager = ConnectionManager()

# Implement sessions with FastAPI

app = FastAPI()

# Create a class to define the data model
class BasicPing(BaseModel):
    greeting: str

# Allow cross origin requests
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- Deal with anyone that connects to the websocket ------------
# https://fastapi.tiangolo.com/advanced/websockets/

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"{Fore.GREEN}Received data: {Fore.WHITE}{data}{Style.RESET_ALL}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast(f"Client #{client_id} left the chat")
    except ConnectionClosedError:
        print(f"{Fore.RED}Client #{client_id} left the chat{Style.RESET_ALL}")
    finally:
        print(f"{Fore.RED}NOTE{Fore.WHITE}:     Client disconnected{Style.RESET_ALL}")


async def broadcast_message(message: str):
    # Use the manager to broadcast the message
    try:
        await manager.broadcast(message)
    except ConnectionClosedError:
        # Cannot broadcast to a closed connection
        print(f"{Fore.RED}Cannot broadcast to a closed connection{Style.RESET_ALL}")

async def send_personal_message(message: str, uid : str):
    # Use the manager to send a personal message
    # Get the websocket from the uid
    websocket = manager.get_websocket(uid)
    try:
        await manager.send_personal_message(message, websocket)
    except ConnectionClosedError:
        # Cannot send to a closed connection
        print(f"{Fore.RED}Cannot send to a closed connection{Style.RESET_ALL}")

# -----------------------------------------------------------------------

@app.get("/")
async def api_root():
    print(f"{Fore.GREEN}Hello from the API{Style.RESET_ALL}")
    return {"message": "API Reached"}

@app.get("/api/v1/hello")
async def api_hello():
    print(f"{Fore.GREEN}Hello from the API{Style.RESET_ALL}")
    return {"message": "Hello from the API"}

@app.post("/api/v1/hello")
async def api_hello(greeting: BasicPing):
    # Print the greeting to the console
    print(f"{Fore.GREEN}{greeting}{Style.RESET_ALL}")
    # Return the greeting to the client
    return {"greeting": "Hey gorgeous!"}

@app.get("/api/v1/uid")
async def api_uuid():
    uid = uuid4()
    print(f"{Fore.GREEN}UUID Generated: {uid}{Style.RESET_ALL}")
    return {"uid": uid}

@app.post("/api/v1/heartbeat/{uid}")
async def heartbeat(uid, request: Request):
    # Emit a message on the websocket
    # get data from the request
    data = await request.json()

    messageDict = \
            {"type": "heartbeat",
            "uid" : uid, 
            "status": "alive",
            "data": data,}
    await broadcast_message(json.dumps(messageDict))
    return {"message": f"Heartbeat accepted"}

# Toggle LED
@app.post("/api/v1/toggleLED")
async def toggleLED(request: Request):
    # pull the uid from the request
    data = await request.json()
    uid = data["uid"]
    # Emit a message on the websocket
    messageDict = \
            {"type" : "toggleLED",
            "uid" : uid}
    await send_personal_message(json.dumps(messageDict), uid)
    return {"message": f"Toggle LED for {uid}"}

# restarting 
@app.post("/api/v1/restart")
async def restart(request: Request):
    # pull the uid from the request
    data = await request.json()
    uid = data["uid"]
    # Emit a message on the websocket
    messageDict = \
            {"type" : "restart",
            "uid" : uid}
    await send_personal_message(json.dumps(messageDict), uid)
    return {"message": f"Restarting {uid}"}

# get health data
@app.post("/api/v1/health")
async def health(request: Request):
    # pull the uid from the request
    data = await request.json()
    uid = data["uid"]
    # Emit a message on the websocket
    messageDict = \
            {"type" : "health",
            "uid" : uid}
    await send_personal_message(json.dumps(messageDict), uid)
    return {"message": f"Health data for {uid}"}