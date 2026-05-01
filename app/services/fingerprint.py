import numpy as np
import librosa
from dejavu import Dejavu
from dejavu.fingerprint import fingerprint
from app.services.acoustid_service import identify_with_acoustid
from app.services.cache_service import (
    generate_fp_hash,
    get_cached_result,
    store_cached_result
)

# SQLite config 
config = {
    "database_type": "sqlite",
    "database": {
        "db": "dejavu.db"
    }
}

djv = Dejavu(config)

# standard response formatting
def build_response(song, artist=None, confidence=0, source="unknown", duration_ms=None):
    return {
        "song": song,
        "artist": artist,
        "confidence": confidence,
        "source": source,
        "duration_ms": duration_ms
    }


def identify_song(file_path: str):
    try:
        # load audio and standardize it
        samples, sr = librosa.load(file_path, sr=22050, mono=True)
        samples = np.array(samples, dtype=np.float32)

        duration_ms = int(len(samples) / sr * 1000)
        print("audio duration (ms):", duration_ms)

        if len(samples) == 0:
            return build_response("no match", None, 0, "none", duration_ms)

        # generate fingerprints
        samples = np.clip(samples, -1.0, 1.0)
        samples = (samples * 32767).astype(np.int16)

        hashes = []
        for channel in [samples]:
            hashes.extend(fingerprint(channel, Fs=sr))

        hashes = list(hashes)
        print("generated hashes:", len(hashes))

        # generate cache key
        fp_hash = generate_fp_hash(hashes)
        print("fingerprint hash:", fp_hash)

        # check cache
        cached = get_cached_result(fp_hash)
        if cached:
            print("cache hit!")
            return build_response(
                cached["song"],
                cached.get("artist"),
                cached.get("confidence"),
                "cache",
                duration_ms
            )

        # acoustID only fast path
        print("using AcoustID (skipping local DB)...")

        api_result = identify_with_acoustid(file_path)

        if api_result:
            print("storing in cache...")

            store_cached_result(
                fp_hash,
                api_result.get("song"),
                api_result.get("artist"),
                api_result.get("confidence")
            )

            return build_response(
                api_result.get("song"),
                api_result.get("artist"),
                api_result.get("confidence"),
                "acoustid",
                duration_ms
            )
        
        # fallback
        return build_response("no match", None, 0, "none", duration_ms)

    except Exception as e:
        return {"error": str(e)}
