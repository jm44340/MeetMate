import hashlib
import base64
import Database
import os

from enum import Enum
from bson.objectid import ObjectId
import Group

class AuthError(Exception):
    pass

class ExistError(Exception):
    pass

class UserType(Enum):
    USER = "USER"
    ORGANIZER = "ORGANIZER"
    ADMINISTRATOR = "ADMINISTRATOR"

class UserStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class User:
    def __init__(self, id):
        if type(id) is str:
            id = ObjectId(id)

        self.__id = id
        self.update()

    def update(self):
        user = Database.db.get_user(self.__id)
        self.__email = user["email"]
        self.__salt = user["salt"]
        self.__password = user["password"]
        self.__phone_number = user["phone_number"]
        self.__first_name = user["first_name"]
        self.__last_name = user["last_name"]
        self.__groups = user["groups"]
        self.__type = user["type"]
        self.__status = user["status"]

    def add_group(self, group: Group.Group):
        groups = self.__groups
        groups.append(group.id)
        Database.db.update_user(self.__id, "groups", groups)
        self.update()

    def del_group(self, group: Group.Group):
        groups = self.__groups
        if group.id in groups:
            groups.remove(group.id)
        Database.db.update_user(self.__id, "groups", groups)
        self.update()

    @property
    def id(self):
        return self.__id

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        Database.db.update_user(self.__id, "email", value)
        self.update()

    @property
    def salt(self):
        return self.__salt

    @salt.setter
    def salt(self, value):
        Database.db.update_user(self.__id, "salt", value)
        self.update()

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        password = self.salt + value
        hash_string = hashlib.sha512(password.encode()).hexdigest()
        Database.db.update_user(self.__id, "password", hash_string)
        self.update()

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        Database.db.update_user(self.__id, "phone_number", value)
        self.update()

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        Database.db.update_user(self.__id, "first_name", value)
        self.update()

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        Database.db.update_user(self.__id, "last_name", value)
        self.update()

    @property
    def groups(self):
        return [Group.Group(group["_id"]) for group in self.__groups]

    @property
    def type(self):
        return UserType[self.__type]

    @type.setter
    def type(self, value: UserType):
        Database.db.update_user(self.__id, "type", value.value)
        self.update()

    @property
    def status(self):
        return UserStatus[self.__status]

    @status.setter
    def status(self, value: UserStatus):
        Database.db.update_user(self.__id, "status", value.value)
        self.update()

    def check_password(self, password):
        password = self.salt + password
        hash_string = hashlib.sha512(password.encode()).hexdigest()
        return hash_string == self.password

    @staticmethod
    def add_user(email, password, phone_number, first_name, last_name):
        exist = Database.db.get_user(email, "email")
        if exist is not None:
            raise ExistError

        user_id = Database.db.new_user()
        user = User(user_id)
        user.email = email
        user.salt = base64.b64encode(os.urandom(16)).decode()
        user.password = password
        user.phone_number = phone_number
        user.first_name = first_name
        user.last_name = last_name
        user.type = UserType.USER
        user.status = UserStatus.INACTIVE

        return user

    @staticmethod
    def auth(email, password):
        user_data = Database.db.get_user(email, variable="email")
        if user_data is None:
            raise AuthError
        user = User(user_data["_id"])
        if user.check_password(password) == False:
            raise AuthError
        return user

