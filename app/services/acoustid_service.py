import acoustid
from app.config.config import ACOUSTID_API_KEY

# uses acoustID api to identify a song 
# generates audio fingerprint using fpcalc (handled internally with acoustID library)
def identify_with_acoustid(file_path):
    try:
        results = list(acoustid.match(
            ACOUSTID_API_KEY,
            file_path,
            meta='recordings'
        ))

        print("RAW ACOUSTID RESULTS:", results) # debug

        # no results handler
        if not results:
            return None

        # highest confidence match
        best = results[0]

        return {
            "song": best[2], # title
            "artist": best[3], # artist name
            "confidence": best[0] # match confidence (scale 0-1)
        }

    # if the key is invalid
    # network errors
    # fingerprint issues with fpcalc
    except Exception as e:
        print("AcoustID error:", e)
        return None