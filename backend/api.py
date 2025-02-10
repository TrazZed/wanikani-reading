import httpx
from fastapi import HTTPException

async def validate_api_key(apiKey: str):
    url = "https://api.wanikani.com/v2/user"
    headers = {"Authorization": f"Bearer {apiKey}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    
    if response.status_code == 200:
        return True
    return False

async def fetch_wanikani_data(apiKey: str, endpoint: str, params: dict = None):
    # Base url for Wanikani API
    baseUrl = "https://api.wanikani.com/v2"

    # Add API key to header
    headers = {"Authorization": f"Bearer {apiKey}"}

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
    
# Function to fetch assignments that have passed_at
async def fetch_assignments(apiKey: str):
    assignments = await fetch_wanikani_data(apiKey, "assignments")
    
    # Filter out assignments where passed_at is not null
    passed_assignments = [assignment['data']['subject_id'] for assignment in assignments if assignment['data'].get('passed_at')]

    return passed_assignments

# Function to fetch vocabulary related to filtered assignments
async def fetch_vocabulary_for_passed_assignments(apiKey: str):
    vocabData = await fetch_wanikani_data(apiKey, "subjects", {"types": "vocabulary"})
    passedVocab = await fetch_assignments(apiKey)

    # Filter and return only the vocabulary objects
    vocabList = [vocab for vocab in vocabData if vocab['id'] in passedVocab]
    print(len(vocabList))
    return vocabList