from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api import *

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define a request body to accept the API key
class APIKeyRequest(BaseModel):
    api_key: str

"""
validate_key()
----------------
Validates the given api key

APIKeyRequest request: The data for the request requiring the field api_key

Returns: {"valid": True/False} if the api key is valid or not respectively
"""
@app.post("/validate_key")
async def validate_key(request: APIKeyRequest):
    isValid = await validate_api_key(request.api_key)
    return {"valid": isValid}


"""
fetch_vocabulary()
-------------------
Retrieves the vocabulary that the user has passed

APIKeyRequest request: the data for the request requiring the field api_key

Returns: An array of vocabulary data that the user has passed
"""
@app.post("/fetch_vocabulary")
async def fetch_vocabulary(request: APIKeyRequest):
    try:
        vocab_list = await fetch_vocabulary_for_passed_assignments(request.api_key)
        return vocab_list
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=f"Could not fetch vocabulary data: {e.detail}")
