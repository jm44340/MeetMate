import hashlib
from pymongo import MongoClient

Mongo = None
db = None

class Database:
    def __init__(self, database: str, host="localhost", port=27017, user=None, password=None):
        if user is not None:
            self.Mongo = MongoClient(
                host=host,
                port=port,
                username=user,
                password=password,
                authSource=database
            )
        else:
            self.Mongo = MongoClient(host="localhost", port=27017)

        self.db = self.Mongo[database]

    def add_user(self, user: str, password: str):
        db_users = self.db.users
        db_users.insert_one(
            {
                "username": user,
                "password": hashlib.sha512(password.encode()).hexdigest(),
                "type": "user",
                "status": "unactivated"
            }
        )

    def get_user(self, user: str):
        db_users = self.db.users
        user = list(db_users.find({"username": user}))
        return user