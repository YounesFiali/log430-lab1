"""
User DAO MongoDB (Data Access Object)
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from models.user import User

class UserDAOMongo:
    def __init__(self):
        try:
            env_path = ".env"
            load_dotenv(dotenv_path=env_path)
            mongo_host = os.getenv("MONGODB_HOST")
            self.client = MongoClient(f"mongodb://labo01:labo01@{mongo_host}:27017/")
            self.db = self.client["labo01_db"]
            self.collection = self.db["users"]

            if self.collection.count_documents({}) == 0:
                self.collection.insert_many([
                    {"name": "Ada Lovelace", "email": "alovelace@example.com"},
                    {"name": "Adele Goldberg", "email": "agoldberg@example.com"},
                    {"name": "Alan Turing", "email": "aturing@example.com"}
            ])

        except Exception as e:
            print("Erreur : " + str(e))

    def select_all(self):
        """ Select all users from MongoDB """
        rows = self.collection.find()
        return [User(str(row["_id"]), row["name"], row["email"]) for row in rows]

    def insert(self, user):
        """ Insert given user into MongoDB """
        result = self.collection.insert_one({"name": user.name, "email": user.email})
        return result.inserted_id

    def update(self, user):
        """ Update given user in MongoDB """
        from bson.objectid import ObjectId
        self.collection.update_one(
            {"_id": ObjectId(user.id)},
            {"$set": {"name": user.name, "email": user.email}}
        )

    def delete(self, user_id):
        """ Delete user from MongoDB with given user ID """
        from bson.objectid import ObjectId
        self.collection.delete_one({"_id": ObjectId(user_id)})

    def delete_all(self):
        """ Empty users collection in MongoDB """
        self.collection.delete_many({})

    def close(self):
        self.client.close()