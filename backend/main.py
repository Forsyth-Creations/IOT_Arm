# Basic fast api

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import websockets
import asyncio

from colorama import Fore, Back, Style
from pydantic import BaseModel
from uuid import uuid4
import json

# Implement sessions with FastAPI

app = FastAPI()

# websocket clients

websocket_clients = []

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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.append(websocket)
    try:
        while True:
            _ = await websocket.receive_text()
            print(f"{Fore.GREEN}Message received: {_}{Style.RESET_ALL}")
    finally:
        websocket_clients.remove(websocket)

async def emit_message(message: str):
    if len(websocket_clients) > 0:
        for client in websocket_clients:
            await client.send_text(message)

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
async def heartbeat(uid):
    # Emit a message on the websocket
    messageDict = \
          {"uid" : uid, 
           "status": "alive",
           "type": "heartbeat"}
    await emit_message(json.dumps(messageDict))
    return {"message": f"Message emitted for {uid}"}

