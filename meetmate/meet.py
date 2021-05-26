import hashlib
import base64
import database
import uuid
import os

from enum import Enum
from bson.objectid import ObjectId
from user import User

class Meet:
    def __init__(self, id):
        if type(id) is str:
            id = ObjectId(id)

        self.__id = id
        self.update()

    def update(self):
        meet = database.db.get_meet(self.__id)
        self.__name = meet["name"]
        self.__participants = meet["participants"]
        self.__organizer = meet["organizer"]
        self.__start_time = meet["start_time"]
        self.__stop_time = meet["stop_time"]
        self.__localization = meet["localization"]
        self.__description = meet["description"]
        self.__longitude = meet["longitude"]
        self.__latitude = meet["latitude"]
        self.__radius = meet["radius"]
        self.__link_id = meet["link_id"]
        self.__secret = meet["secret"]
        self.__checks_count = meet["checks_count"]
        self.__checks_interval = meet["checks_interval"]

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        database.db.update_meet(self.__id, "name", value)
        self.update()

    @property
    def participants(self):
        return self.__participants

    @participants.setter
    def participants(self, value):
        database.db.update_meet(self.__id, "participants", value)
        self.update()

    @property
    def organizer(self):
        return self.__organizer

    @organizer.setter
    def organizer(self, value):
        database.db.update_meet(self.__id, "organizer", value)
        self.update()

    @property
    def start_time(self):
        return self.__start_time

    @start_time.setter
    def start_time(self, value):
        database.db.update_meet(self.__id, "start_time", value)
        self.update()

    @property
    def stop_time(self):
        return self.__stop_time

    @stop_time.setter
    def stop_time(self, value):
        database.db.update_meet(self.__id, "stop_time", value)
        self.update()

    @property
    def localization(self):
        return self.__localization

    @localization.setter
    def localization(self, value):
        database.db.update_meet(self.__id, "localization", value)
        self.update()

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        database.db.update_meet(self.__id, "description", value)
        self.update()

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        database.db.update_meet(self.__id, "longitude", value)
        self.update()

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        database.db.update_meet(self.__id, "latitude", value)
        self.update()

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, value):
        database.db.update_meet(self.__id, "radius", value)
        self.update()

    @property
    def link_id(self):
        return self.__link_id

    @link_id.setter
    def link_id(self, value):
        database.db.update_meet(self.__id, "link_id", value)
        self.update()

    @property
    def secret(self):
        return self.__secret

    @secret.setter
    def secret(self, value):
        database.db.update_meet(self.__id, "secret", value)
        self.update()

    @property
    def checks_count(self):
        return self.__checks_count

    @checks_count.setter
    def checks_count(self, value):
        database.db.update_meet(self.__id, "checks_count", value)
        self.update()

    @property
    def checks_interval(self):
        return self.__checks_interval

    @checks_interval.setter
    def checks_interval(self, value):
        database.db.update_meet(self.__id, "checks_interval", value)
        self.update()

    @staticmethod
    def get_by_linkid(link_id):
        meet_id = database.db.get_meet(link_id, variable="link_id")
        return Meet(meet_id["_id"])

    @staticmethod
    def create_meet(name, organizer: User, localization, description):
        meet_id = database.db.new_meet()
        meet = Meet(meet_id)

        meet.name = name
        meet.participants = []
        meet.organizer = organizer.id
        meet.start_time = 0
        meet.stop_time = 0
        meet.localization = localization
        meet.description = description
        meet.longitude = 0.0
        meet.latitude = 0.0
        meet.radius = 300
        meet.link_id = str(uuid.uuid4())
        meet.secret = str(uuid.uuid4())
        meet.checks_count = 0
        meet.checks_interval = 0

        return meet