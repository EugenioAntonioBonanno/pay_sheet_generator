import pickle
from hashlib import sha256 as sha256hash
from pathlib import Path

import config
from lib.logger import Logger

LOGGER = Logger.get_logger(__name__)


class User:
    name: str
    hashed_password: str

    def __init__(self, name: str, hashed_password: str):
        self.name = name
        self.hashed_password = hashed_password


class UserDataSource:
    def all(self):
        self.__ensure_database_exists()
        try:
            users = open(config.USER_DB_PATH, "rb")
            all_users = pickle.load(users)
            users.close()
            return all_users
        except Exception as e:
            print(str(e))
            return {}

    def load_by_username(self, username):
        all_users = self.all()
        if username in all_users:
            return User(username, all_users[username])
        else:
            return None

    def save_user(self, user: User):
        self.__ensure_database_exists()
        try:
            users = open(config.USER_DB_PATH, "rb")
            all_users = pickle.load(users)
            users.close()

            all_users[user.name] = user.hashed_password
            users = open(config.USER_DB_PATH, "wb")
            pickle.dump(all_users, users)
            users.close()

        except Exception as error:
            LOGGER.error("database creation failed: " + str(error))
            raise UserDataSourceException("Sorry but we cannot currently access the database.")

    def username_exists(self, new_user):
        self.__ensure_database_exists()
        try:
            users = open(config.USER_DB_PATH, "rb")
            all_users = pickle.load(users)
            return new_user in all_users

        except Exception as error:
            LOGGER.error("database creation failed: " + error)
            raise UserDataSourceException("Sorry but we cannot currently access the database.")

    @staticmethod
    def __ensure_database_exists():
        if UserDataSource.__user_database_exists():
            return
        UserDataSource.__create_user_database()

    @staticmethod
    def __user_database_exists():
        return Path(config.USER_DB_PATH).is_file()

    @staticmethod
    def __create_user_database():
        try:
            users = open(config.USER_DB_PATH, "wb")
            pickle.dump({}, users)
        except Exception as error:
            LOGGER.error("database creation failed: " + error)
            raise UserDataSourceException("Sorry but database creation has failed.")


class UserDataSourceException(Exception):
    pass


class UserRegistrar:
    __user_ds: UserDataSource

    def __init__(self, user_ds: UserDataSource):
        self.__user_ds = user_ds

    def register(self, name, password):
        user_exists = self.__user_ds.username_exists(name)
        if user_exists:
            raise UserAlreadyExistsException("user %s already exists".format(name))

        user = User(name, password)
        self.__user_ds.save_user(user)
        return user

    def login(self, credentials):
        current_user = self.__user_ds.load_by_username(credentials["name"])

        if current_user is None:
            raise UserNotFoundException("user %s not found".format(credentials["name"]))

        if not sha256hash(credentials["password"].encode("utf-8")).digest() == current_user.hashed_password:
            raise CredentialsMismatchException("passwords did not match")

        return current_user


class UserAlreadyExistsException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class CredentialsMismatchException(Exception):
    pass
