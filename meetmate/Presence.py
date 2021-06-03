from bson.objectid import ObjectId
import time
import Database
import Meet
import User


class ExistError(Exception):
    pass


class Presence:
    def __init__(self, id):
        if type(id) is str:
            id = ObjectId(id)

        self.__id = id
        self.update()

    def update(self):
        presence = Database.db.get_presence(self.__id)
        self.__time = presence["time"]
        self.__meeting = presence["meeting"]
        self.__user = presence["user"]

    @property
    def id(self):
        return self.__id

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, value):
        Database.db.update_presence(self.__id, "time", value)
        self.update()

    @property
    def meeting(self):
        return Meet.Meet(self.__meeting)

    @meeting.setter
    def meeting(self, meet: Meet.Meet):
        Database.db.update_presence(self.__id, "meeting", meet.id)
        self.update()

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user: User.User):
        Database.db.update_presence(self.__id, "user", user.id)
        self.update()

    @staticmethod
    def new_presence(meet : Meet.Meet, user: User.User):
        presence_id = Database.db.new_presence()
        presence = Presence(presence_id)
        presence.time = int(time.time())
        presence.meeting = meet
        presence.user = user
        return presence