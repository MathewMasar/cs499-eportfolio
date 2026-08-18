# ============================================================
# DATABASE CONFIGURATION
# ============================================================
# Loads MongoDB connection settings from environment variables.
# Default values support local development while allowing secure
# credentials to be supplied without storing them in source code.

from dotenv import load_dotenv
import os


# Load values stored in the local .env file when available.
load_dotenv()


# = = MongoDB Configuration = =

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", "27017"))

MONGO_DB = os.getenv("MONGO_DB", "aac")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "animals")

# Authentication is optional so the local development database
# can operate without requiring MongoDB credentials.
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")