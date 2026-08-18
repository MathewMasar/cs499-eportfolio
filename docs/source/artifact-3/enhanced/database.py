# ============================================================
# DATABASE CONNECTION
# ============================================================
# Manages the MongoDB connection used by the application.
# Database configuration is kept separate from repository logic
# so connection details can be changed without modifying CRUD
# operations or dashboard functionality.

from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConnectionFailure

from config import (
    MONGO_HOST,
    MONGO_PORT,
    MONGO_DB,
    MONGO_COLLECTION,
    MONGO_USERNAME,
    MONGO_PASSWORD
)


class DatabaseConnection:

    # Constructor establishes the MongoDB connection using
    # configuration values loaded from the environment.
    def __init__(self):

        try:

            # Use authentication when credentials have been supplied.
            if MONGO_USERNAME and MONGO_PASSWORD:
                connection_string = (
                    f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}"
                    f"@{MONGO_HOST}:{MONGO_PORT}"
                )

            else:
                # Local development can connect without authentication.
                connection_string = (
                    f"mongodb://{MONGO_HOST}:{MONGO_PORT}"
                )

            self.client = MongoClient(
                connection_string,
                serverSelectionTimeoutMS=5000
            )

            # Force an immediate connection attempt rather than
            # waiting until the first database operation occurs.
            self.client.admin.command("ping")

            self.database = self.client[MONGO_DB]
            self.collection = self.database[MONGO_COLLECTION]

        except ConnectionFailure as e:
            raise ConnectionError(
                f"Unable to connect to MongoDB: {e}"
            ) from e


    # Method verifies that the MongoDB server is currently reachable.
    def health_check(self):

        try:
            self.client.admin.command("ping")
            return True

        except PyMongoError:
            return False