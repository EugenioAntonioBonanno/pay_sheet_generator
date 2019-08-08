import pickle
import logging
from lib.objects import Session, Day, User
from pathlib import Path

root = Path(".")

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(funcName)s:%(levelname)s:%(message)s")

file_handler = logging.FileHandler("logs.txt")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)


class ScheduleDataService:

    def create_object_path(self, active_user):

        users_object_path = root / "user_objects" / active_user

        return users_object_path

    def save_users_schedule(self, users_schedule, users_object_path, active_user):
        self._ensure_database_exists(active_user)

        schedule = open(users_object_path, "wb")
        pickle.dump(users_schedule, schedule)
        schedule.close()

        logger.debug("\nYour schedule has been successfully saved \n")
        logger.info(active_user + "has successfully saved their schedule.")

    def load_users_schedule(self, active_user):
        self._ensure_database_exists(active_user)

        users_object_path = self.create_object_path(active_user)
        schedule = open(users_object_path, "rb")
        users_schedule = pickle.load(schedule)
        schedule.close()

        return users_schedule

    def _ensure_database_exists(self, active_user):
        users_object_path = self.create_object_path(active_user)
        if self._schedule_database_exists(users_object_path):
            return
        self._create_user_database(users_object_path)

    def _schedule_database_exists(self, users_object_path):

        return Path(users_object_path).is_file()

    def _create_user_database(self, users_object_path):
        try:
            users = open(users_object_path, "wb")
            pickle.dump({}, users)
        except Exception as error:
            logger.error("database creation failed: " + str(error))
            raise ScheduleDataException("Sorry but database creation has failed.")


class ScheduleCreator:

    _schedule_data_service: ScheduleDataService

    def __init__(self, schedule_data_service):
        self._schedule_data_service = schedule_data_service


    def set_users_week(self, sessions):
        monday_sessions = []
        tuesday_sessions = []
        wednesday_sessions = []
        thursday_sessions = []
        friday_sessions = []

        for session in sessions:
            if session.day_taught == "1":
                monday_sessions.append(session)
            elif session.day_taught == "2":
                tuesday_sessions.append(session)
            elif session.day_taught == "3":
                wednesday_sessions.append(session)
            elif session.day_taught == "4":
                thursday_sessions.append(session)
            elif session.day_taught == "5":
                friday_sessions.append(session)

        week = []
        monday = Day("Monday", monday_sessions)
        week.append(monday)
        tuesday = Day("Tuesday", tuesday_sessions)
        week.append(tuesday)
        wednesday = Day("Wednesday", wednesday_sessions)
        week.append(wednesday)
        thursday = Day("Thursday", thursday_sessions)
        week.append(thursday)
        friday = Day("Friday", friday_sessions)
        week.append(friday)

        return week

    def create_user_object(self, active_user, week):

        users_schedule = User(active_user, week)

        return users_schedule

    def save_schedule(self, active_user, users_object_path, users_schedule):
        self._schedule_data_service.save_users_schedule(users_schedule, users_object_path, active_user)



class EditSchedule:

    _schedule_data_service: ScheduleDataService

    def __init__(self, schedule_data_service):
        self._schedule_data_service = schedule_data_service


    def save_schedule(self, active_user, users_object_path, users_schedule):
        self._schedule_data_service.save_users_schedule(users_schedule, users_object_path, active_user)



class ViewSchedule:

    __schedule_data_service: ScheduleDataService

    def __init__(self, schedule_data_service):
        self.__schedule_data_service = schedule_data_service

    def view_day(self, day_to_see, active_user):
        users_schedule = self.__schedule_data_service.load_users_schedule(active_user)


        to_view = []

        if day_to_see == "1":
            to_view.append("Monday")
        elif day_to_see == "2":
            to_view.append("Tuesday")
        elif day_to_see == "3":
            to_view.append("Wednesday")
        elif day_to_see == "4":
            to_view.append("Thursday")
        elif day_to_see == "5":
            to_view.append("Friday")
        elif day_to_see.lower() == "all":
            to_view = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        else:
            logger.debug("Sorry that isn't a valid option please try again")
            logger.info(active_user + "failed to view " + day_to_see + " from their schedule due to incorrect input")
            pass

        for day in users_schedule.week:
            if day.name in to_view:
                logger.debug("")
                for session in day.sessions:
                    logger.debug("Day: " + day.name + " session Code: " + session.code + " session length: "
                                 + session.length)
                logger.debug("")

class ScheduleDataException(Exception):
    pass



class CmdInputHandler:

    __schedule_data_service: ScheduleDataService

    def __init__(self, schedule_data_service):
        self._schedule_data_service = schedule_data_service

    def add_sessions(self, active_user):
        sessions = []
        logger.debug("\nPlease input your session info in EXACTLY the same format that will be described below: \n "
                     "[session (W55) length(in hours) day (as a num)]. \n"
                     "Days taught are entered as a number between 1-5 [1 = Monday 5 = Friday] \n"
                     "Use the following example to format your input: \"W60 1 3\".\n"
                     "The above means session W60, taught for one hour, on Wednesday \n"
                     "Do not include "" or a space before W in your input. \n")

        while True:
            session_info = input("Please input session information or type \"done\" if you are finished: \n")
            if session_info.lower() == "done":
                break
            else:
                try:
                    session_list = session_info.split()
                    if len(session_list) == 3:
                        sessions.append(Session(session_list[0], session_list[1], session_list[2]))
                        logger.debug("You have entered the following sessions:")
                        for session in sessions:
                            logger.debug(session.code + " day = " + session.day_taught)
                        logger.debug(" ")
                        logger.info(active_user + " added the session " + session_info + " to there schedule.")
                    else:
                        logger.debug("Sorry it seems the data you entered doesnt the required format. Please try again")
                        logger.info(active_user + "attempted to add the incorrect format: " + session_info +
                                    " to their schedule.")
                except:
                    logger.debug("Sorry it seems the data you entered doesnt the required format. Please try again")
                    logger.info(active_user + "attempted to add the incorrect format:" + session_info + ""
                                " to their schedule.")
        return sessions

    def add_sessions_to_user_schedule(self, active_user):
        sessions_to_add = []

        users_schedule = self._schedule_data_service.load_users_schedule(active_user)

        while True:

            session_to_add = input("Please enter the session you wish to add in the same format you see below. "
                                 "\"[session, length day]\" ex: W60 1 3. Or type \"done\": \n")

            if session_to_add.lower() == "done":
                break

            try:
                session_list = session_to_add.split()
                if len(session_list) == 3:
                    sessions_to_add.append(Session(session_list[0], session_list[1], session_list[2]))
                    logger.debug("You have entered the following sessions:", end=" ")
                    for session in sessions_to_add:
                        logger.debug(session.code, "day = " + session.day_taught, end=" ")
                    logger.debug("\n")
                    logger.info(active_user + "added the session", session_to_add, "to their schedule.")

                else:
                    logger.debug("Sorry it seems the data you entered doesnt match the required format. Please try again")
                    logger.info(active_user + "attempted to add incorrect input " + session_to_add + " to their schedule.")
            except:
                logger.debug("Sorry it seems the data you entered doesnt match the required format. Please try again")
                logger.info(active_user + " attempted to add incorrect input " + session_to_add + " to their schedule.")

        for add_session in sessions_to_add:
            for user_day in users_schedule.week:
                for user_session in user_day.sessions:
                    if user_session.day_taught == add_session.day_taught:
                        user_day.sessions.append(add_session)
                        break

        return users_schedule

    def remove_session(self, active_user):

        sessions_to_remove = []
        users_object_path = self._schedule_data_service.create_object_path(active_user)
        users_schedule = self._schedule_data_service.load_users_schedule(active_user)

        while True:

            session_to_remove = input("Please enter the session you wish to remove in the same format you entered it "
                                    "\"[session, length day]\" ex: W60 1 3. Or type \"done\": \n")

            if session_to_remove.lower() == "done":
                break

            try:
                session_list = session_to_remove.split()
                if len(session_list) == 3:
                    sessions_to_remove.append(Session(session_list[0], session_list[1], session_list[2]))
                    logger.debug("You have entered the following sessions:", end=" ")
                    for session in sessions_to_remove:
                        logger.debug(session.code, "day = " + session.day_taught, end=" ")
                    logger.debug("\n")
                    logger.info(active_user + "removed the session" + session_to_remove + " from their schedule.")
                else:
                    logger.debug("Sorry it seems the data you entered doesnt match the required format. Please try again")
                    logger.info(active_user + "attempted to removed the session via incorrect input " + session_to_remove +
                                " from their schedule.")
            except:
                logger.debug("Sorry it seems the data you entered doesnt match the required format. Please try again")
                logger.info(active_user + "attempted to removed the session via incorrect input" + session_to_remove +
                            " from their schedule.")

        for day in users_schedule.week:
            for user_session in day.sessions:
                for delete_session in sessions_to_remove:
                    if user_session.code == delete_session.code and user_session.length == delete_session.length \
                            and user_session.day_taught == delete_session.day_taught:
                        day.sessions.remove(user_session)

        self._schedule_data_service.save_users_schedule(users_schedule, users_object_path, active_user)