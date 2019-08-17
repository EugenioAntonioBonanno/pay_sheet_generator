import getpass
import pickle
import logging

from lib.monthly_variables import MonthSpecificData
from lib.objects import Session
from pathlib import Path

from lib.schedule_exporter import ScheduleFormatter, ScheduleWriter
from lib.user import UserDataSource, User, UserAuthenticator
from dateutil.rrule import rrule, DAILY
from dateutil.parser import parse
from hashlib import sha256 as hash
import openpyxl


root = Path(".")

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(funcName)s:%(levelname)s:%(message)s")

file_handler = logging.FileHandler("logs.txt")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)

class CmdInputHandler:
    available_user_choices = ["register", "login"]

    available_actions = ["new", "add", "edit", "export", "view", "remove", "done"]

    username_input_message = """
    Please input your desired user name:
    """

    action_input_message = """
    Enter 'new' create a new schedule, 'add' to add sessions to your current one,
    remove' to remove a session, 'view' to see your current schedule, or 'export' to
    create a copy of it:
    """

    sessions_help = """
    Please input your session info in EXACTLY the same format that will be described below:
    [session (W55) length(in hours) day (as a num)].
    Days taught are entered as a number between 1-5 [1 = Monday 5 = Friday]
    Use the following example to format your input: "W60 1 3"
    The above means session W60, taught for one hour, on Wednesday
    Do not include "" or a space before W in your input.
    """

    sessions_input_message = """
    Please input session information or type "done" if you are finished:
    """

    view_day_input_message = """
    Please enter the day you wish to view, enter "all" to see your entire
    schedule or "done" to exit.
    """

    def retrieve_user_choice(self):
        user_choice_known = False
        while not user_choice_known:
            user_choice = input("Hello, please enter 'login' to login, or type 'register' to create an account:\n")
            logger.info("A user entered: " + user_choice)
            user_choice_known = user_choice in self.available_user_choices

    def retrieve_password(self):
        while True:
            password_1 = getpass.getpass("Please enter your password:\n")
            password_1 = hash(password_1.encode("utf-8")).digest()
            password_2 = getpass.getpass("Please enter it one more time:\n")
            password_2 = hash(password_2.encode("utf-8")).digest()
            if password_1 == password_2:
                return password_1
            else:
                logger.debug("Sorry your passwords don't match.")

    def retrieve_username(self):
        return input(self.username_input_message).lower()

    def retrieve_action(self):
        action_known = False
        while not action_known:
            action = input(self.action_input_message).lower()
            action_known = action in self.available_actions
            if not action_known:
                logger.debug("Sorry that wasn't one of the options, please try again.")
                logger.info("Could not proceed with option  " + action + " due to invalid input.")
        return action

    def retrieve_sessions(self):
        sessions = []
        logger.debug(self.sessions_help)

        while True:
            session_info = input(self.sessions_input_message).lower()
            if session_info == "done":
                return sessions

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

    def retrieve_credentials(self):
        name = input("Please enter your user name:\n").lower()
        password = getpass.getpass("Please enter your password:\n")
        return {"name": name, "password": password}

    def retrieve_day_to_view(self):
        return input(self.view_day_input_message).lower()


class ScheduleDataSource:
    def save_users_schedule(self, schedule, active_user):
        users_object_path = ScheduleDataSource._create_user_object_path(active_user)
        self._ensure_database_exists(active_user)
        schedule_file = open(users_object_path, "wb")
        pickle.dump(schedule, schedule_file)
        schedule_file.close()
        logger.debug("\nYour schedule has been successfully saved \n")
        logger.info(active_user + "has successfully saved their schedule.")

    def load_users_schedule(self, active_user):
        self._ensure_database_exists(active_user)

        users_object_path = ScheduleDataSource._create_user_object_path(active_user)
        schedule = open(users_object_path, "rb")
        users_schedule = pickle.load(schedule)
        schedule.close()

        return users_schedule

    def _ensure_database_exists(self, active_user):
        if self._schedule_database_exists(active_user):
            return
        self._create_user_database(active_user)

    @staticmethod
    def _create_user_object_path(active_user):
        return root / "user_objects" / active_user

    @staticmethod
    def _schedule_database_exists(active_user):
        return Path(ScheduleDataSource._create_user_object_path(active_user)).is_file()

    @staticmethod
    def _create_user_database(active_user):
        try:
            users = open(ScheduleDataSource._create_user_object_path(active_user), "wb")
            pickle.dump({}, users)
        except Exception as error:
            logger.error("database creation failed: " + str(error))
            raise ScheduleDataException("Sorry but database creation has failed.")


class Controller:
    __active_user: User
    __input_handler: CmdInputHandler
    __user_ds: UserDataSource
    __schedule_ds: ScheduleDataSource

    def __init__(self, active_user: User, input_handler: CmdInputHandler, user_repo: UserDataSource, schedule_ds: ScheduleDataSource):
        __active_user = active_user
        __input_handler = input_handler
        __user_repo = user_repo
        __schedule_ds = schedule_ds

    def execute(self, action):
        getattr(self, action)()

    def add(self):
        sessions_to_add = self.__input_handler.retrieve_sessions()
        schedule = self.__schedule_ds.load_users_schedule(self.__active_user)
        schedule.add_sessions(sessions_to_add)
        self.__schedule_ds.save_users_schedule(schedule, self.__active_user)

    def new(self):
        sessions = self.__input_handler.retrieve_sessions()
        schedule = Schedule().add_sessions(sessions)
        self.__schedule_ds.save_users_schedule(schedule, self.__active_user)

    def view(self):
        day_to_see = self.__input_handler.retrieve_day_to_view()
        logger.info(self.__active_user + " is about to view the day " + day_to_see + " from their schedule")

        if day_to_see.lower() == 'done':
            return
        else:
            users_schedule = self.__schedule_ds.load_users_schedule(self.__active_user)
            for weekday, sessions in users_schedule.week.items():
                if weekday != day_to_see:
                    continue
                for session in sessions:
                    logger.debug("Day: " + weekday + " session Code: " + session.code + " session length: "
                                 + session.length)
                logger.debug("")

    def export(self):
        def make_skipped_days_filter(skipped_days):
            def sick_days_filter(day):
                if day.day in skipped_days:
                    return False
                else:
                    return True
            return sick_days_filter

        year = "2019"
        users_schedule =self.__schedule_ds.load_users_schedule(self.__active_user)
        while True:
            possible_months = ['01', '1', '2', '02', "3", '03', "4", '04', "5", '05', "6", '06', "7", '07', "8", '08',
                               "9", '09', "10", '11', '12']
            month = input("Please input a month as a numeric value [EX 4 for April]: \n")
            logger.info(self.__active_user + ' set the month to ' + month + ' well making schedule.')
            if len(month) == 1:
                month = "0" + month
            if month in possible_months:
                break
            else:
                logger.debug("Sorry I can't make sense of what month you mean. Please try again.")
                logger.info(self.__active_user + ' set the month to something that is not recognized as a month:'
                                          ' ' + month + ' well making schedule.')

        days_to_skip = MonthSpecificData().get_days_missed(self.__active_user)

        end = MonthSpecificData().find_month_length(month, year)

        # Creates a list of all the days in the month
        date_range = list(rrule(DAILY, dtstart=parse("2019" + month + "01T090000"),
                                until=parse("2019" + month + end + "T090000")))

        days_to_schedule = list(filter(make_skipped_days_filter(days_to_skip), date_range))

        monthly_meetings = MonthSpecificData().get_monthly_meetings(self.__active_user)

        extra_sessions_worked = MonthSpecificData().get_extra_session_worked(self.__active_user)

        workbook = openpyxl.Workbook()

        sheet = ScheduleFormatter().create_schedule(workbook)

        sheet = ScheduleFormatter().format_schedule(sheet, self.__active_user, month, year)

        sheet = ScheduleFormatter().label_schedule(sheet)

        # Writes users schedule to active sheet then saves workbook.
        sheet = ScheduleWriter(self.__schedule_ds).write_sessions(days_to_schedule, sheet, users_schedule,
                                                           monthly_meetings, extra_sessions_worked)

        try:
            ScheduleWriter(self.__schedule_ds).export_schedule(workbook, self.__active_user)
            logger.debug("Your Paysheet has been created and saved and should be available in a folder name 'paysheets'"
                         " located inside the folder containing this program.")
            logger.info(self.__active_user + ' successfully generated a paysheet.')
        except:
            logger.debug("An error occurred when attempting to save your Paysheet. Make sure no spreadsheets are "
                         "currently open. If they are close them, and then retry well paying careful attention to "
                         "the on screen instructions.")
            logger.info(self.__active_user + ' encountered an error well generating a paysheet.')

    def remove(self):
        sessions_to_remove = self.__input_handler.retrieve_sessions()
        schedule = self.__schedule_ds.load_users_schedule(self.__active_user)
        schedule.remove_sessions(sessions_to_remove)
        self.__schedule_ds.save_users_schedule(schedule, self.__active_user)

    def done(self):
        exit("Program exited.")


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


class Schedule:

    def __init__(self):
        self.week = {
            "monday": [],
            "tuesday": [],
            "wednesday": [],
            "thursday": [],
            "friday": [],
        }

    def add_sessions(self, sessions):
        for session in sessions:
            if session.day_taught == "monday":
                self.week["monday"].append(session)
            elif session.day_taught == "tuesday":
                self.week["tuesday"].append(session)
            elif session.day_taught == "wednesday":
                self.week["wednesday"].append(session)
            elif session.day_taught == "thursday":
                self.week["thursday"].append(session)
            elif session.day_taught == "friday":
                self.week["friday"].append(session)
        return self

    def remove_sessions(self, sessions):
        for sessionToRemove in sessions:
            for weekday in self.week:
                if sessionToRemove.day_taught != weekday:
                    continue
                self.week[weekday].remove(sessionToRemove)


class ScheduleDataException(Exception):
    pass

