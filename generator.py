import openpyxl
from hashlib import sha256 as hash
import pickle
from dateutil.rrule import *
from dateutil.parser import *
from sessions_and_days import mon, wed, fri
from functions import find_month_length, format_sheet, write_schedule
from datetime import *

# Code to write to or edit a excel file. Currently under development.


year = "2019"
month = input("Please input a month as a numeric value [ie 04 for April]")


end = find_month_length(month, year)

to_schedule = list(rrule(DAILY, dtstart=parse("2019" + month + "01T090000"), until=parse("2019" + month + end + "T090000")))

workbook = openpyxl.Workbook()

sheet = format_sheet(workbook, month, year)

sheet = write_schedule(to_schedule, sheet, mon, wed, fri)


workbook.save('paysheet.xlsx')








