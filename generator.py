import openpyxl
import pickle
from dateutil.rrule import *
from dateutil.parser import *
from schedule_functions import find_month_length, format_sheet, write_schedule, get_days_missed, create_schedule
from user_functions import register_user, login_user



user_choice = input("Hello, please enter 'login' to login, or type 'register' to register: \n ")

if user_choice.lower() == 'register':
    register_user()

if user_choice.lower() == "login":
    active_user = login_user()

    make_or_write = input("Enter 'set' to set your schedule, or 'export' to create a copy of it: \n ")

    if make_or_write.lower() == "set":
        create_schedule(active_user)
    elif make_or_write.lower() == "export":
        schedule = open(active_user, 'rb')
        users_schedule = pickle.load(schedule)
        schedule.close()

        # Allows the user to set the year and month they want a schedule created for.
        year = "2019"
        month = input("Please input a month as a numeric value [ie 04 for April]: \n")

        # Generates a list of user input representing days they missed work
        days_to_skip = get_days_missed()

        # Figures out how many days are in the month
        end = find_month_length(month, year)

        # Creates a list of all the days in the month
        to_schedule = list(
            rrule(DAILY, dtstart=parse("2019" + month + "01T090000"), until=parse("2019" + month + end + "T090000")))

        # Creates excel workbook
        workbook = openpyxl.Workbook()

        # Formats the currently active sheet
        sheet = format_sheet(workbook, active_user, month, year)

        # Writes users schedule to active sheet then saves workbook.
        sheet = write_schedule(to_schedule, sheet, users_schedule, days_to_skip)

        try:
            workbook.save('paysheet.xlsx')
            print("Your Paysheet has been created and saved and should be available in the same directly as this program")
        except:
            print("An error occurred when attempting to save your Paysheet. Make sure no spreadsheets are currently open."
                  "If they are close them, and then retry well paying careful attention to the on screen instructions.")



























