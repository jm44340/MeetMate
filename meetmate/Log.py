import datetime
import hashlib
import base64

from flask import request

import Database
import os

from enum import Enum
from bson.objectid import ObjectId
import Group


class Log:
    def __init__(self, id):
        if type(id) is str:
            id = ObjectId(id)
        self.__id = id
        self.update()

    def update(self):
        entry = Database.db.get_log_entry(self.__id)
        self.__time = entry["time"]
        self.__client_ip = entry["client_ip"]
        self.__user = entry["user"]
        self.__request_code = entry["request_code"]
        self.__request_desc = entry["request_desc"]
        self.__response_code = entry["response_code"]
        self.__response_desc = entry["response_desc"]

    @property
    def id(self):
        return self.__id

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        Database.db.log_update(self.__id, "user", value)
        self.update()

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, value):
        Database.db.log_update(self.__id, "time", value)
        self.update()

    @property
    def client_ip(self):
        return self.__client_ip

    @client_ip.setter
    def client_ip(self, value):
        Database.db.log_update(self.__id, "client_ip", value)
        self.update()

    @property
    def request_code(self):
        return self.__request_code

    @request_code.setter
    def request_code(self, value):
        Database.db.log_update(self.__id, "request_code", value)
        self.update()

    @property
    def request_desc(self):
        return self.__request_desc

    @request_desc.setter
    def request_desc(self, value):
        Database.db.log_update(self.__id, "request_desc", value)
        self.update()

    @property
    def response_code(self):
        return self.__response_code

    @response_code.setter
    def response_code(self, value):
        Database.db.log_update(self.__id, "response_code", value)
        self.update()

    @property
    def response_desc(self):
        return self.__response_desc

    @response_desc.setter
    def response_desc(self, value):
        Database.db.log_update(self.__id, "response_desc", value)
        self.update()

    @staticmethod
    def get_logs():
        entries = Database.db.get_log_entries()
        return [Log(entry["_id"]) for entry in entries]

    @staticmethod
    def add_entry(user, request_code, request_desc, response_code, response_desc):
        entry_id = Database.db.log_new_entry()
        entry = Log(entry_id)
        entry.time = datetime.datetime.now()
        entry.client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        entry.user = user
        entry.request_code = request_code
        entry.request_desc = request_desc
        entry.response_code = response_code
        entry.response_desc = response_desc
        return entry
