# ============================================================
# ANIMAL SHELTER REPORTING SERVICE
# ============================================================
# Provides MongoDB aggregation and reporting operations used by
# the animal shelter dashboard. Reporting logic is separated from
# standard CRUD operations so analytics can grow independently
# without increasing the complexity of the animal repository.

from pymongo.errors import PyMongoError


class ReportingService:

    # Constructor receives the shared database connection and
    # provides reporting methods access to the animals collection.
    def __init__(self, database_connection):

        self.database_connection = database_connection
        self.collection = database_connection.collection

    # ============================================================
    # ADOPTION SUMMARY REPORTS
    # ============================================================

    # Returns overall adoption totals and the adoption percentage
    # across the entire animal collection.
    def get_adoption_summary(self):

        try:
            total_animals = self.collection.count_documents({})

            total_adoptions = self.collection.count_documents(
                {"outcome_type": "Adoption"}
            )

            adoption_rate = (
                (total_adoptions / total_animals) * 100
                if total_animals > 0
                else 0
            )

            return {
                "total_animals": total_animals,
                "total_adoptions": total_adoptions,
                "adoption_rate": round(adoption_rate, 2)
            }

        except PyMongoError as e:
            print(f"Adoption summary failed: {e}")
            return {}


    # ============================================================
    # ADOPTION REPORTS BY ANIMAL TYPE
    # ============================================================

    # Returns total records, adoption count, and adoption rate for
    # each animal type represented in the collection.
    def get_adoption_stats_by_animal_type(self):

        pipeline = [
            {
                "$group": {
                    "_id": "$animal_type",
                    "total": {"$sum": 1},
                    "adoptions": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$outcome_type", "Adoption"]},
                                1,
                                0
                            ]
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "animal_type": "$_id",
                    "total": 1,
                    "adoptions": 1,
                    "adoption_rate": {
                        "$cond": [
                            {"$gt": ["$total", 0]},
                            {
                                "$multiply": [
                                    {
                                        "$divide": [
                                            "$adoptions",
                                            "$total"
                                        ]
                                    },
                                    100
                                ]
                            },
                            0
                        ]
                    }
                }
            },
            {
                "$sort": {
                    "total": -1
                }
            }
        ]

        try:
            results = list(
                self.collection.aggregate(pipeline)
            )

            for result in results:
                result["adoption_rate"] = round(
                    result["adoption_rate"],
                    2
                )

            return results

        except PyMongoError as e:
            print(f"Animal type adoption report failed: {e}")
            return []


    # ============================================================
    # ADOPTION REPORTS BY BREED
    # ============================================================

    # Returns total records, adoption count, and adoption rate for
    # the breeds with the highest number of completed adoptions.
    def get_adoption_stats_by_breed(self, limit=10):

        if not isinstance(limit, int) or limit <= 0:
            print(
                "Breed adoption report failed: "
                "limit must be a positive integer."
            )
            return []

        pipeline = [
            {
                "$match": {
                    "breed": {
                        "$exists": True,
                        "$nin": [None, ""]
                    }
                }
            },
            {
                "$group": {
                    "_id": "$breed",
                    "total": {
                        "$sum": 1
                    },
                    "adoptions": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$eq": [
                                        "$outcome_type",
                                        "Adoption"
                                    ]
                                },
                                1,
                                0
                            ]
                        }
                    }
                }
            },

            # Remove breeds with no completed adoptions.
            {
                "$match": {
                    "adoptions": {
                        "$gt": 0
                    }
                }
            },

            {
                "$project": {
                    "_id": 0,
                    "breed": "$_id",
                    "total": 1,
                    "adoptions": 1,
                    "adoption_rate": {
                        "$cond": [
                            {
                                "$gt": [
                                    "$total",
                                    0
                                ]
                            },
                            {
                                "$multiply": [
                                    {
                                        "$divide": [
                                            "$adoptions",
                                            "$total"
                                        ]
                                    },
                                    100
                                ]
                            },
                            0
                        ]
                    }
                }
            },

            # Rank breeds by completed adoption count.
            {
                "$sort": {
                    "adoptions": -1
                }
            },

            {
                "$limit": limit
            }
        ]

        try:
            results = list(
                self.collection.aggregate(pipeline)
            )

            for result in results:
                result["adoption_rate"] = round(
                    result["adoption_rate"],
                    2
                )

            return results

        except PyMongoError as e:
            print(
                f"Breed adoption report failed: {e}"
            )
            return []


    # ============================================================
    # ADOPTION REPORTS BY AGE GROUP
    # ============================================================

    # Groups animals into practical age ranges and returns each
    # group's total animals, adoption count, and adoption rate.
    def get_adoption_stats_by_age_group(self):

        pipeline = [
            {
                "$match": {
                    "age_upon_outcome_in_weeks": {
                        "$type": "double"
                    }
                }
            },
            {
                "$project": {
                    "outcome_type": 1,
                    "age_group": {
                        "$switch": {
                            "branches": [
                                {
                                    "case": {
                                        "$lt": [
                                            "$age_upon_outcome_in_weeks",
                                            52
                                        ]
                                    },
                                    "then": "Under 1 year"
                                },
                                {
                                    "case": {
                                        "$lt": [
                                            "$age_upon_outcome_in_weeks",
                                            156
                                        ]
                                    },
                                    "then": "1-3 years"
                                },
                                {
                                    "case": {
                                        "$lt": [
                                            "$age_upon_outcome_in_weeks",
                                            364
                                        ]
                                    },
                                    "then": "3-7 years"
                                }
                            ],
                            "default": "7+ years"
                        }
                    }
                }
            },
            {
                "$group": {
                    "_id": "$age_group",
                    "total": {"$sum": 1},
                    "adoptions": {
                        "$sum": {
                            "$cond": [
                                {"$eq": ["$outcome_type", "Adoption"]},
                                1,
                                0
                            ]
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "age_group": "$_id",
                    "total": 1,
                    "adoptions": 1,
                    "adoption_rate": {
                        "$cond": [
                            {"$gt": ["$total", 0]},
                            {
                                "$multiply": [
                                    {
                                        "$divide": [
                                            "$adoptions",
                                            "$total"
                                        ]
                                    },
                                    100
                                ]
                            },
                            0
                        ]
                    }
                }
            }
        ]

        try:
            results = list(
                self.collection.aggregate(pipeline)
            )

            age_order = {
                "Under 1 year": 1,
                "1-3 years": 2,
                "3-7 years": 3,
                "7+ years": 4
            }

            for result in results:
                result["adoption_rate"] = round(
                    result["adoption_rate"],
                    2
                )

            results.sort(
                key=lambda result:
                    age_order.get(result["age_group"], 99)
            )

            return results

        except PyMongoError as e:
            print(f"Age adoption report failed: {e}")
            return []


    # ============================================================
    # OUTCOME DISTRIBUTION REPORTS
    # ============================================================

    # Returns every outcome type along with its total count and its
    # percentage of all animal outcomes in the collection.
    def get_outcome_distribution(self):

        pipeline = [
            {
                "$match": {
                    "outcome_type": {
                        "$exists": True,
                        "$nin": [None, ""]
                    }
                }
            },
            {
                "$group": {
                    "_id": "$outcome_type",
                    "count": {"$sum": 1}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_outcomes": {
                        "$sum": "$count"
                    },
                    "outcomes": {
                        "$push": {
                            "outcome_type": "$_id",
                            "count": "$count"
                        }
                    }
                }
            },
            {
                "$unwind": "$outcomes"
            },
            {
                "$project": {
                    "_id": 0,
                    "outcome_type":
                        "$outcomes.outcome_type",
                    "count":
                        "$outcomes.count",
                    "percentage": {
                        "$multiply": [
                            {
                                "$divide": [
                                    "$outcomes.count",
                                    "$total_outcomes"
                                ]
                            },
                            100
                        ]
                    }
                }
            },
            {
                "$sort": {
                    "count": -1
                }
            }
        ]

        try:
            results = list(
                self.collection.aggregate(pipeline)
            )

            for result in results:
                result["percentage"] = round(
                    result["percentage"],
                    2
                )

            return results

        except PyMongoError as e:
            print(f"Outcome distribution report failed: {e}")
            return []

        pipeline = [
            {
                "$group": {
                    "_id": "$animal_type",
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {
                    "count": -1
                }
            }
        ]

        try:
            return list(self.collection.aggregate(pipeline))

        except PyMongoError as e:
            print(f"Animal type report failed: {e}")
            return []