from fastapi import APIRouter, UploadFile, File
import shutil
import subprocess

from app.models.response_model import IdentifyResponse, SongResult
from app.services.fingerprint import identify_song

router = APIRouter()

# helper function to try and improve recording identify properly
def convert_to_wav(input_path: str) -> str:
    output_path = input_path + ".wav"

    subprocess.run([
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-ac", "1",
        "-ar", "44100",
        "-af", "silenceremove=1:0:-50dB,loudnorm,highpass=f=200,lowpass=f=3000",
        output_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return output_path

# main route 
@router.post("/identify", response_model=IdentifyResponse)
async def identify(file: UploadFile = File(...)):
    try:
        temp_path = f"temp_{file.filename}"

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("Saved file:", temp_path)

        if file.filename.endswith(".webm"):
            print("Converting webm → wav...")
            temp_path = convert_to_wav(temp_path)

        result = identify_song(temp_path)

        return IdentifyResponse(
            filename=file.filename,
            result=SongResult(**result)
        )

    except Exception as e:
        return {"error": str(e)}