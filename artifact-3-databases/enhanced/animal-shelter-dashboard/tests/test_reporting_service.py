# ============================================================
# REPORTING SERVICE TESTS
# ============================================================
# Verifies that MongoDB aggregation operations return valid
# adoption statistics, breed metrics, age-group summaries, and
# outcome distributions for dashboard reporting.

from database import DatabaseConnection
from reporting_service import ReportingService


# Creates a reporting service connected to the AAC dataset.
def create_reporting_service():

    database = DatabaseConnection()

    return ReportingService(database)


# ============================================================
# ADOPTION SUMMARY TESTS
# ============================================================

# Verifies that the overall adoption summary contains valid
# totals and an adoption rate between 0 and 100 percent.
def test_adoption_summary():

    reports = create_reporting_service()

    result = reports.get_adoption_summary()

    assert "total_animals" in result
    assert "total_adoptions" in result
    assert "adoption_rate" in result

    assert result["total_animals"] > 0
    assert result["total_adoptions"] >= 0

    assert 0 <= result["adoption_rate"] <= 100

    assert result["total_adoptions"] <= result["total_animals"]


# ============================================================
# ANIMAL TYPE REPORT TESTS
# ============================================================

# Verifies that adoption statistics are returned for animal
# types and that each result contains the expected metrics.
def test_adoption_stats_by_animal_type():

    reports = create_reporting_service()

    results = reports.get_adoption_stats_by_animal_type()

    assert len(results) > 0

    for result in results:

        assert "animal_type" in result
        assert "total" in result
        assert "adoptions" in result
        assert "adoption_rate" in result

        assert result["total"] > 0
        assert result["adoptions"] >= 0

        assert result["adoptions"] <= result["total"]

        assert 0 <= result["adoption_rate"] <= 100


# ============================================================
# BREED REPORT TESTS
# ============================================================

# Verifies that the breed report respects the requested result
# limit and returns valid adoption statistics.
def test_adoption_stats_by_breed():

    reports = create_reporting_service()

    results = reports.get_adoption_stats_by_breed(5)

    assert len(results) <= 5
    assert len(results) > 0

    for result in results:

        assert "breed" in result
        assert "total" in result
        assert "adoptions" in result
        assert "adoption_rate" in result

        assert result["total"] > 0
        assert result["adoptions"] >= 0

        assert 0 <= result["adoption_rate"] <= 100


# Verifies that invalid breed report limits are safely rejected.
def test_invalid_breed_limit():

    reports = create_reporting_service()

    results = reports.get_adoption_stats_by_breed(0)

    assert results == []


# ============================================================
# AGE GROUP REPORT TESTS
# ============================================================

# Verifies that age-group reporting returns recognized age
# categories and valid adoption statistics for each category.
def test_adoption_stats_by_age_group():

    reports = create_reporting_service()

    results = reports.get_adoption_stats_by_age_group()

    assert len(results) > 0

    valid_age_groups = {
        "Under 1 year",
        "1-3 years",
        "3-7 years",
        "7+ years"
    }

    for result in results:

        assert result["age_group"] in valid_age_groups

        assert result["total"] > 0
        assert result["adoptions"] >= 0

        assert result["adoptions"] <= result["total"]

        assert 0 <= result["adoption_rate"] <= 100


# ============================================================
# OUTCOME DISTRIBUTION TESTS
# ============================================================

# Verifies that all reported outcome percentages form a complete
# distribution that totals approximately 100 percent.
def test_outcome_distribution():

    reports = create_reporting_service()

    results = reports.get_outcome_distribution()

    assert len(results) > 0

    total_percentage = 0

    for result in results:

        assert "outcome_type" in result
        assert "count" in result
        assert "percentage" in result

        assert result["count"] > 0

        assert 0 <= result["percentage"] <= 100

        total_percentage += result["percentage"]

    # Individual percentages are rounded to two decimal places,
    # so allow a small rounding tolerance around 100 percent.
    assert 99.9 <= total_percentage <= 100.1