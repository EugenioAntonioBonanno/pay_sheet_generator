from typing import Optional

from dateutil.parser import parse
from dateutil.rrule import rrule, DAILY

from lib.generator import ExcelSheetGenerator
from lib.input_handler import CmdInputHandler, FakeInputHandler
from lib.logger import Logger
from lib.schedule import Schedule, ScheduleDataSource
from lib.user import User, UserAlreadyExistsException, UserDataSource, UserRegistrar, UserNotFoundException

LOGGER = Logger.get_logger(__name__)


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
            LOGGER.debug("Welcome %s.", self._active_user.name)
            LOGGER.info("%s has successfully logged in", self._active_user.name)
        except UserNotFoundException:
            LOGGER.debug("Sorry that information doesn't match our records. Please try again, or register new")
            self.register_or_login()

    def register(self):
        name = self._input_handler.retrieve_username()
        password = self._input_handler.retrieve_password()
        try:
            self._active_user = self._registrar.register(name, password)
        except UserAlreadyExistsException:
            LOGGER.debug("Sorry that name is already taken. Please try again")
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
        LOGGER.info("%s is about to view the day %s from their schedule", self._active_user.name, day_to_see)

        if day_to_see.lower() == 'done':
            return

        if day_to_see.lower() == 'all':
            users_schedule = self._schedule_ds.load_users_schedule(self._active_user)
            for weekday, sessions in users_schedule.week.items():
                for session in sessions:
                    LOGGER.debug("Day: %s session Code: %s session length: %s", weekday, session.code, session.length)
        else:
            users_schedule = self._schedule_ds.load_users_schedule(self._active_user)
            for weekday, sessions in users_schedule.week.items():
                if weekday != day_to_see:
                    continue
                for session in sessions:
                    LOGGER.debug("Day: %s session Code: %s session length: %s", weekday, session.code, session.length)

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
        month = self._input_handler.retrieve_month()
        LOGGER.info("%s set the month to %s well making schedule.", self._active_user.name, month)

        days_to_skip = self._input_handler.retrieve_missed_days()

        end = self._input_handler.find_month_length(month, year)

        # Creates a list of all the days in the month
        date_range = list(rrule(DAILY, dtstart=parse("2019" + month + "01T090000"),
                                until=parse("2019" + month + end + "T090000")))

        days_to_schedule = list(filter(make_skipped_days_filter(days_to_skip), date_range))

        monthly_meetings = self._input_handler.get_monthly_meetings()

        extra_sessions = self._input_handler.retrieve_extra_sessions()

        generator = ExcelSheetGenerator()
        sheet = generator.generate(self._active_user.name, month, year, users_schedule,
                                   days_to_schedule, monthly_meetings, extra_sessions)
        generator.export(sheet, self._active_user.name)

    def remove(self):
        sessions_to_remove = self._input_handler.retrieve_sessions()
        schedule = self._schedule_ds.load_users_schedule(self._active_user)
        schedule.remove_sessions(sessions_to_remove)
        self._schedule_ds.save_users_schedule(schedule, self._active_user)

    def done(self):  # pylint: disable=R0201
        exit("Program exited.")
