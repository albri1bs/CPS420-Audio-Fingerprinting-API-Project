# Audio Fingerprinting & Song Identification API

## Overview
The project is a full-stack audio fingerprinting system that identifies songs from short audio clips. Users can either upload audio files or record snippets directly through the browser. The system processes the audio, generates a fingerprint, and matches it against a global database using the AcoustID API/Database.

## Purpose
The purpose of this system is to demonstrate how audio fingerprinting works in practice, including preprocessing, fingerprint generation, external API intergration, and performance optimization through caching.

## Target Users
- Students learning about audio processing and APIs
- Developers interested in building media recognition systems
- Anyone who wants to identify songs from short audio clips

## Key Features
- Upload audio files (MP3, WAV, etc.)
- Record audio (~10-15 seconds) via browser microphone
- Automatic audio preprocessing (normalization, silence removal)
- Song identification using AcoustID (Chromaprint, fpcalc)
- SQLite-based cashing for fast repeated lookups
- Streuctured API responses using FastAPI + Pydantic
- Interactive frontend built with Vite + TypeScript

## System Architecture/Hig-Level Flow
- Frontend (Vite + TS)
- FastAPI Router (views.py)
- Audio Processing (FFmpeg)
- Service Layer (fingerprint.py)
- Cache (SQLite)
- AcoustID API (Chromaprint / fpcalc)
- Response Model (Pydantic)
- Frontend Display

## Architecture Explanation
- Frontend: Handles user interaction (upload/record)
- Router Layer: Accepts requests and prepares audio
- Service Layer: Preprocesses audio and performs identification
- Cache Layer: Avoids repeated API calls
- External API: Matches audio fingerprints globally
- Model Layer: Ensures consistent response structure

## API Documentation

### 'POST /identify'

Identifies a song from an uploaded or recorded audio file.

---

### Request

### Form Data



## Data Flow + Business Logic

1. User uploads or records audio
2. File is sent to /identify endpoint
3. Audio is saved and converted (if needed)
4. Audio is processed and fingerprinted
5. Fingerprint hash is generated
6. Cache is checked for an existing result
  - If found: return cached result
  - If not: call AcoustID API
7. API result is stored in cache
8. Response is formatted using Pydantic models
9. Result is returned to frontend



## Setup Instructions

# Backend Setup

git clone https://github.com/albri1bs/CPS420-Audio-Fingerprinting-API-Project.git
cd CPS420-AudioFingerprint
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Environment Variables 

Create a .env file in the root directory:


Navigate to https://acoustid.org/ and register your application to get an API key. You must not deploy for financial gain, the AcoustID API is an open-source, free software.
ACOUSTID_API_KEY=your_api_key_here
DB_PATCH=dejavu.db

# Run Backend
uvicorn app.main:app --reload

# Frontend Setup 
cd frontend
npm install
npm run dev

Open in browser:
hhtp://localhost:5173

# Deployment Notes
- Backend can be deployed using:
    - Render
    - Railway
    - Docker
- Frontend can be deployed using:
    - Vervel
    - Netlify
- Environment variables must be configured in production


## Logging & Error Handling

Logging
    - Audio processing steps
    - Fingerprint generation
    - Cache hits and misses
    - API responses
Error Handling
    - Try/catch blocks across services 
    - Safe fallback responses:
    {
       "song": "no match",
       "confidence": 0
    }


## Maintenance Considerations
- Cache may grow over time (future improvement: expiration)
- Audio preprocessing can be tuned further for accuracy (especially for recording)

## Future Improvements
- Return multiple match results
- Improve frontend UI/UX
- Deploy publicly
- Optimize performance further


## Author
Bret Albright
Central Michigan University
CPS420 - Audio Fingerprinting Project
