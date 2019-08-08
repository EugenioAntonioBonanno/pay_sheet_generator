import logging
import pickle
from pathlib import Path
from hashlib import sha256 as hash


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(message)s', level=logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(funcName)s:%(levelname)s:%(message)s')

file_handler = logging.FileHandler('logs.txt')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)

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
