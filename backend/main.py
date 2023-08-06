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
import time    

from pymongo import MongoClient

from dbHelper import dbHelper

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

# This endpoint is intended for the client, as in a web browser
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

@app.get("/")
async def api_root():
    print(f"{Fore.GREEN}Hello from the API{Style.RESET_ALL}")
    return {"message": "API Reached"}

@app.get("/api/v1/hello")
async def api_hello():
    print(f"{Fore.GREEN}Hello from the API{Style.RESET_ALL}")
    return {"message": "Hello from the API"}

@app.post("/api/v1/register_device")
async def api_register_device(request: Request):
    try:
        # Pull the uid from the request, which is stored in the body
        data = await request.json()
        # Try to add it to the mongo database
        uid = data["uid"]
        client.database.Devices.insert_one({"uid": uid})
        print(f"{Fore.GREEN}Device registered: {uid}{Style.RESET_ALL}")
        return {"message": "Device registered"}
    except Exception as e:
        print(f"{Fore.RED}Device registration failed{Style.RESET_ALL}")
        return {"message": "Device registration failed", "reason" : str(e)}

@app.get("/api/v1/uid")
async def api_uuid():
    uid = uuid4()
    print(f"{Fore.GREEN}UUID Generated: {uid}{Style.RESET_ALL}")
    # Add the uid to the database
    return {"uid": uid}

# uid and auto-register the device in the database
@app.post("/api/v1/uid/register")
async def api_uuid_register():
    try:
        # Check to see if the uid is already in the database
        # If it is, generate a new one and try again
        # If it isn't, add it to the database
        # try 10 times, then give up and throw an error
        for i in range(10):
            uid = str(uuid4())
            if client.database.Devices.find_one({"uid": uid}):
                print(f"{Fore.YELLOW}UID {uid} already exists. Attempting to generate a new one{Style.RESET_ALL}")
                uid = str(uuid4())
            else:
                break
            uid = None
        
        if uid is None:
            raise Exception("Failed to generate a unique uid")

        print(f"{Fore.GREEN}UUID Generated: {uid}{Style.RESET_ALL}")
        # Add the uid to the database
        client.database.Devices.insert_one({"uid": uid})
        return {"uid": uid}
    except Exception as e:
        return {"message": "Device registration/uid generation failed", "reason" : str(e)}

@app.post("/api/v1/heartbeat/{uid}")
async def heartbeat(uid, request: Request):
    # Emit a message on the websocket
    # get data from the request
    try:
        data = await request.json()

        messageDict = \
                {"type": "heartbeat",
                "uid" : uid, 
                "status": "alive",
                "data": data,}
        await manager.broadcast_to_clients(json.dumps(messageDict))

        epoch_time = int(time.time())

        # Store the data in the database by updating an entry
        client.database.Devices.update_one({"uid": uid}, {"$set": {"last_heartbeat": epoch_time}})
        client.database.Devices.update_one({"uid": uid}, {"$set": {"data": data}})

        return {"message": f"Heartbeat accepted"}
    except Exception as e:
        print(f"{Fore.RED}Heartbeat failed for {uid}{Style.RESET_ALL}")
        return {"message": f"Heartbeat failed", "reason" : str(e)}

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
    try:
        # Pull the uid and name from the request
        data = await request.json()
        uid = data["uid"]
        name = data["name"]
        # Add the uid and name to the database. updating the Device collection
        client.database.Devices.update_one({"uid": uid}, {"$set": {"name": name}})
        print(f"{Fore.GREEN}Assigned name to uid{Style.RESET_ALL}")
        return {"message": f"'{name}' was assigned to {uid}"}
    except Exception as e:
        print(f"{Fore.RED}Failed to assign name to uid{Style.RESET_ALL}")
        return {"message": f"Failed to assign name to uid", "reason" : str(e)}

# Get the name of a specific uid from the database
@app.get("/api/v1/getName/{uid}")
async def getName(uid: str):
    # Get the name of the uid from the database
    name = client.database.Devices.find_one({"uid": uid})["name"]
    print(f"{Fore.GREEN}Got name of uid{Style.RESET_ALL}")
    return {"name": f"{name}"}

# Login
@app.post("/api/v1/login")
async def login(request: Request):
    print(f"{Fore.GREEN}Login request received{Style.RESET_ALL}")
    # Pull the username and password from the request
    data = await request.json()
    email = data["email"]
    password = data["password"]

    # Check if the email and password are in the database and correct
    # All users are stored in the database in the Users collection

    foundDatabase = client.database.Users.find_one({"email": email, "password": password})

    if foundDatabase is None:
        print(f"{Fore.RED}email or password incorrect for : {email}{Style.RESET_ALL}")
        raise HTTPException(status_code=500, detail="email or password incorrect")
    else:
        # Create a new session
        token = str(uuid4())
        # Store the session in the database
        epoch_time = int(time.time())
        print("Registering session")
        client.database.sessions.insert_one({"token": token, "email": email, "epoch_time": epoch_time})
        print(f"{Fore.GREEN}Login successful{Style.RESET_ALL}")
        return {"message": "Login successful", "token": token}

# Create new account 
@app.post("/api/v1/create_account")
async def createAccount(request: Request):
    # Pull the username and password from the request
    print(f"{Fore.GREEN}Create account request received{Style.RESET_ALL}")
    data = await request.json()
    data = data['data']
    print(f"{Fore.YELLOW}{data}{Style.RESET_ALL}")
    email = data["email"]

    # Check if the email is already taken
    # All users are stored in the database in the Users collection

    found_name = client.database.Users.find_one({"email": email})

    if found_name is None:
        # Create a new session
        session_id = str(uuid4())
        # Store the session in the database
        epoch_time = int(time.time())
        client.database.sessions.insert_one({"session_id": session_id, "email": email, "epoch_time": epoch_time})
        # Store the data in the database by creating a new entry

        db = client["database"]
        collection = db["Users"]

        collection.insert_one(data)

        print(f"{Fore.GREEN}Created account{Style.RESET_ALL}")
        return {"message": "Account created", "session_id": session_id}
    else:
        print(f"{Fore.RED}email already taken{Style.RESET_ALL}")
        raise HTTPException(status_code=500, detail="Username already taken")
    
@app.get("/api/v1/device/{uid}")
async def get_device(uid: str):
    # Get the device from the database
    print(f"Attempting to find device with uid: {uid} ")
    device = client.database.Devices.find_one({"uid": uid})
    if device is None:
        print(f"{Fore.RED}Device not found{Style.RESET_ALL}")
        raise HTTPException(status_code=500, detail="Device not found")
    # remove the _id field
    device.pop("_id")
    return device

@app.post("/api/v1/registerDevice")
async def register_device(request: Request):
    # Get the device from the database
    
    requestJson = await request.json()
    uid = requestJson["uid"]
    token = requestJson["token"]

    device = client.database.Devices.find_one({"uid": uid})
    if device is None:
        print(f"{Fore.RED}Device not found{Style.RESET_ALL}")
        raise HTTPException(status_code=500, detail="Device not found")


    # Get the email from the request
    outputData = client.database.sessions.find_one({"token": token})

    # Add the device to the collection called AccountToDevices
    # This collection is used to map devices to accounts
    # check to make sure the device isn't already registered

    if (client.database.AccountToDevices.find_one({"uid": uid})):
        print(f"{Fore.RED}Device already registered{Style.RESET_ALL}")
        raise HTTPException(status_code=500, detail="Device already registered")

    db = client["database"]
    collection = db["AccountToDevices"]
    collection.insert_one({"email": outputData["email"], "uid": uid})

    device.pop("_id")
    
    return device


@app.post("/api/v1/devices/")
async def get_devices(request: Request):
    # Requires a token
    # Get a list of uid from the database that are associated with the devices

    # Get the email from the request
    requestedJson = await request.json()
    token = requestedJson["token"]
    outputData = client.database.sessions.find_one({"token": token})

    email = outputData["email"]

    # Find all database entries in AccountToDevices collection that have the email in them

    data = client.database.AccountToDevices.find({"email": email})

    # Create a list of uids
    uids = []
    for entry in data:
        uids.append(entry["uid"])

    print(f"{Fore.GREEN}Devices found{Style.RESET_ALL}")
    print(uids)
    return {"devices": uids}
    