# WaniKani Reader

## Description
This project is designed to help users generate reading practice paragraphs using their WaniKani vocabulary. It integrates with the WaniKani API to fetch vocabulary and generates a paragraph using a language model based on the user's learned vocabulary.

### Features:
- Validate WaniKani API keys
- Fetch user vocabulary from WaniKani
- Generate reading practice paragraphs using the fetched vocabulary
- Frontend built with React, Backend powered by FastAPI and Uvicorn

## Requirements

### Backend:
To install the requirements for the backend, you can use the following command:

```bash
pip install -r requirements.txt
```

### Frontend:
- `npm`
- `ReactJs`

To install requirements for the frontend, navigate to the frontend directory 
```bash
cd frontend
npm install
```

## Usage
### Backend Setup
Navigate to the backend directory
```bash
cd backend
```
Start up uvicorn service
```
uvicorn main:app --reload
```

### Frontend Setup
Navigate to the frontend directory
```bash
cd frontend
```
Use npm to run the page
```
npm run dev
```

### Application Usage
1. Supply your Wanikani API Key from https://www.wanikani.com/settings/personal_access_tokens
2. After validation, click on the button to generate a reading practice paragraph. This will use your vocabulary and a language model to create a text for reading practice.
