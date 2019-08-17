import pickle
from pathlib import Path
from hashlib import sha256 as hash

from lib.application import CmdInputHandler
from lib.logger import Logger

logger = Logger.get_logger(__name__)

root = Path(".")

users_info_path = root / "user_info" / "users"


class User:
    username: str
    hashed_password: str

    def __init__(self, username: str, hashed_password: str):
        self.username = username
        self.hashed_password = hashed_password


class UserDataSource:
    def all(self):
        self.__ensure_database_exists()
        try:
            users = open(users_info_path, "rb")
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
            users = open(users_info_path, "rb")
            all_users = pickle.load(users)
            users.close()

            all_users[user.username] = user.hashed_password
            users = open(users_info_path, "wb")
            pickle.dump(all_users, users)
            users.close()

        except Exception as error:
            logger.error("database creation failed: " + str(error))
            raise UserDataServiceException("Sorry but we cannot currently access the database.")

    def username_exists(self, new_user):
        self.__ensure_database_exists()
        try:
            users = open(users_info_path, "rb")
            all_users = pickle.load(users)
            return not new_user in all_users

        except Exception as error:
            logger.error("database creation failed: " + error)
            raise UserDataServiceException("Sorry but we cannot currently access the database.")

    @staticmethod
    def __ensure_database_exists():
        if UserDataSource.__user_database_exists():
            return
        UserDataSource.__create_user_database()

    @staticmethod
    def __user_database_exists():
        return Path(users_info_path).is_file()

    @staticmethod
    def __create_user_database():
        try:
            users = open(users_info_path, "wb")
            pickle.dump({}, users)
        except Exception as error:
            logger.error("database creation failed: " + error)
            raise UserDataServiceException("Sorry but database creation has failed.")


class UserDataServiceException(Exception):
    pass


class UserAuthenticator:
    def is_authentic(self, user: User, provided_password):
        return hash(provided_password.encode("utf-8")).digest() == user.hashed_password


class UserRegistrar:
    __input_handler: CmdInputHandler
    __user_ds: UserDataSource

    def __init__(self, input_handler: CmdInputHandler, user_ds: UserDataSource):
        self.__input_handler = input_handler
        self.__user_ds = user_ds

    def register(self):
        new_user = self.__input_handler.retrieve_username()
        user_exists = self.__user_ds.username_exists(new_user)
        while user_exists:
            logger.debug("Sorry that name is already taken. Please try again")
            new_user = self.__input_handler.retrieve_username()
            user_exists = self.__user_ds.username_exists(new_user)
        password = self.__input_handler.retrieve_password()
        user = User(new_user, password)
        self.__user_ds.save_user(user)
        return user

    def login(self):
        is_authenticated = False
        while not is_authenticated:
            credentials = self.__input_handler.retrieve_credentials()
            current_user = self.__user_ds.load_by_username(credentials["name"])

            if current_user is None:
                logger.debug("Sorry but that user doesn't exist")
                break

            is_authenticated = UserAuthenticator().is_authentic(current_user, credentials["password"])
            if is_authenticated:
                active_user = current_user.username
                logger.debug("Welcome " + active_user + ".")
                logger.info(active_user + " has successfully logged in")
                return active_user
            else:
                logger.debug(
                    "Sorry that information doesn't match our records. Please try again, or register a new account")

