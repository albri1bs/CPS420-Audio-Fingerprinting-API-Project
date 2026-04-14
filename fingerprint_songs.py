from dejavu import Dejavu

config = {
    "database_type": "sqlite",
    "database": {
        "db": "dejavu.db"
    }
}

def main():
    djv = Dejavu(config)

    print("Fingerprinting songs...")
    djv.fingerprint_directory("songs/", [".mp3"])
    print("Done!")


if __name__ == "__main__":
    main()