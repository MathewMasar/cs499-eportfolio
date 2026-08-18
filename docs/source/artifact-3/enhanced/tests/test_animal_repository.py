# ============================================================
# ANIMAL REPOSITORY TESTS
# ============================================================
# Verifies CRUD operations, validation, advanced searching, and
# geospatial functionality provided by the enhanced repository.
# Temporary test records are removed after each test to preserve
# the original AAC dataset.

import pytest

from database import DatabaseConnection
from animal_repository import AnimalRepository


# Unique ID used only by the automated test suite.
TEST_ANIMAL_ID = "PYTEST999"


@pytest.fixture
def repository():

    database = DatabaseConnection()
    repo = AnimalRepository(database)

    # Remove a leftover test record if a previous test run
    # was interrupted before cleanup occurred.
    repo.collection.delete_many({
        "animal_id": TEST_ANIMAL_ID
    })

    yield repo

    # Always remove the temporary record after the test.
    repo.collection.delete_many({
        "animal_id": TEST_ANIMAL_ID
    })


def create_test_animal(repository):

    test_animal = {
        "animal_id": TEST_ANIMAL_ID,
        "animal_type": "Dog",
        "breed": "Test Breed",
        "color": "Black",
        "outcome_type": "Adoption",
        "sex_upon_outcome": "Neutered Male",
        "age_upon_outcome_in_weeks": 52.0,
        "location_lat": 30.50665787,
        "location_long": -97.34087807
    }

    return repository.create(test_animal)


# ============================================================
# CREATE AND READ TESTS
# ============================================================

def test_create_animal(repository):

    result = create_test_animal(repository)

    assert result is True

    records = repository.read({
        "animal_id": TEST_ANIMAL_ID
    })

    assert len(records) == 1
    assert records[0]["animal_id"] == TEST_ANIMAL_ID


def test_duplicate_animal_id_rejected(repository):

    assert create_test_animal(repository) is True

    duplicate_result = create_test_animal(repository)

    assert duplicate_result is False


# ============================================================
# ADVANCED SEARCH TESTS
# ============================================================

def test_search_animals_by_multiple_filters(repository):

    create_test_animal(repository)

    results = repository.search_animals(
        animal_type="Dog",
        breed="Test Breed",
        outcome_type="Adoption",
        min_age_weeks=50,
        max_age_weeks=60
    )

    matching_records = [
        animal for animal in results
        if animal.get("animal_id") == TEST_ANIMAL_ID
    ]

    assert len(matching_records) == 1


def test_invalid_age_range_rejected(repository):

    results = repository.search_animals(
        min_age_weeks=100,
        max_age_weeks=50
    )

    assert results == []


# ============================================================
# GEOSPATIAL TESTS
# ============================================================

def test_create_generates_geojson_location(repository):

    create_test_animal(repository)

    records = repository.read({
        "animal_id": TEST_ANIMAL_ID
    })

    assert len(records) == 1

    location = records[0]["location"]

    assert location["type"] == "Point"
    assert location["coordinates"] == [
        -97.34087807,
        30.50665787
    ]


def test_nearby_animal_search(repository):

    create_test_animal(repository)

    results = repository.find_nearby_animals(
        -97.34087807,
        30.50665787,
        100
    )

    matching_records = [
        animal for animal in results
        if animal.get("animal_id") == TEST_ANIMAL_ID
    ]

    assert len(matching_records) == 1

# ============================================================
# UPDATE TESTS
# ============================================================

def test_valid_update(repository):

    create_test_animal(repository)

    modified_count = repository.update(
        {"animal_id": TEST_ANIMAL_ID},
        {"breed": "Updated Test Breed"}
    )

    assert modified_count == 1

    records = repository.read({
        "animal_id": TEST_ANIMAL_ID
    })

    assert records[0]["breed"] == "Updated Test Breed"


def test_protected_animal_id_cannot_be_updated(repository):

    create_test_animal(repository)

    modified_count = repository.update(
        {"animal_id": TEST_ANIMAL_ID},
        {"animal_id": "CHANGED999"}
    )

    assert modified_count == 0

    original_record = repository.read({
        "animal_id": TEST_ANIMAL_ID
    })

    assert len(original_record) == 1


def test_empty_update_rejected(repository):

    create_test_animal(repository)

    modified_count = repository.update(
        {"animal_id": TEST_ANIMAL_ID},
        {}
    )

    assert modified_count == 0


# ============================================================
# DELETE TESTS
# ============================================================

def test_valid_delete(repository):

    create_test_animal(repository)

    deleted_count = repository.delete({
        "animal_id": TEST_ANIMAL_ID
    })

    assert deleted_count == 1

    records = repository.read({
        "animal_id": TEST_ANIMAL_ID
    })

    assert records == []


def test_broad_delete_query_rejected(repository):

    create_test_animal(repository)

    deleted_count = repository.delete({
        "animal_type": "Dog"
    })

    assert deleted_count == 0

    # Make sure our test animal still exists.
    records = repository.read({
        "animal_id": TEST_ANIMAL_ID
    })

    assert len(records) == 1