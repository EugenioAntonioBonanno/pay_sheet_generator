import os
from hashlib import sha256 as hash
import pickle


class User:

    username: str
    hashed_password: str

    def __init__(self, username: str, hashed_password: str):
        self.username = username
        self.hashed_password = hashed_password


class UserDataService:

    def load(self):
        try:
            users = open(os.getenv("PSG_USER_DATABASE_PATH"), "rb")
            all_users = pickle.load(users)
            users.close()
            return all_users
        except Exception as e:
            print(str(e))
            return {}


class UserRepository:
    __data_service: UserDataService

    def __init__(self, data_service):
        self.__data_service = data_service

    def find_by_username(self, username):
        users = self.__data_service.load()
        if username in users:
            return User(username, users[username])
        else:
            return None


class UserAuthenticator:

    def is_authentic(self, user: User, provided_password):
        return hash(provided_password.encode("utf-8")).digest() == user.hashed_password
