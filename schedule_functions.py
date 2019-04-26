from openpyxl.styles import Font
from objects import SubbedSession


# Takes in a month an year and returns how many days that month will have in it.
def find_month_length(month, year):
    if month in ["01", "03", "05", "07", "08", "10"]:
        length = "31"
    elif month in ["04", "06", "09", "11", "12"]:
        length = "30"
    else:
        if int(year) % 4 == 0:
            length = 29
        else:
            length = 28
    return length


# Sets up a excel sheet to fit users schedule. Adds titles.
def format_sheet(workbook, active_user, month, year):
    sheet = workbook.active
    font_obj = Font(name="Times New Roman", bold=True, size=20, italic=True)
    sheet.title = "Paysheet"
    sheet.merge_cells("C1:G2")
    sheet.column_dimensions["A"].width = 6
    sheet.column_dimensions["F"].width = 6
    sheet.column_dimensions["B"].width = 17
    sheet.column_dimensions['G'].width = 17
    sheet.column_dimensions["E"].width = 5

    sheet["C1"] = active_user.title() + "'s " + "Paysheet: " + month + "/" + year
    sheet['C1'].font = font_obj

    sheet["A3"] = "Date"
    sheet["B3"] = "Class name"
    sheet["C3"] = "Length"
    sheet["D3"] = "Signature"
    sheet["F3"] = "Date"
    sheet['G3'] = "Class name"
    sheet['H3'] = "Length"
    sheet['I3'] = "Signature"
    return sheet


# Writes users schedule across 8 cells before dropping down one row.
def write_schedule(to_schedule, sheet, users_schedule, days_to_skip, monthly_meeting, classes_subbed):
    col = ["A", 'B', "C", "D", "E", "F", "G", "H", "I"]
    col_index = 0
    row_index = 4

    for day in to_schedule:
        day_and_month = str(day.month) + '/' + str(day.day)
        skip = False

        if day.day in days_to_skip:
            skip = True

        elif day.weekday() == 0:
            schedule = users_schedule.week
            for weekday in schedule:
                for session in weekday.sessions:
                    if weekday.name == "Monday":
                        sheet[col[col_index] + str(row_index)] = day_and_month
                        col_index += 1
                        sheet[col[col_index] + str(row_index)] = session.code
                        col_index += 1
                        sheet[col[col_index] + str(row_index)] = session.length
                        col_index += 3

                        if col_index == 5:
                            pass
                        else:
                            col_index = 0
                            row_index += 1

        elif day.weekday() == 1:
            schedule = users_schedule.week
            for weekday in schedule:
                for session in weekday.sessions:
                    if weekday.name == "Tuesday":
                        sheet[col[col_index] + str(row_index)] = day_and_month
                        col_index += 1
                        sheet[col[col_index] + str(row_index)] = session.code
                        col_index += 1
                        sheet[col[col_index] + str(row_index)] = session.length
                        col_index += 3

                        if col_index == 5:
                            pass
                        else:
                            col_index = 0
                            row_index += 1
        elif day.weekday() == 2:
            schedule = users_schedule.week
            for weekday in schedule:
                for session in weekday.sessions:
                    if weekday.name == "Wednesday":
                        sheet[col[col_index] + str(row_index)] = day_and_month
                        col_index += 1
                        sheet[col[col_index] + str(row_index)] = session.code
                        col_index += 1
                        sheet[col[col_index] + str(row_index)] = session.length
                        col_index += 3

                        if col_index == 5:
                            pass
                        else:
                            col_index = 0
                            row_index += 1

        elif day.weekday() == 3:
            schedule = users_schedule.week
            for weekday in schedule:
                for session in weekday.sessions:
                    if weekday.name == "Thursday":
                        sheet[col[col_index] + str(row_index)] = day_and_month
                        col_index += 1
                        sheet[col[col_index] + str(row_index)] = session.code
                        col_index += 1
                        sheet[col[col_index] + str(row_index)] = session.length
                        col_index += 3

                        if col_index == 5:
                            pass
                        else:
                            col_index = 0
                            row_index += 1

        elif day.weekday() == 4:
            schedule = users_schedule.week
            for weekday in schedule:
                for session in weekday.sessions:
                    if weekday.name == "Friday":
                        sheet[col[col_index] + str(row_index)] = day_and_month
                        col_index += 1
                        sheet[col[col_index] + str(row_index)] = session.code
                        col_index += 1
                        sheet[col[col_index] + str(row_index)] = session.length
                        col_index += 3

                        if col_index == 5:
                            pass
                        else:
                            col_index = 0
                            row_index += 1
        if skip:
            pass
        else:
            if int(day.day) == int(monthly_meeting):
                sheet[col[col_index] + str(row_index)] = day_and_month
                col_index += 1
                sheet[col[col_index] + str(row_index)] = "Meeting"
                col_index += 1
                sheet[col[col_index] + str(row_index)] = "1"
                col_index += 3

                if col_index == 5:
                    pass
                else:
                    col_index = 0
                    row_index += 1

            if len(classes_subbed) > 0:
                for subbed in classes_subbed:
                    if int(subbed.date) == int(day.day):
                        sheet[col[col_index] + str(row_index)] = day_and_month
                        col_index += 1
                        sheet[col[col_index] + str(row_index)] = subbed.code
                        col_index += 1
                        sheet[col[col_index] + str(row_index)] = subbed.length
                        col_index += 3

                        if col_index == 5:
                            pass
                        else:
                            col_index = 0
                            row_index += 1

    return sheet






# Uses a while true loop to allow users to build a list of any days they missed work.
def get_days_missed():
    days_to_skip = []
    print("Enter any days you missed work due to sickness or holiday as a number. [ex '12'] for the 12th or enter 'done'. \n")
    while True:

        print("Your current missed days are as follows:", days_to_skip)
        missed_work = input("Enter a missed day as a number or 'done' to move on. \n")
        if missed_work.lower() == 'done':
            break
        else:
            days_to_skip.append(int(missed_work))

    return days_to_skip

def get_classes_subbed():
    classes_subbed = []
    while True:

        subbed = input("Have you subbed any classes this month? \nInput 'done' if you haven't.\n"
                   "If you have enter it in the following format [class id, length , date] \n"
                   "ex: W34 2 13 :\n")

        if subbed.lower() == 'done':
            break
        else:
            subbed = subbed.split()
            classes_subbed.append(SubbedSession(subbed[0], subbed[1], subbed[2]))

    return classes_subbed

def get_monthly_meeting():
    meeting = input("Did you have a meeting this month? If yes enter the date as a number \n"
                       "or enter 'no':\n")
    if meeting.lower() == "no":
        return 100
    else:
        return meeting


