import Database

from bson.objectid import ObjectId
import User

class ExistError(Exception):
    pass

class Group:
    def __init__(self, id):
        if type(id) is str:
            id = ObjectId(id)

        self.__id = id
        self.update()

    def update(self):
        group = Database.db.get_group(self.__id)
        self.__name = group["name"]

    def get_users(self):
        users = Database.db.get_group_users(self.__id)
        return [User.User(user["_id"]) for user in users]

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        Database.db.update_group(self.__id, "name", value)
        self.update()

    @staticmethod
    def add_group(name):
        exist = Database.db.get_group(name, "name")
        if exist is not None:
            raise ExistError

        group_id = Database.db.new_group(name)
        group = Group(group_id)
        group.name = name
        return group

    @staticmethod
    def get_by_name(name):
        group = Database.db.get_group(name, "name")
        if group is None:
            raise ExistError

        return Group(group["_id"])
