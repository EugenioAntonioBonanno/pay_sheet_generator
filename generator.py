import getpass
import logging
import openpyxl
from pathlib import Path
from dateutil.rrule import rrule, DAILY
from dateutil.parser import parse
from hashlib import sha256 as hash
from lib.user import UserDataService, UserAuthenticator, UserRepository, User
from lib.schedule_exporter import ScheduleFormatter, ScheduleWriter
from lib.monthly_variables import MonthSpecificData
from lib.schedule_data import ScheduleCreator, ScheduleDataService, EditSchedule, ViewSchedule, CmdInputHandler


logger = logging.getLogger(__name__)
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(funcName)s:%(levelname)s:%(message)s")

file_handler = logging.FileHandler("logs.txt")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)


root = Path(".")
user_database_path = root / "user_info" / "users"


#if os.getenv("PSG_USER_DATABASE_PATH") == "":
    #logger.debug("Please export the user database path to environment as 'PSG_USER_DATABASE_PATH'")
    #sys.exit(1)


def make_skipped_days_filter(skipped_days):
    def sick_days_filter(day):
        if day.day in skipped_days:
            return False
        else:
            return True
    return sick_days_filter


while True:
    user_choice = input("Hello, please enter 'login' to login, or type 'register' to create an account: \n ")
    logger.info("A user entered: " + user_choice)

    if user_choice.lower() == 'register':
        new_user = input("Please input your desired user name:\n")
        advance = UserDataService().username_exists(new_user)

        if advance:
            password_1 = getpass.getpass("Hello " + new_user + " please create your password: \n ")
            password_1 = hash(password_1.encode("utf-8"))
            password_2 = getpass.getpass("please enter it one more time: \n ")
            password_2 = hash(password_2.encode("utf-8"))
            passwords_match = UserDataService().ensure_passwords_match(password_1.digest(), password_2.digest())

            if passwords_match:
                UserDataService().save_user(User(new_user, password_2.digest()))
                logger.debug(new_user + " has been saved. GREAT SUCCESS!")
                break
            else:
                logger.debug("Sorry your passwords don't match.")

        else:
            logger.debug("Sorry that name is already taken. Please try again")

    if user_choice.lower() == "login":
        is_authenticated = False
        while not is_authenticated:
            name = input("Please enter your user name:\n")
            password = getpass.getpass("Please enter your password:\n")

            current_user = UserRepository(UserDataService()).find_by_username(name)

            if current_user is None:
                logger.debug("Sorry but that user doesn't exist")
                break

            is_authenticated = UserAuthenticator().is_authentic(current_user, password)
            if is_authenticated:
                active_user = current_user.username
                logger.debug("Welcome " + name + ".")
                logger.info(active_user + " has successfully logged in")
            else:
                logger.debug(
                    "Sorry that information doesn't match our records. Please try again, or register a new account")

        schedule_ds = ScheduleDataService()
        input_handler = CmdInputHandler()
        while True:
            make_or_write = input("Enter 'set' create a new schedule, 'add' to add sessions to your current one, "
                                  "'remove' to remove a session, 'view' to see your current schedule, or 'export' to "
                                  "create a copy of it: \n")
            logger.info(active_user + " has chosen the option: " + make_or_write)
            if make_or_write.lower() == "set":
                sessions = input_handler.retrieve_sessions(active_user)
                week = ScheduleCreator(schedule_ds).set_users_week(sessions)
                users_schedule = ScheduleCreator(schedule_ds).create_user_object(active_user, week)
                schedule_ds.save_users_schedule(users_schedule, schedule_ds.create_object_path(active_user), active_user)

            elif make_or_write.lower() == "add":
                users_schedule = schedule_ds.load_users_schedule(active_user)

                sessions_to_add = input_handler.retrieve_sessions(active_user)
                for add_session in sessions_to_add:
                    for user_day in users_schedule.week:
                        for user_session in user_day.sessions:
                            if user_session.day_taught == add_session.day_taught:
                                user_day.sessions.append(add_session)
                                break
                EditSchedule(schedule_ds).save_schedule(active_user, root / "user_objects"
                                                                  / active_user, users_schedule)
            elif make_or_write.lower() == "view":
                day_to_see = input("Please enter the day you wish to view as a number, enter \"all\" to see your entire"
                                   " schedule or \"done\" to exit. \n [1 = Monday 5 = Friday]:\n")
                logger.info(active_user + " is about to view the day " + day_to_see + " from their schedule")

                if day_to_see.lower() == 'done':
                    break
                else:
                    ViewSchedule(schedule_ds).view_day(day_to_see, active_user)


            elif make_or_write.lower() == "export":
                users_schedule = schedule_ds.load_users_schedule(active_user)
                break

            elif make_or_write.lower() == "remove":
                users_schedule = schedule_ds.load_users_schedule(active_user)
                sessions_to_remove = input_handler.remove_session(active_user)
                for day in users_schedule.week:
                    for user_session in day.sessions:
                        for delete_session in sessions_to_remove:
                            if user_session.code == delete_session.code \
                                    and user_session.length == delete_session.length \
                                    and user_session.day_taught == delete_session.day_taught:
                                day.sessions.remove(user_session)

                EditSchedule(schedule_ds).save_schedule(active_user, root / "user_objects"
                                                        / active_user, users_schedule)

            else:
                logger.debug("Sorry that wasn't one of the options, please try again.")
                logger.info(active_user + " could not proceed with option  " + make_or_write + " due to invalid input.")

        year = "2019"

        while True:
            possible_months = ['01', '1', '2', '02', "3", '03', "4", '04', "5", '05', "6", '06', "7", '07', "8", '08',
                               "9", '09', "10", '11', '12']
            month = input("Please input a month as a numeric value [EX 4 for April]: \n")
            logger.info(active_user + ' set the month to ' + month + ' well making schedule.')
            if len(month) == 1:
                month = "0" + month
            if month in possible_months:
                break
            else:
                logger.debug("Sorry I can't make sense of what month you mean. Please try again.")
                logger.info(active_user + ' set the month to something that is not recognized as a month:'
                                          ' ' + month + ' well making schedule.')

        days_to_skip = MonthSpecificData().get_days_missed(active_user)

        end = MonthSpecificData().find_month_length(month, year)

        # Creates a list of all the days in the month
        date_range = list(rrule(DAILY, dtstart=parse("2019" + month + "01T090000"),
                                until=parse("2019" + month + end + "T090000")))

        days_to_schedule = list(filter(make_skipped_days_filter(days_to_skip), date_range))

        monthly_meetings = MonthSpecificData().get_monthly_meetings(active_user)

        extra_sessions_worked = MonthSpecificData().get_extra_session_worked(active_user)

        workbook = openpyxl.Workbook()

        sheet = ScheduleFormatter().create_schedule(workbook)

        sheet = ScheduleFormatter().format_schedule(sheet, active_user, month, year)

        sheet = ScheduleFormatter().label_schedule(sheet)

        # Writes users schedule to active sheet then saves workbook.
        sheet = ScheduleWriter(schedule_ds).write_sessions(days_to_schedule, sheet, users_schedule,
                                                monthly_meetings, extra_sessions_worked)

        try:
            ScheduleWriter(schedule_ds).export_schedule(workbook, active_user)
            logger.debug("Your Paysheet has been created and saved and should be available in a folder name 'paysheets'"
                         " located inside the folder containing this program.")
            logger.info(active_user + ' successfully generated a paysheet.')

            break
        except:
            logger.debug("An error occurred when attempting to save your Paysheet. Make sure no spreadsheets are "
                         "currently open. If they are close them, and then retry well paying careful attention to "
                         "the on screen instructions.")
            logger.info(active_user + ' encountered an error well generating a paysheet.')
            exit()

    else:
        logger.debug("Sorry but I can understand what you want to do, please try again")

