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

    def retrieve_sessions(self, active_user):
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
                    else:
                        logger.debug("Sorry it seems the data you entered doesnt the required format. Please try again")
                except:
                    logger.debug("Sorry it seems the data you entered doesnt the required format. Please try again")
        return sessions
