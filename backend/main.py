# Basic fast api

from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# ConnectionClosedError
from websockets.exceptions import ConnectionClosedError

from colorama import Fore, Back, Style
from pydantic import BaseModel
from uuid import uuid4
import json

import requests
import datetime

from pymongo import MongoClient

class Cacher:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

# Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket, uid: str, type = "client"):
        await websocket.accept()
        websocket.client_id = uid
        websocket.client_type = type
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

    async def broadcast_to_servants(self, message: str):
        for connection in self.active_connections:
            if connection.client_type == "servant":
                await connection.send_text(message)

    async def broadcast_to_clients(self, message: str):
        for connection in self.active_connections:
            if connection.client_type == "client":
                await connection.send_text(message)


manager = ConnectionManager()
cacher = Cacher()
client = MongoClient("localhost", 27017)

# Implement sessions with FastAPI

app = FastAPI()

# Allow cross origin requests
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# This enpoint is intended for the client, as in a web browser
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"{Fore.GREEN}Received data: {Fore.WHITE}{data}{Style.RESET_ALL}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except ConnectionClosedError:
        print(f"{Fore.RED}Client #{client_id} left the chat{Style.RESET_ALL}")
    finally:
        print(f"{Fore.RED}NOTE{Fore.WHITE}:     Client disconnected{Style.RESET_ALL}")

# This enpoint is intended for the servant, as in the microcontroller
@app.websocket("/ws/servant/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id, "servant")
    try:
        while True:
            data = await websocket.receive_text()
            print(f"{Fore.GREEN}Received data: {Fore.WHITE}{data}{Style.RESET_ALL}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
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

@app.get("/api/")
async def api_root():
    print(f"{Fore.GREEN}Hello from the API{Style.RESET_ALL}")
    return {"message": "API Reached. Have a cookie"}

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
    await manager.broadcast_to_clients(json.dumps(messageDict))
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

# get latest firmware version for device
@app.get("/api/v1/firmware")
async def firmware():
    version = get_firmware_version()
    # Return the latest firmware version
    return {"version": f"{version}"}

# get latest firmware version for device
async def get_firmware_version():
    # Get the latest released firmware version from the github repo
    if cacher.get("firmware_checked") is None or cacher.get("firmware_checked") < datetime.datetime.now() - datetime.timedelta(seconds=30):
        # if our cache is empty or the cache is older than 30 seconds
        url = "https://api.github.com/repos/Forsyth-Creations/IOT_Arm/releases/latest"
        response = requests.get(url)
        cacher.set("firmware", response.json()["tag_name"])
        cacher.set("firmware_checked", datetime.datetime.now())
        return response.json()["tag_name"]
    else:
        return cacher.get("firmware")

# Compare firmware version to the latest version
@app.get("/api/v1/firmware/{version}")
async def firmware(version: str):
    # Get the latest released firmware version from the github repo
    latest_version = await get_firmware_version()
    if version == latest_version:
        return {"message": f"false"}
    else:
        return {"message": f"true"}
    
# Assign a name to a specific uid and store it in the database
@app.post("/api/v1/assignName")
async def assignName(request: Request):
    # pull the uid from the request
    data = await request.json()
    print(data)
    uid = data["uid"]
    name = data["name"]

    print(f"{Fore.GREEN}Assigning name {name} to {uid}{Style.RESET_ALL}")

    # Store the name and uid in the mongodb database
    db = client["database"]
    collection = db["uidMapping"]

    # Check if the uid is already in the database
    if collection.find_one({"uid": uid}) is None:
        # Create a new entry
        collection.insert_one({"uid": uid, "name": name})
    else:
        # Update the entry
        collection.update_one({"uid": uid}, {"$set": {"name": name}})

    print(f"{Fore.GREEN}Assigned name {name} to {uid}{Style.RESET_ALL}")

# Get the name of a specific uid from the database
@app.get("/api/v1/getName/{uid}")
async def getName(uid: str):
    print(f"{Fore.GREEN}Getting name for {uid}{Style.RESET_ALL}")
    collection = client["database"]["uidMapping"]
    # Check if the uid is already in the database
    if collection.find_one({"uid": uid}) is None:
        # Create a new entry
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        # Update the entry
        return {"name": collection.find_one({"uid": uid})["name"]}
    
