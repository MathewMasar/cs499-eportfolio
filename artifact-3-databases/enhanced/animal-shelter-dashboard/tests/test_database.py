# ============================================================
# DATABASE CONNECTION TESTS
# ============================================================
# Verifies that the enhanced database connection layer can
# connect to MongoDB and access the configured animals collection.

from database import DatabaseConnection


# Verifies that the database health check confirms
# the MongoDB server is reachable.
def test_database_health_check():

    database = DatabaseConnection()

    assert database.health_check() is True


# Verifies that the configured animals collection
# can be accessed successfully.
def test_database_collection_access():

    database = DatabaseConnection()

    assert database.collection is not None


# Verifies that the imported AAC dataset contains
# animal records and is available to the application.
def test_database_contains_records():

    database = DatabaseConnection()

    record_count = database.collection.count_documents({})

    assert record_count > 0