import numpy as np
import librosa
from collections import defaultdict, Counter
from dejavu import Dejavu
from dejavu.fingerprint import fingerprint

# SQLite config
config = {
    "database_type": "sqlite",
    "database": {
        "db": "dejavu.db"
    }
}

# initialize Dejavu
djv = Dejavu(config)


def identify_song(file_path: str):
    try:
        # load audio

        samples, sr = librosa.load(file_path, sr=44100, mono=True)
        samples = np.array(samples, dtype=np.float32)

        duration_ms = int(len(samples) / sr * 1000)
        print("Audio duration (ms):", duration_ms)

        # convert to int16 format for fingerprinting

        samples = np.clip(samples, -1.0, 1.0)
        samples = (samples * 32767).astype(np.int16)

        if len(samples) == 0:
            return {"error": "Audio samples are empty"}

        # generate fingerprints
        hashes = []
        for channel in [samples]:
            hashes.extend(fingerprint(channel, Fs=sr))

        hashes = list(hashes)
        print("Generated hashes:", len(hashes))

        # limit hashes for performance (currently takes 5ish minutes for 2-3 minute songs)
        hashes = hashes[:15000]

        # query database for matches
        raw_matches = djv.db.return_matches(hashes)
        print("Raw matches found:", len(raw_matches))
        print("Sample raw match:", raw_matches[:5])

        # clean matches and handle SQLite offsets properly
        clean_matches = []

        for m in raw_matches:
            try:
                sid = int(m[0])

                # SQLite stores offsets as bytes then convert
                if isinstance(m[1], bytes):
                    offset = int.from_bytes(m[1], byteorder='little')
                else:
                    offset = int(m[1])

                clean_matches.append((sid, offset))
            except:
                continue

        print("Clean matches:", len(clean_matches))

        if not clean_matches:
            return {"song": "No match", "confidence": 0}


        # align matches
        offset_groups = defaultdict(list)

        for sid, offset in clean_matches:
            offset_groups[sid].append(offset)

        best_song = None
        best_score = 0

        for sid, offsets in offset_groups.items():
            offset_count = Counter(offsets)
            _, count = offset_count.most_common(1)[0]

            if count > best_score:
                best_score = count
                best_song = sid

        print("Best song ID:", best_song)
        print("Best score:", best_score)

        if best_song is None:
            return {"song": "No match", "confidence": 0}


        # lookup song name
        song = djv.db.get_song_by_id(best_song)
        print("Best song raw:", song)

        # handle different return formats safely
        if isinstance(song, tuple):
            song_name = song[1]
        elif isinstance(song, str):
            song_name = song
        else:
            song_name = f"ID {best_song}"

        return {
            "song": song_name,
            "confidence": best_score
        }

    except Exception as e:
        return {"error": str(e)}