import os
from dotenv import load_dotenv
# get the environment variables
load_dotenv()

ACOUSTID_API_KEY = os.getenv("ACOUSTID_API_KEY")
DB_PATH = os.getenv("DB_PATH", "dejavu.db")