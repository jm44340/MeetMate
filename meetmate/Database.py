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

    def get_all_users(self):
        db_users = self.db.users
        users = db_users.find({})
        return users

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

    # Groups
    
    def new_group(self, name):
        db_groups = self.db.groups
        group_id = db_groups.insert_one(
            {
                "name": name,
            }
        )
        return group_id.inserted_id

    def get_group(self, value: str, variable="_id"):
        db_groups = self.db.groups
        group = db_groups.find_one({variable: value})
        return group

    def update_group(self, group_id, variable, value):
        db_groups = self.db.groups
        db_groups.update_one(
            {"_id": group_id},
            {
                "$set":{
                    variable: value
                }
            }
        )

    def get_group_users(self, group_id):
        db_users = self.db.users
        users = db_users.find({"groups": {"$in": [group_id]}})
        return list(users)

    # Meets

    def new_meet(self):
        db_meets = self.db.meets
        meet_id = db_meets.insert_one(
            {
                #General
                "name": None, 
                "users": [],
                "organizer": None,
                "start_time": None,
                "stop_time": None,
                "localization": None,
                "description": None,
                "status": None,
                #GPS
                "longitude": None,
                "latitude": None,
                "radius": None,
                #QR Code
                "link_id": None,
                "secret": None,
                #Checks
                "checks_count": 0,
                "checks_interval": 0
            }
        )
        return meet_id.inserted_id

    def get_meet(self, value: str, variable="_id"):
        db_meets = self.db.meets
        meet = db_meets.find_one({variable: value})
        return meet

    def get_meetings(self, value: str, variable="_id"):
        db_meets = self.db.meets
        meetings = db_meets.find({variable: value})
        return list(meetings)

    def update_meet(self, meet_id, variable, value):
        db_meets = self.db.meets
        db_meets.update_one(
            {"_id": meet_id},
            {
                "$set":{
                    variable: value
                }
            }
        )

    # Presence

    def new_presence(self):
        db_presence = self.db.presence
        presence_id = db_presence.insert_one(
            {
                "time": None,
                "meeting": None,
                "user": None
            }
        )
        return presence_id.inserted_id

    def get_presence(self, value: str, variable="_id"):
        db_presence = self.db.presence
        presence = db_presence.find_one({variable: value})
        return presence

    def update_presence(self, presence_id, variable, value):
        db_presence = self.db.presence
        db_presence.update_one(
            {"_id": presence_id},
            {
                "$set":{
                    variable: value
                }
            }
        )



# logs

    def log_new_entry(self):
        db_logs = self.db.logs
        entry_id = db_logs.insert_one(
            {
                "time": None,
                "user": None,
                "client_ip": None,
                "request_code": None,
                "request_desc": None,
                "response_code": None,
                "response_desc": None,
            }
        )
        return entry_id.inserted_id

    def log_update(self, entry_id, variable, value):
        db_logs = self.db.logs
        db_logs.update_one(
            {"_id": entry_id},
            {
                "$set":{
                    variable: value
                }
            }
        )

    def get_log_entry(self, value: str, variable="_id"):
        db_logs = self.db.logs
        return db_logs.find_one({variable: value})

    def get_log_entries(self):
        db_logs = self.db.logs
        return list(db_logs.find())


def database_init(database, host, port, user, password):
    global db

    db = Database(
        database,
        host,
        port,
        user,
        password,
    )
