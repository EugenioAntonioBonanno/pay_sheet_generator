import openpyxl
from hashlib import sha256 as hash
import pickle
from dateutil.rrule import *
from dateutil.parser import *
from sessions_and_days import mon, wed, fri
from functions import find_month_length
from datetime import *

# Code to write to or edit a excel file. Currently under development.


# year = input("Please input the year as a numeric value [ie 2019]")
month = input("Please input a month as a numeric value [ie 04 for April]")


end = find_month_length(month)


time = list(rrule(DAILY, dtstart=parse("2019" + month + "01T090000"), until=parse("2019" + month + end + "T090000")))


workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Paysheet"
sheet.column_dimensions["B"].width = 20
sheet["A1"] = "Date"
sheet["B1"] = "Class name"
sheet["C1"] = "Length"
# sheet['A4'] = "Regular start time"


col = ["A", 'B', "C", "D", "E"]
col_index = 0
row_index = 2

for date in time:
    day_and_month = str(date.month) + '/' + str(date.day)
    if date.weekday() == 0:
        schedule = mon
        for session in schedule:
            sheet[col[col_index] + str(row_index)] = day_and_month
            col_index += 1
            sheet[col[col_index] + str(row_index)] = session.code
            col_index += 1
            sheet[col[col_index] + str(row_index)] = session.length
            col_index += 1
            # sheet[col[col_index] + str(row_index)] = session.time
            col_index += 1
            col_index = 0
            row_index += 1
    elif date.weekday() == 2:
        schedule = wed
        for session in schedule:
            sheet[col[col_index] + str(row_index)] = day_and_month
            col_index += 1
            sheet[col[col_index] + str(row_index)] = session.code
            col_index += 1
            sheet[col[col_index] + str(row_index)] = session.length
            col_index += 1
            # sheet[col[col_index] + str(row_index)] = session.time
            col_index += 1
            col_index = 0
            row_index += 1
    elif date.weekday() == 4:
        schedule = fri
        for session in schedule:
            sheet[col[col_index] + str(row_index)] = day_and_month
            col_index += 1
            sheet[col[col_index] + str(row_index)] = session.code
            col_index += 1
            sheet[col[col_index] + str(row_index)] = session.length
            col_index += 1
            # sheet[col[col_index] + str(row_index)] = session.time
            col_index += 1
            col_index = 0
            row_index += 1

workbook.save('paysheet.xlsx')








