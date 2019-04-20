import openpyxl
from hashlib import sha256 as hash
import pickle
from dateutil.rrule import *
from dateutil.parser import *
from sessions_and_days import mon, wed, fri
from schedule_functions import find_month_length, format_sheet, write_schedule, get_days_missed
from user_functions import register_user, login_user
from objects import Session, Day, User
from datetime import *


user_choice = input("Hello, please enter your username to login, or type 'register' to register: ")

if user_choice.lower() == 'register':
    register_user()

if user_choice.lower() == "login":
    active_user = login_user()






    make_or_write = input("Do you want to set a new schedule of print your current one?")


    sessions = []
    while True:
        session_id = input("Please input the id for this class ex F60: \n")
        length = input("Please input its length in hours such as 1 or .5: \n")
        day_taught = input("Please tell me the day you teach this class as a number. Ex 1 = Monday")
        sessions.append(Session(session_id, length, day_taught))
        add_another = input("Enter 'add' to add another class or 'done' if you have created all your classes: \n")

        if add_another.lower() == 'done':
            print(sessions)
            break

    monday_sessions= []
    tuesday_sessions = []
    wednesday_sessions = []
    thursday_sessions = []
    friday_sessions = []

    for session in sessions:
        if session.day_taught == 1:
            monday_sessions.append(session)
        elif session.day_taught == 2:
            tuesday_sessions.append(session)
        elif session.day_taught == 3:
            wednesday_sessions.append(session)
        elif session.day_taught == 4:
            thursday_sessions.append(session)
        elif session.day_taught == 5:
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

    users_schedule = User(active_user, week)

    #for day in users_schedule.week:














# Allows the user to set the year and month they want a schedule created for.
year = "2019"
month = input("Please input a month as a numeric value [ie 04 for April] \n:")

# Generates a list of user input representing days they missed work
days_to_skip = get_days_missed()


# Figures out how many days are in the month
end = find_month_length(month, year)

# Creates a list of all the days in the month
to_schedule = list(rrule(DAILY, dtstart=parse("2019" + month + "01T090000"), until=parse("2019" + month + end + "T090000")))

# Creates excel workbook
workbook = openpyxl.Workbook()


# Formats the currently active sheet
sheet = format_sheet(workbook, month, year)

# Writes users schedule to active sheet then saves workbook.
sheet = write_schedule(to_schedule, sheet, mon, wed, fri, days_to_skip)



try:
    workbook.save('paysheet.xlsx')
    print("Your Paysheet has been created and saved and should be available in the same directly as this program")
except:
    print("An error occurred when attempting to save your Paysheet. Make sure no spreadsheets are currently open."
          "If they are close them, and then retry, well paying careful attention to the on screen instructions.")










