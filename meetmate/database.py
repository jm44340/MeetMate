from pymongo import MongoClient

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

    # Users

    def new_user(self):
        db_users = self.db.users
        user_id = db_users.insert_one(
            {
                "email": None,
                "salt": None,
                "password": None,
                "phone_number": None,
                "first_name": None,
                "last_name": None,
                "groups": [],
                "type": None,
                "status": None,
            }
        )
        return user_id.inserted_id

    def get_user(self, value: str, variable="_id"):
        db_users = self.db.users
        user = db_users.find_one({variable: value})
        return user

    def update_user(self, user_id, variable, value):
        db_users = self.db.users
        db_users.update_one(
            {"_id": user_id},
            {
                "$set":{
                    variable: value
                }
            }
        )


def database_init(database, host, port, user, password):
    global db

    db = Database(
        database,
        host,
        port,
        user,
        password,
    )