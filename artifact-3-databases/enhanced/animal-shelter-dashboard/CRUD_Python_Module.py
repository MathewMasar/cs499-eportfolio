# Example Python Code to Insert a Document 

from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConnectionFailure
from dotenv import load_dotenv
from pymongo import MongoClient, GEOSPHERE
import os

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    # Constructor establishes MongoDB connection using environment configuration
    def __init__(self):

        # Load local values from .env when available
        load_dotenv()

        # = = Database Configuration = =
        host = os.getenv("MONGO_HOST", "localhost")
        port = int(os.getenv("MONGO_PORT", "27017"))
        database_name = os.getenv("MONGO_DB", "aac")
        collection_name = os.getenv("MONGO_COLLECTION", "animals")

        username = os.getenv("MONGO_USERNAME")
        password = os.getenv("MONGO_PASSWORD")

        try:
            # If credentials are provided, create an authenticated connection.
            if username and password:
                connection_string = (
                    f"mongodb://{username}:{password}@{host}:{port}"
                )
            else:
                # Local development can connect without authentication.
                connection_string = f"mongodb://{host}:{port}"

            self.client = MongoClient(
                connection_string,
                serverSelectionTimeoutMS=5000
            )

            # Force an immediate connection attempt instead of waiting
            # until the first database operation is performed.
            self.client.admin.command("ping")

            self.database = self.client[database_name]
            self.collection = self.database[collection_name]

        except ConnectionFailure as e:
            raise ConnectionError(
                f"Unable to connect to MongoDB: {e}"
            ) from e


    # Method verifies that the MongoDB server is reachable
    def health_check(self):
        try:
            self.client.admin.command("ping")
            return True
        except PyMongoError:
            return False
    
        # Method converts latitude and longitude values into a GeoJSON Point
    
    # so MongoDB can perform location based searches and geospatial queries
    def create_location_points(self):

        try:
            # Find records that have valid latitude and longitude values
            query = {
                "location_lat": {"$exists": True},
                "location_long": {"$exists": True}
            }

            records = self.collection.find(
                query,
                {
                    "_id": 1,
                    "location_lat": 1,
                    "location_long": 1
                }
            )

            updated_count = 0
            skipped_count = 0

            for record in records:

                latitude = record.get("location_lat")
                longitude = record.get("location_long")

                # Make sure coordinates are numeric before creating GeoJSON data
                if not isinstance(latitude, (int, float)) or not isinstance(
                        longitude, (int, float)):

                    skipped_count += 1
                    continue

                # MongoDB GeoJSON requires coordinates in:
                # [longitude, latitude] order.
                location = {
                    "type": "Point",
                    "coordinates": [
                        longitude,
                        latitude
                    ]
                }

                result = self.collection.update_one(
                    {"_id": record["_id"]},
                    {"$set": {"location": location}}
                )

                if result.modified_count > 0:
                    updated_count += 1

            print(
                f"Location conversion complete: "
                f"{updated_count} updated, "
                f"{skipped_count} skipped."
            )

            return updated_count

        except PyMongoError as e:
            print(f"Location conversion failed: {e}")
            return 0


    # Method creates indexes for fields commonly searched by the application.
    # These indexes improve retrieval performance as the collection grows.
    def ensure_indexes(self):

        try:
            # Unique animal identifier used for direct animal lookup
            self.collection.create_index(
                "animal_id",
                name="idx_animal_id"
            )

            # Supports filtering animals by type such as Dog or Cat
            self.collection.create_index(
                "animal_type",
                name="idx_animal_type"
            )

            # Supports breed-based searches and rescue category filtering
            self.collection.create_index(
                "breed",
                name="idx_breed"
            )

            # Supports searches based on adoption, transfer, and other outcomes
            self.collection.create_index(
                "outcome_type",
                name="idx_outcome_type"
            )

            # Specialized geospatial index used for map and location searches
            self.collection.create_index(
                [("location", GEOSPHERE)],
                name="idx_location_2dsphere"
            )

            print("Database indexes verified successfully.")
            return True

        except PyMongoError as e:
            print(f"Index creation failed: {e}")
            return False
    
    
    
    
    # Method ensures unique entry to DB (rec_num and animal_id)
    def validate_create_ids(self, data):
        
        # if rec_num, doc already in DB, not a create
        if "rec_num" in data:
            print("Create skipped: rec_num provided. Use update() instead.")
            return False
        
        # if animal id non existent in data
        if "animal_id" not in data or not data["animal_id"]:
            print("Create failed: animal_id field required.")
            return False
        
        # duplication check assignment
        existing = self.collection.find_one({"animal_id": data["animal_id"]})
        
        # if animal id duplicate
        if existing:
            print("Create skipped: animal_id already exists. Use update() instead.")
            return False
        
        return True
    
    # Create a method to return the next available record number for use in the create method
    def get_next_rec_num(self):
    
        try:
            last_doc = self.collection.find_one(
                {"rec_num": {"$exists": True}},
                sort=[("rec_num", -1)],
                projection={"rec_num": 1}
            )
            if last_doc and "rec_num" in last_doc:
                return int(last_doc["rec_num"]) + 1
            return 1
        except PyMongoError as e:
            print(f"Failed to get next rec_num: {e}")
            return 1
    
    # Method validates query has valid rec_num or animal_num for queries
    def validate_target_query(self, query):

        # 1) format check
        if not isinstance(query, dict) or not query:
            print("Operation failed: invalid format.")
            return None

        try:
            # 2) use rec_num if present
            if "rec_num" in query and query["rec_num"] is not None:
                # string vs int validate
                rec = query["rec_num"]
                if isinstance(rec, str) and rec.isdigit():
                    rec = int(rec)
                
                # find rec_num 
                exists = self.collection.find_one({"rec_num": rec}, projection={"_id": 1})
                if not exists:
                    print("Operation failed: rec_num invalid.")
                    return None

                return {"rec_num": rec}

            # 3) if no rec_num, fall back to animal_id
            if "animal_id" in query and query["animal_id"]:
                exists = self.collection.find_one({"animal_id": query["animal_id"]}, projection={"_id": 1})
                if not exists:
                    print("Operation failed: animal_id invalid.")
                    return None

                return {"animal_id": query["animal_id"]}

            # 4) must have one of them
            print("Operation failed: query must include 'rec_num' or 'animal_id'.")
            return None

        except PyMongoError as e:
            print(f"Operation failed: {e}")
            return None
    
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        #if data is not None: 
            #self.database.animals.insert_one(data)  # data should be dictionary
        # make sure format is valid
        if not isinstance(data, dict) or not data:
            print("Create failed: invalid format.")
            return False
        
        try:
            # 1) ensure valid animal_id
            if not self.validate_create_ids(data):
                return False
            
            # 2) valid data, get next rec_num
            data["rec_num"] = self.get_next_rec_num()
            
            # 3) insert 
            result = self.collection.insert_one(data)
            return result.inserted_id is not None

        except PyMongoError as e:
            print(f"Create failed: {e}")
            return False

    # Create method to implement the R in CRUD.
    def read(self, query):
        
        if not isinstance(query, dict):
            print("Read failed: invalid format.")
            return []

        try:
            # find results in db
            results = list(self.collection.find(query))

            if not results:
                print("Read completed: no matching records found.")

            return results

        except PyMongoError as e:
            print(f"Read failed: {e}")
            return []
    
    
    # Method performs an advanced search of animal records using optional
    # filters. The query is built dynamically so the caller may search by
    # one field or combine multiple criteria without creating separate
    # database methods for every possible search combination.
    def search_animals(
            self,
            animal_type=None,
            breed=None,
            outcome_type=None,
            min_age_weeks=None,
            max_age_weeks=None):

        # = = Input Validation = =

        # Age values must be numeric when provided.
        if min_age_weeks is not None and not isinstance(
                min_age_weeks, (int, float)):
            print("Search failed: minimum age must be numeric.")
            return []

        if max_age_weeks is not None and not isinstance(
                max_age_weeks, (int, float)):
            print("Search failed: maximum age must be numeric.")
            return []

        # Negative ages are not valid for animal records.
        if min_age_weeks is not None and min_age_weeks < 0:
            print("Search failed: minimum age cannot be negative.")
            return []

        if max_age_weeks is not None and max_age_weeks < 0:
            print("Search failed: maximum age cannot be negative.")
            return []

        # If both boundaries are supplied, the minimum cannot
        # be greater than the maximum.
        if (
            min_age_weeks is not None
            and max_age_weeks is not None
            and min_age_weeks > max_age_weeks
        ):
            print(
                "Search failed: minimum age cannot be "
                "greater than maximum age."
            )
            return []

        # = = Build MongoDB Query = =

        # Begin with an empty query. Each supplied search option
        # adds another condition to the MongoDB query.
        query = {}

        if animal_type:
            query["animal_type"] = animal_type

        if breed:
            query["breed"] = breed

        if outcome_type:
            query["outcome_type"] = outcome_type

        # Age is stored numerically in weeks, allowing MongoDB to
        # perform efficient range comparisons instead of comparing
        # values such as "1 year" or "3 months" as strings.
        if min_age_weeks is not None or max_age_weeks is not None:

            age_query = {}

            if min_age_weeks is not None:
                age_query["$gte"] = min_age_weeks

            if max_age_weeks is not None:
                age_query["$lte"] = max_age_weeks

            query["age_upon_outcome_in_weeks"] = age_query

        # = = Execute Search = =

        try:
            # MongoDB evaluates all supplied query conditions together.
            # Converting the cursor to a list provides the caller with
            # the matching animal records.
            results = list(
                self.collection.find(query)
            )

            return results

        except PyMongoError as e:
            print(f"Animal search failed: {e}")
            return []
    
    
    # Method returns animals located near a selected geographic point.
    # MongoDB uses the 2dsphere index on the GeoJSON "location" field
    # to perform the distance based search efficiently.
    def find_nearby_animals(
            self,
            longitude,
            latitude,
            max_distance_meters=16093):

        # = = Input Validation = =
        if not isinstance(longitude, (int, float)):
            print("Nearby search failed: longitude must be numeric.")
            return []

        if not isinstance(latitude, (int, float)):
            print("Nearby search failed: latitude must be numeric.")
            return []

        if not isinstance(max_distance_meters, (int, float)) \
                or max_distance_meters <= 0:

            print(
                "Nearby search failed: "
                "maximum distance must be greater than zero."
            )
            return []

        # Longitude and latitude must fall within valid geographic ranges.
        if longitude < -180 or longitude > 180:
            print(
                "Nearby search failed: "
                "longitude must be between -180 and 180."
            )
            return []

        if latitude < -90 or latitude > 90:
            print(
                "Nearby search failed: "
                "latitude must be between -90 and 90."
            )
            return []

        try:
            # $near searches outward from the selected point.
            # MongoDB GeoJSON coordinates use [longitude, latitude].
            query = {
                "location": {
                    "$near": {
                        "$geometry": {
                            "type": "Point",
                            "coordinates": [
                                longitude,
                                latitude
                            ]
                        },
                        "$maxDistance": max_distance_meters
                    }
                }
            }

            results = list(
                self.collection.find(query)
            )

            return results

        except PyMongoError as e:
            print(f"Nearby animal search failed: {e}")
            return []
        
    # Method implements the CRUD UPDATE
    def update(self, query, update_data):
        if not isinstance(update_data, dict) or not update_data:
            print("Update failed: invalid format.")
            return 0

        target = self.validate_target_query(query)
        if not target:
            return 0

        try:
            # update db document
            result = self.collection.update_one(target, {"$set": update_data})
            return result.modified_count
        except PyMongoError as e:
            print(f"Update failed: {e}")
            return 0
    
    # Method implements the CRUD DELETE
    def delete(self, query):
        target = self.validate_target_query(query)
        if not target:
            return 0

        try:
            # delete document
            result = self.collection.delete_one(target)
            return result.deleted_count
        except PyMongoError as e:
            print(f"Delete failed: {e}")
            return 0
