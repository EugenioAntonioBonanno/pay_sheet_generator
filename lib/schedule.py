import pickle
import os
from pathlib import Path

import config
from lib.logger import Logger
from lib.user import User

LOGGER = Logger.get_logger(__name__)


class ScheduleDataSource:
    def save_users_schedule(self, schedule, user: User):
        ScheduleDataSource._ensure_database_exists(user)
        schedule_db = open(ScheduleDataSource._get_user_schedule_path(user), "wb")
        pickle.dump(schedule, schedule_db)
        schedule_db.close()
        LOGGER.debug("\nYour schedule has been successfully saved \n")
        LOGGER.info(user.name + "has successfully saved their schedule.")

    def load_users_schedule(self, user: User):
        ScheduleDataSource._ensure_database_exists(user)
        schedule_db = open(ScheduleDataSource._get_user_schedule_path(user), "rb")
        schedule = pickle.load(schedule_db)
        schedule_db.close()
        return schedule

    @staticmethod
    def _ensure_database_exists(user: User):
        if ScheduleDataSource._schedule_database_exists(user):
            return
        ScheduleDataSource._create_user_database(user)

    @staticmethod
    def _get_user_schedule_path(user: User):
        return os.path.join(config.USER_SCHEDULES_DIR, user.name)

    @staticmethod
    def _schedule_database_exists(user: User):
        return Path(ScheduleDataSource._get_user_schedule_path(user)).is_file()

    @staticmethod
    def _create_user_database(user: User):
        try:
            users = open(ScheduleDataSource._get_user_schedule_path(user), "wb")
            pickle.dump({}, users)
        except Exception as error:
            LOGGER.error("database creation failed: " + str(error))
            raise ScheduleDataException("Sorry but database creation has failed.")


class Schedule:

    def __init__(self):
        self.week = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
        }

    def add_sessions(self, sessions):
        for session in sessions:
            if session.day == "monday" or session.day == "1":
                self.week["Monday"].append(session)
            elif session.day == "tuesday" or session.day == "2":
                self.week["Tuesday"].append(session)
            elif session.day == "wednesday" or session.day == "3":
                self.week["Wednesday"].append(session)
            elif session.day == "thursday" or session.day == "4":
                self.week["Thursday"].append(session)
            elif session.day == "friday" or session.day == "5":
                self.week["Friday"].append(session)
        return self

    def remove_sessions(self, sessions):
        for sessionToRemove in sessions:
            for weekday in self.week:
                if sessionToRemove.day != weekday:
                    continue
                self.week[weekday].remove(sessionToRemove)


class ScheduleDataException(Exception):
    pass


class Session:
    def __init__(self, code, length, day):
        self.code = code
        self.length = length
        self.day = day

    def __eq__(self, other):
        return isinstance(other, Session) \
               and self.code == other.code \
               and self.length == other.length \
               and self.day == other.day


class ExtraSession:
    def __init__(self, code, length, date):
        self.code = code
        self.length = length
        self.date = date