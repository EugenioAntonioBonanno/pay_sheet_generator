import openpyxl
from typing import Optional
from dateutil.rrule import rrule, DAILY
from dateutil.parser import parse

from lib.input_handler import CmdInputHandler, FakeInputHandler
from lib.logger import Logger
from lib.monthly_variables import MonthSpecificData
from lib.schedule import ScheduleFormatter, ScheduleWriter, Schedule, ScheduleDataSource
from lib.user import User, UserAlreadyExistsException, UserDataSource, UserRegistrar, UserNotFoundException

logger = Logger.get_logger(__name__)


class ApplicationFactory:

    @staticmethod
    def make():
        schedule_data_source = ScheduleDataSource()
        input_handler = CmdInputHandler()
        user_data_source = UserDataSource()
        user_registrar = UserRegistrar(user_data_source)
        return Application(user_registrar,
                           input_handler,
                           schedule_data_source)

    @staticmethod
    def mock():
        schedule_data_source = ScheduleDataSource()
        input_handler = FakeInputHandler()
        user_data_source = UserDataSource()
        user_registrar = UserRegistrar(user_data_source)
        return Application(user_registrar,
                           input_handler,
                           schedule_data_source)


class Application:
    _active_user: Optional[User]

    _registrar: UserRegistrar
    _input_handler: CmdInputHandler
    _schedule_ds: ScheduleDataSource

    def __init__(self, registrar: UserRegistrar, input_handler: CmdInputHandler, schedule_ds: ScheduleDataSource):
        self._registrar = registrar
        self._input_handler = input_handler
        self._schedule_ds = schedule_ds
        self._active_user = None

    def run(self):
        self.register_or_login()
        while True:
            action = self._input_handler.retrieve_action()
            getattr(self, action)()

    def register_or_login(self):
        if self._active_user is None:
            user_choice = self._input_handler.register_or_login()
            getattr(self, user_choice)()

    def login(self):
        credentials = self._input_handler.retrieve_credentials()
        try:
            self._active_user = self._registrar.login(credentials)
            logger.debug("Welcome " + self._active_user.name + ".")
            logger.info(self._active_user.name + " has successfully logged in")
        except UserNotFoundException:
            logger.debug("Sorry that information doesn't match our records. Please try again, or register new")
            self.register_or_login()

    def register(self):
        name = self._input_handler.retrieve_username()
        password = self._input_handler.retrieve_password()
        try:
            self._active_user = self._registrar.register(name, password)
        except UserAlreadyExistsException:
            logger.debug("Sorry that name is already taken. Please try again")
            self.register_or_login()

    def add(self):
        sessions_to_add = self._input_handler.retrieve_sessions()
        schedule = self._schedule_ds.load_users_schedule(self._active_user)
        schedule.add_sessions(sessions_to_add)
        self._schedule_ds.save_users_schedule(schedule, self._active_user)

    def new(self):
        sessions = self._input_handler.retrieve_sessions()
        schedule = Schedule().add_sessions(sessions)
        self._schedule_ds.save_users_schedule(schedule, self._active_user)

    def view(self):
        day_to_see = self._input_handler.retrieve_day_to_view()
        logger.info(self._active_user.name + " is about to view the day " + day_to_see + " from their schedule")

        if day_to_see.lower() == 'done':
            return
        elif day_to_see.lower() == 'all':
            users_schedule = self._schedule_ds.load_users_schedule(self._active_user)
            for weekday, sessions in users_schedule.week.items():
                for session in sessions:
                    logger.debug("Day: " + weekday + " session Code: " + session.code + " session length: "
                                 + session.length)
                logger.debug("")
        else:
            users_schedule = self._schedule_ds.load_users_schedule(self._active_user)
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
        users_schedule = self._schedule_ds.load_users_schedule(self._active_user)
        while True:
            possible_months = ['01', '1', '2', '02', "3", '03', "4", '04', "5", '05', "6", '06', "7", '07', "8", '08',
                               "9", '09', "10", '11', '12']
            month = input("Please input a month as a numeric value [EX 4 for April]: \n")
            logger.info(self._active_user.name + ' set the month to ' + month + ' well making schedule.')
            if len(month) == 1:
                month = "0" + month
            if month in possible_months:
                break
            else:
                logger.debug("Sorry I can't make sense of what month you mean. Please try again.")
                logger.info(self._active_user.name + ' set the month to something that is not recognized as a month:'
                                                     ' ' + month + ' well making schedule.')

        days_to_skip = MonthSpecificData().get_days_missed(self._active_user)

        end = MonthSpecificData().find_month_length(month, year)

        # Creates a list of all the days in the month
        date_range = list(rrule(DAILY, dtstart=parse("2019" + month + "01T090000"),
                                until=parse("2019" + month + end + "T090000")))

        days_to_schedule = list(filter(make_skipped_days_filter(days_to_skip), date_range))

        monthly_meetings = MonthSpecificData().get_monthly_meetings()

        extra_sessions_worked = MonthSpecificData().get_extra_session_worked(self._active_user)

        workbook = openpyxl.Workbook()

        sheet = ScheduleFormatter().create_schedule(workbook)

        sheet = ScheduleFormatter().format_schedule(sheet, self._active_user, month, year)

        sheet = ScheduleFormatter().label_schedule(sheet)

        # Writes users schedule to active sheet then saves workbook.
        sheet = ScheduleWriter(self._schedule_ds).write_sessions(days_to_schedule, sheet, users_schedule,
                                                                 monthly_meetings, extra_sessions_worked)

        try:
            ScheduleWriter(self._schedule_ds).export_schedule(workbook, self._active_user)
            logger.debug("Your Paysheet has been created and saved and should be available in a folder name 'paysheets'"
                         " located inside the folder containing this program.")
            logger.info(self._active_user.name + ' successfully generated a paysheet.')
        except:
            logger.debug("An error occurred when attempting to save your Paysheet. Make sure no spreadsheets are "
                         "currently open. If they are close them, and then retry well paying careful attention to "
                         "the on screen instructions.")
            logger.info(self._active_user.name + ' encountered an error well generating a paysheet.')

    def remove(self):
        sessions_to_remove = self._input_handler.retrieve_sessions()
        schedule = self._schedule_ds.load_users_schedule(self._active_user)
        schedule.remove_sessions(sessions_to_remove)
        self._schedule_ds.save_users_schedule(schedule, self._active_user)

    def done(self):
        exit("Program exited.")
