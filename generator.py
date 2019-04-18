import openpyxl
from hashlib import sha256 as hash
import pickle
from dateutil.rrule import *
from dateutil.parser import *
from sessions_and_days import mon, wed, fri
from functions import find_month_length, format_sheet, write_schedule, get_days_missed
from datetime import *


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



workbook.save('paysheet.xlsx')








