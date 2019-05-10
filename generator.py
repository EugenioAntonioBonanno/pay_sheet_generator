import openpyxl, os
import pickle
from dateutil.rrule import *
from dateutil.parser import *
from schedule_functions import find_month_length, format_sheet, write_schedule, get_days_missed, get_classes_subbed, get_monthly_meeting
from user_functions import register_user, login_user, create_schedule
from pathlib import Path


root = Path(".")


def get_sick_days_filter(edays_to_skip):
    def sick_days_filter(day):
        if day.day in edays_to_skip:
            return False
        else:
            return True
    return sick_days_filter


while True:
    user_choice = input("Hello, please enter 'login' to login, or type 'register' to create an account: \n ")

    if user_choice.lower() == 'register':
        register_user()
        break

    if user_choice.lower() == "login":
        active_user = login_user()

        while True:
            make_or_write = input("Enter 'set' to set your schedule, or 'export' to create a copy of it: \n")
            if make_or_write.lower() == "set":
                create_schedule(active_user)
                break
            elif make_or_write.lower() == "export":
                users_object_path = root / "user_objects" / active_user

                schedule = open(users_object_path, 'rb')
                users_schedule = pickle.load(schedule)
                schedule.close()
                break
            else:
                print("Sorry that wasn't one of the options, please try again.")


        year = "2019"

        while True:
            possible_months = ['01', '1', '2', '02', "3", '03', "4", '04', "5", '05', "6", '06', "7", '07', "8", '08', "9", '09', "10", '11', '12']
            month = input("Please input a month as a numeric value [EX 4 for April]: \n")
            if len(month) == 1:
                month = "0" + month
            if month in possible_months:
                break
            else:
                print("Sorry I can't make sense of what month you mean. Please try again.")

        # Generates a list of user input representing days they missed work
        days_to_skip = get_days_missed()

        # Figures out how many days are in the month
        end = find_month_length(month, year)

        # Creates a list of all the days in the month
        date_range = list(rrule(DAILY, dtstart=parse("2019" + month + "01T090000"), until=parse("2019" + month + end + "T090000")))
        to_schedule = list(filter(get_sick_days_filter(days_to_skip), date_range))

        monthly_meeting = get_monthly_meeting()

        classes_subbed = get_classes_subbed()

        workbook = openpyxl.Workbook()

        sheet = format_sheet(workbook, active_user, month, year)

        # Writes users schedule to active sheet then saves workbook.
        sheet = write_schedule(to_schedule, sheet, users_schedule, days_to_skip, monthly_meeting, classes_subbed)

        try:

            if not os.path.isdir("paysheets"):
                os.makedirs("paysheets")


            workbook.save(os.path.join('paysheets', active_user + "paysheet" + '.xlsx'))
            print("Your Paysheet has been created and saved and should be available in a folder name 'paysheets' located inside the folder containing this program.")
            break
        except:
            print("An error occurred when attempting to save your Paysheet. Make sure no spreadsheets are currently open. "
                  "If they are close them, and then retry well paying careful attention to the on screen instructions.")
            break

    else:
        print("Sorry but I can understand what you want to do, please try again")

























