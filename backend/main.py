from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api import *

app = FastAPI()

# curl -X 'POST'   'http://127.0.0.1:8000/validate_key'   -H 'Content-Type: application/json'   -d '{"api_key": "<YOUR-API-KEY>"}'

# Define a request body to accept the API key
class APIKeyRequest(BaseModel):
    api_key: str

@app.post("/validate_key")
async def validate_key(request: APIKeyRequest):
    isValid = await validate_api_key(request.api_key)
    return {"valid": isValid}


# curl -X 'POST'   'http://127.0.0.1:8000/fetch_vocabulary'   -H 'Content-Type: application/json'   -d '{"api_key": "<YOUR-API-KEY>"}'

@app.post("/fetch_vocabulary")
async def fetch_vocabulary(request: APIKeyRequest):
    # Call the utility function to fetch data from WaniKani API
    try:
        data = await fetch_wanikani_data(request.api_key, "subjects", {"types": "vocabulary"})
        return data  # Return the fetched vocabulary data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=f"Could not fetch vocabulary data: {e.detail}")