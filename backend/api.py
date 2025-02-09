import httpx
from fastapi import HTTPException

async def fetch_wanikani_data(apiKey: str, endpoint: str, params: dict = None):
    # Base url for Wanikani API
    baseUrl = "https://api.wanikani.com/v2"

    # Add API key to header
    headers = {
        "Authorization": f"Bearer {apiKey}"
    }

    # If no parameters, use an empty dict
    if params is None:
        params = {}

    allData = []

    # Make initial GET request to WaniKani API
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{baseUrl}/{endpoint}", headers=headers, params=params)

        # Check for successful request
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Error fetching data: {response.text}")
        
        data = response.json()
        allData.extend(data['data'])

        # Check for next page and continue fetching if it exists
        while data['pages']['next_url']:
            # Update params with the next URL for the next page of data
            nextUrl = data['pages']['next_url']
            response = await client.get(nextUrl, headers=headers)

            # Check for successful request
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=f"Error fetching data: {response.text}")

            data = response.json()
            allData.extend(data['data'])

        return allData
