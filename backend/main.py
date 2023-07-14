# Basic fast api

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from colorama import Fore, Back, Style
from pydantic import BaseModel
from uuid import uuid4

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