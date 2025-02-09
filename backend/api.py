import httpx
from fastapi import HTTPException

async def fetch_wanikani_data(apiKey: str, endpoint: str, params: dict = None):
    # Base url for Wanikani API
    baseUrl = "https://api.wanikani.com/v2"

    #Add API key to header
    headers = {
        "Authorization": f"Bearer {apiKey}"
    }

    #If no parameters, use empty dict
    if params is None:
        params = {}
    
    # Make get request to Wanikani API
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{baseUrl}/{endpoint}", headers=headers, params=params)

        # Check for successful request
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Error fetching data: {response.text}")
        
        return response.json()
