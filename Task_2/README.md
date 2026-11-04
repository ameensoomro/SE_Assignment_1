# Task 2: API Key Generation and Sharing

## Overview
A Flask API that processes text using API key authentication. Three unique API keys are generated for three different consumers.

## Technologies Used
- Python
- Flask
- JSON
- cURL / PowerShell

## API Endpoint

| Method | Endpoint | Description |
|---|---|---|
| POST | `/process` | Processes text after API key validation |

## Authentication
The API key must be provided through the `X-API-Key` request header.

Three unique API keys are generated for:
- Consumer 1
- Consumer 2
- Consumer 3

API keys are stored locally in `api_keys.json` and are excluded from the public repository.

## Text Processing
The API accepts JSON input containing text and converts it to uppercase.

## How to Run

Generate API keys:

```bash
python Task_2/keys.py
```

Start Flask server:

```bash
python Task_2/app.py
```

Server runs at:

`http://127.0.0.1:5001`

## Testing
- All three valid API keys were tested successfully.
- Invalid API key was rejected.
- Missing or invalid authentication returns an error.
- Valid text is converted to uppercase.

## Security
API keys are stored locally and are not committed to the public GitHub repository.