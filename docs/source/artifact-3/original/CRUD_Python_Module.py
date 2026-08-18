# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 
from pymongo.errors import PyMongoError

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username="aacuser", password="Password123"):
        HOST = "localhost"
        PORT = 27017
        DB = "aac"
        COL = "animals"

        self.client = MongoClient(f"mongodb://{username}:{password}@{HOST}:{PORT}")
        self.database = self.client[DB]
        self.collection = self.database[COL]

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
