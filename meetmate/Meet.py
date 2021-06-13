import decimal
from enum import Enum
from bson.objectid import ObjectId
from cmath import sin, cos, asin, pi, sqrt
import hashlib
import base64
import time
import uuid
import os
import User
import Database
import Setting


class ExistError(Exception):
    pass


class MeetStatus(Enum):
    INACTIVE = "INACTIVE"
    ACTIVE = "ACTIVE"
    ENDED = "ENDED"


class Meet:
    def __init__(self, id):
        if type(id) is str:
            id = ObjectId(id)

        self.__id = id
        self.update()

    def update(self):
        meet = Database.db.get_meet(self.__id)
        self.__name = meet["name"]
        self.__users = meet["users"]
        self.__organizer = meet["organizer"]
        self.__start_time = meet["start_time"]
        self.__stop_time = meet["stop_time"]
        self.__localization = meet["localization"]
        self.__description = meet["description"]
        self.__status = meet["status"]
        self.__longitude = meet["longitude"]
        self.__latitude = meet["latitude"]
        self.__radius = meet["radius"]
        self.__link_id = meet["link_id"]
        self.__secret = meet["secret"]
        self.__checks_count = meet["checks_count"]
        self.__checks_interval = meet["checks_interval"]

    def __calc_qr_hash(self, timestamp):
        secret_string = str(timestamp) + self.__secret
        hash = hashlib.sha256()
        hash.update(secret_string.encode("utf-8"))
        return hash.hexdigest()

    def __calc_distance(self, longitude, latitude):
        earth_radius = 6371000
        diff_lon = (longitude - float(str(self.__longitude))) * (pi / 180)
        diff_lat = (latitude - float(str(self.__latitude))) * (pi / 180)
        a = sin(diff_lat / 2) * sin(diff_lat / 2) + cos(float(str(self.__latitude)) * (pi / 180)) * cos(
            latitude * (pi / 180)) * sin(diff_lon / 2) * sin(diff_lon / 2)
        b = 2 * asin(sqrt(a))
        distance = earth_radius * b
        return distance.real

    def get_qr_data(self):
        timestamp = int(time.time() / Setting.setting["qr_time"])
        hash = self.__calc_qr_hash(timestamp)
        qr_data = "/meet/" + self.__link_id + "/" + hash
        return qr_data

    def check_qr_data(self, hash):
        timestamp = int(time.time() / Setting.setting["qr_time"])
        hash0 = self.__calc_qr_hash(timestamp)
        hash1 = self.__calc_qr_hash(timestamp - 1)
        return (hash == hash0) or (hash == hash1)

    def check_localization(self, longitude, latitude):
        distance = self.__calc_distance(longitude,latitude)
        print(distance.real, self.__radius)
        return distance.real <= self.__radius

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        Database.db.update_meet(self.__id, "name", value)
        self.update()

    @property
    def users(self):
        return self.__users

    @users.setter
    def users(self, value):
        Database.db.update_meet(self.__id, "users", value)
        self.update()

    @property
    def organizer(self):
        return self.__organizer

    @organizer.setter
    def organizer(self, user: User.User):
        Database.db.update_meet(self.__id, "organizer", user.id)
        self.update()

    @property
    def start_time(self):
        return self.__start_time

    @start_time.setter
    def start_time(self, value):
        Database.db.update_meet(self.__id, "start_time", value)
        self.update()

    @property
    def stop_time(self):
        return self.__stop_time

    @stop_time.setter
    def stop_time(self, value):
        Database.db.update_meet(self.__id, "stop_time", value)
        self.update()

    @property
    def localization(self):
        return self.__localization

    @localization.setter
    def localization(self, value):
        Database.db.update_meet(self.__id, "localization", value)
        self.update()

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        Database.db.update_meet(self.__id, "description", value)
        self.update()

    @property
    def status(self):
        return MeetStatus[self.__status]

    @status.setter
    def status(self, value: MeetStatus):
        Database.db.update_meet(self.__id, "status", value.value)
        self.update()

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        Database.db.update_meet(self.__id, "longitude", value)
        self.update()

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        Database.db.update_meet(self.__id, "latitude", value)
        self.update()

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, value):
        Database.db.update_meet(self.__id, "radius", value)
        self.update()

    @property
    def link_id(self):
        return self.__link_id

    @link_id.setter
    def link_id(self, value):
        Database.db.update_meet(self.__id, "link_id", value)
        self.update()

    @property
    def secret(self):
        return self.__secret

    @secret.setter
    def secret(self, value):
        Database.db.update_meet(self.__id, "secret", value)
        self.update()

    @property
    def checks_count(self):
        return self.__checks_count

    @checks_count.setter
    def checks_count(self, value):
        Database.db.update_meet(self.__id, "checks_count", value)
        self.update()

    @property
    def checks_interval(self):
        return self.__checks_interval

    @checks_interval.setter
    def checks_interval(self, value):
        Database.db.update_meet(self.__id, "checks_interval", value)
        self.update()

    @staticmethod
    def get_by_linkid(link_id):
        meet_id = Database.db.get_meet(link_id, variable="link_id")
        if meet_id == None:
            raise ExistError
        return Meet(meet_id["_id"])

    @staticmethod
    def get_by_organizer(user: User.User):
        meetings = Database.db.get_meetings(user.id, variable="organizer")
        return [Meet(meet["_id"]) for meet in meetings]

    @staticmethod
    def get_by_user(user: User.User):
        meetings = Database.db.get_meetings(user.id, variable="user")
        return [Meet(meet["_id"]) for meet in meetings]

    @staticmethod
    def create_meet(name, organizer: User.User, localization, description):
        meet_id = Database.db.new_meet()
        meet = Meet(meet_id)

        meet.name = name
        meet.users = []
        meet.organizer = organizer
        meet.start_time = 0
        meet.stop_time = 0
        meet.localization = localization
        meet.description = description
        meet.status = MeetStatus.INACTIVE
        meet.longitude = 0.0
        meet.latitude = 0.0
        meet.radius = 300
        meet.link_id = base64.b64encode(os.urandom(9)).decode("utf-8").replace("/+", "")
        meet.secret = str(uuid.uuid4())
        meet.checks_count = 0
        meet.checks_interval = 0

        return meet