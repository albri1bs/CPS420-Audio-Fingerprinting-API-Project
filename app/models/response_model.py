from pydantic import BaseModel
from typing import Optional

class SongResult(BaseModel):
    song: Optional[str]
    artist: Optional[str]
    confidence: Optional[float]
    source: Optional[str]
    duration_ms: Optional[int]

class IdentifyResponse(BaseModel):
    filename: str
    result: SongResult