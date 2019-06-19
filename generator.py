import os
import pickle
import logging
from pathlib import Path
from dateutil.rrule import rrule, DAILY
from dateutil.parser import parse
import openpyxl
from schedule_functions import find_month_length, format_sheet, write_schedule, get_days_missed, get_classes_subbed, \
    get_monthly_meeting
from user_functions import register_user, login_user, create_schedule, remove_class, add_class, view_schedule


root = Path(".")

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(message)s', level=logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(funcName)s:%(levelname)s:%(message)s')

file_handler = logging.FileHandler('logs.txt')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)


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
        register_user()
        break

    if user_choice.lower() == "login":
        active_user = login_user()

        while True:
            make_or_write = input("Enter 'set' create a new schedule, 'add' to add classes to your current one, "
                                  "'remove' to remove a class, 'view' to see your current schedule, or 'export' to "
                                  "create a copy of it: \n")
            logger.info(active_user + " has chosen the option: " + make_or_write)
            if make_or_write.lower() == "set":
                create_schedule(active_user, make_or_write)
            elif make_or_write.lower() == "add":
                add_class(active_user)
            elif make_or_write.lower() == "view":
                view_schedule(active_user)
            elif make_or_write.lower() == "export":
                users_object_path = root / "user_objects" / active_user
                schedule = open(users_object_path, "rb")
                users_schedule = pickle.load(schedule)
                break

            elif make_or_write.lower() == "remove":
                remove_class(active_user)

            else:
                logger.debug("Sorry that wasn't one of the options, please try again.")
                logger.info(active_user + " could not proceed with option  "+ make_or_write + " due to invalid input. ")

        year = "2019"

        while True:
            possible_months = ['01', '1', '2', '02', "3", '03', "4", '04', "5", '05', "6", '06', "7", '07', "8", '08',
                               "9", '09', "10", '11', '12']
            month = input("Please input a month as a numeric value [EX 4 for April]: \n")
            logger.info(active_user, 'set the month to', month, 'well making schedule.')
            if len(month) == 1:
                month = "0" + month
            if month in possible_months:
                break
            else:
                logger.debug("Sorry I can't make sense of what month you mean. Please try again.")
                logger.info(active_user + ' set the month to something that is not recognized as a month:'
                                          ' ' + month + ' well making schedule.')

        # Generates a list of user input representing days they missed work
        days_to_skip = get_days_missed(active_user)

        # Figures out how many days are in the month
        end = find_month_length(month, year)

        # Creates a list of all the days in the month
        date_range = list(rrule(DAILY, dtstart=parse("2019" + month + "01T090000"),
                                until=parse("2019" + month + end + "T090000")))
        days_to_schedule = list(filter(make_skipped_days_filter(days_to_skip), date_range))

        monthly_meeting = get_monthly_meeting(active_user)

        classes_subbed = get_classes_subbed(active_user)

        workbook = openpyxl.Workbook()

        sheet = format_sheet(workbook, active_user, month, year)

        # Writes users schedule to active sheet then saves workbook.
        sheet = write_schedule(days_to_schedule, sheet, users_schedule, monthly_meeting, classes_subbed)

        try:

            if not os.path.isdir("paysheets"):
                os.makedirs("paysheets")
            workbook.save(os.path.join('paysheets', active_user + "paysheet" + '.xlsx'))
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

