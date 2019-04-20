from openpyxl.styles import Font
from objects import Day, User, Session
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
def write_schedule(to_schedule, sheet, users_schedule, days_to_skip):
    col = ["A", 'B', "C", "D", "E", "F", "G", "H", "I"]

    col_index = 0
    row_index = 4

    for day in users_schedule.week:
        for session in day.sessions:
            if day.name == "Monday":
                print(session.code)

    for day in to_schedule:
        day_and_month = str(day.month) + '/' + str(day.day)

        if day.day in days_to_skip:
            pass
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
    return sheet


# Uses a while true loop to allow users to build a list of any days they missed work.
def get_days_missed():
    days_to_skip = []

    while True:
        print("Enter any days you missed work due to sickness or holiday as a number. [ex '12']")
        print("Or enter 'end' if you've either missed no days or have entered all the ones you missed")
        print("Your current missed days are as follows:", days_to_skip)
        missed_work = input(":")
        if missed_work.lower() == 'end':
            break
        else:
            days_to_skip.append(int(missed_work))

    return days_to_skip


def create_schedule(active_user):
    sessions = []
    while True:
        session_id = input("Please input the id for this class ex F60: \n")
        length = input("Please input its length in hours such as 1 or .5: \n")
        day_taught = input("Please tell me the day you teach this class as a number. [ Ex 1 = Monday ]: \n")
        sessions.append(Session(session_id, length, day_taught))
        print(sessions)
        add_another = input("Enter 'add' to add another class or 'done' if you have created all your classes: \n")

        if add_another.lower() == 'done':
            print(sessions)
            break

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


