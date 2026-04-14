from fastapi import FastAPI, UploadFile, File
import shutil
import os
from app.services.fingerprint import identify_song

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"message": "API running"}


@app.post("/identify")
async def identify(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = identify_song(file_path)

    return {
        "filename": file.filename,
        "result": result
    }