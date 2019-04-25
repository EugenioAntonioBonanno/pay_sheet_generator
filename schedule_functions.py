from openpyxl.styles import Font
from objects import Day, User, Session, SubbedSession
import pickle


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
def write_schedule(to_schedule, sheet, users_schedule, days_to_skip, monthly_meeting):
    col = ["A", 'B', "C", "D", "E", "F", "G", "H", "I"]
    col_index = 0
    row_index = 4

    for day in to_schedule:
        day_and_month = str(day.month) + '/' + str(day.day)

        if day.day in days_to_skip:
            pass

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

        if day.weekday() == 0:
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

def get_days_subbed():
    while True:
        classes_subbed = []

        subbed = input("Have you subbed any classes this month? \n input 'done' if you haven't\n"
                   " If you have enter it in the following format [class id, length , date] \n"
                   "ex: W34 2 13 :/n")
        if subbed.lower() == 'done':
            break
        else:
            class_subbed = subbed.split()
            classes_subbed.append(SubbedSession(class_subbed[0], class_subbed[1], class_subbed[2]))

    return classes_subbed

# Prompts a user for information that can be used to create Session objects representing the classes taught.
def create_schedule(active_user):
    sessions = []
    print("\nPlease input your class info in EXACTLY the same format that will be described below: \n"
          "[class (W55) length(in hours) day (as a num)]. \n"
          "Days taught are entered as a number between 1-5 [1 = Monday 5 = Friday] \n"
          "Use the following example to format your input: 'W60 1 3'.\n"
          "The above means class W60, taught for one hour, on Wednesday \n"
          "Do not include '' or a space before W in your input. \n")
    while True:
        session_info = input("Please input class information or type 'done' if you are finished: \n")
        if session_info.lower() == "done":
            break
        else:
            session_list = session_info.split()
            sessions.append(Session(session_list[0], session_list[1], session_list[2]))
            print("You have entered the following classes:", end=" ")
            for session in sessions:
                print(session.code, "day = ", session.day_taught, end=" ")
            print("\n")

    monday_sessions = []
    tuesday_sessions = []
    wednesday_sessions = []
    thursday_sessions = []
    friday_sessions = []

    for session in sessions:
        if session.day_taught == '1':
            monday_sessions.append(session)
        elif session.day_taught == '2':
            tuesday_sessions.append(session)
        elif session.day_taught == '3':
            wednesday_sessions.append(session)
        elif session.day_taught == '4':
            thursday_sessions.append(session)
        elif session.day_taught == '5':
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

    schedule = open(active_user, "wb")
    pickle.dump(users_schedule, schedule)
    schedule.close()


