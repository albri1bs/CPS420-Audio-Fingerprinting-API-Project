import hashlib
import sqlite3
import os
from app.config.config import DB_PATH


def generate_fp_hash(hashes):
    # create a stable fingerprint key 
    try:
        # limit hashes for conistency and performance
        subset = hashes[:100]
        # every hash follows (hash_value, offset)
        hash_strings = [str(h[0]) for h in subset] # only need hash_value
        combined = "".join(hash_strings)
        return hashlib.sha1(combined.encode()).hexdigest()
    except Exception as e:
        print("Hash generation error:", e)
        return None

def get_cached_result(fp_hash):
    try:
        # connect db
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # query cache table
        cursor.execute(
            "SELECT song, artist, confidence FROM acoustid_cache WHERE fingerprint_hash = ?",
            (fp_hash,)
        )

        row = cursor.fetchone()
        conn.close()
        # if match not found just return formatted result
        if row:
            return {
                "song": row[0],
                "artist": row[1],
                "confidence": row[2],
                "source": "cache"
            }

        return None

    except Exception as e:
        print("Cache read error:", e)
        return None
# store the fingerprint result in the cache
# faster lookup speeds
def store_cached_result(fp_hash, song, artist, confidence):
    try:
        # connect db
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # insert or update existing entry
        cursor.execute("""
            INSERT OR REPLACE INTO acoustid_cache (fingerprint_hash, song, artist, confidence)
            VALUES (?, ?, ?, ?)
        """, (fp_hash, song, artist, confidence))

        conn.commit()
        conn.close()

        print("Cached result stored.")

    except Exception as e:
        print("Cache write error:", e)