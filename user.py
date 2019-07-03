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


class UserDataService:

    def load(self):
        self.__ensure_database_exists()
        try:
            users = open(users_info_path, "rb")
            all_users = pickle.load(users)
            users.close()
            return all_users
        except Exception as e:
            print(str(e))
            return {}

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

    def check_if_user_unique(self, new_user):
        self.__ensure_database_exists()
        try:
            users = open(users_info_path, "rb")
            all_users = pickle.load(users)
            if new_user in all_users:
                return False
            else:
                return True
        except Exception as error:
            logger.error("database creation failed: " + error)
            raise UserDataServiceException("Sorry but we cannot currently access the database.")

    def ensure_passwords_match(self, password_1, password_2):
        return password_1 == password_2


    def __ensure_database_exists(self):
        if self.__user_database_exists():
            return
        self.__create_user_database()

    def __user_database_exists(self):

        return Path(users_info_path).is_file()

    def __create_user_database(self):
        try:
            users = open(users_info_path, "wb")
            pickle.dump({}, users)
        except Exception as error:
            logger.error("database creation failed: " + error)
            raise UserDataServiceException("Sorry but database creation has failed.")


class UserDataServiceException(Exception):
    pass


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

    def register_user(self, user: User):
       self.__data_service.save_user(user)


class UserAuthenticator:

    def is_authentic(self, user: User, provided_password):
        return hash(provided_password.encode("utf-8")).digest() == user.hashed_password



