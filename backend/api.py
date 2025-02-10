import httpx
from fastapi import HTTPException

"""
validate_api_key()
---------------------
Validates the api key given in the parameters to be valid

str apiKey: the api key to check validity of

Returns: True if valid, False else
"""
async def validate_api_key(apiKey: str):
    url = "https://api.wanikani.com/v2/user"
    headers = {"Authorization": f"Bearer {apiKey}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    
    if response.status_code == 200:
        return True
    return False

"""
fetch_wanikani_data()
-----------------------
Retrieves all data from wanikani from a given endpoint with parameters

str apiKey: the api key to access the data from
str endpoint: the endpoint to reach
dict params: the parameters to supply the request with

Returns: the data from the request an an array
"""
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


"""
fetch_assignments()
---------------------
Fetches the data from the assignments endpoint from the Wanikani API, and filters all vocabulary the user has passed

str apiKey: the api key to access the data from

Returns: An array of all passed vocabularies id's
"""
async def fetch_assignments(apiKey: str):
    assignments = await fetch_wanikani_data(apiKey, "assignments")
    
    # Filter out assignments where passed_at is not null
    passed_assignments = [assignment['data']['subject_id'] for assignment in assignments if assignment['data'].get('passed_at')]

    return passed_assignments

"""
fetch_vocabulary_for_passed_assignments()
--------------------------------------------
Filters through all of the vocab available on Wanikani and returns the vocab that the user has passed

str apiKey: the api key to access the data from

Returns: An array of vocab data that the user has passed
"""
async def fetch_vocabulary_for_passed_assignments(apiKey: str):
    vocabData = await fetch_wanikani_data(apiKey, "subjects", {"types": "vocabulary"})
    passedVocab = await fetch_assignments(apiKey)

    # Filter and return only the vocabulary objects
    vocabList = [vocab for vocab in vocabData if vocab['id'] in passedVocab]
    print(len(vocabList))
    return vocabList