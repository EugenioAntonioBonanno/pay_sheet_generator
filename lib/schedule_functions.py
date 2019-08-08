from openpyxl.styles import Font
from lib.objects import SubbedSession
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(funcName)s:%(levelname)s:%(message)s")

file_handler = logging.FileHandler("logs.txt")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)


# Takes in a month an year and returns how many days that month will have in it.
def find_month_length(month, year):
    if month in ["01", "1" "03", "3", "05", "5", "07", "7", "08", "8", "10"]:
        length = "31"
    elif month in ["04", "4", "06", "6", "09", "9", "11", "12"]:
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
    sheet.column_dimensions["G"].width = 17
    sheet.column_dimensions["E"].width = 5

    sheet["C1"] = active_user.title() + "\"s " + "Paysheet: " + month + "/" + year
    sheet["C1"].font = font_obj

    sheet["A3"] = "Date"
    sheet["B3"] = "session name"
    sheet["C3"] = "Length"
    sheet["D3"] = "Signature"
    sheet["F3"] = "Date"
    sheet["G3"] = "session name"
    sheet["H3"] = "Length"
    sheet["I3"] = "Signature"
    return sheet


# Writes users schedule across 8 cells before dropping down one row.
def write_schedule(to_schedule, sheet, users_schedule, monthly_meeting, sessions_subbed):
    col = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    col_index = 0
    row_index = 4

    for day in to_schedule:
        day_and_month = str(day.month) + "/" + str(day.day)

        if day.weekday() == 0:
            [sheet, row_index, col_index] = write_day(users_schedule, row_index, col_index, day_and_month, sheet, col,
                                                      day="Monday")

        elif day.weekday() == 1:
            [sheet, row_index, col_index] = write_day(users_schedule, row_index, col_index, day_and_month, sheet, col,
                                                      day="Tuesday")

        elif day.weekday() == 2:
            [sheet, row_index, col_index] = write_day(users_schedule, row_index, col_index, day_and_month, sheet, col,
                                                      day="Wednesday")

        elif day.weekday() == 3:
            [sheet, row_index, col_index] = write_day(users_schedule, row_index, col_index, day_and_month, sheet, col,
                                                      day="Thursday")

        elif day.weekday() == 4:
            [sheet, row_index, col_index] = write_day(users_schedule, row_index, col_index, day_and_month, sheet, col,
                                                      day="Friday")

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

        if len(sessions_subbed) > 0:
            for subbed in sessions_subbed:
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
def get_days_missed(active_user):
    days_to_skip = []
    logger.debug("Enter any days you missed work due to sickness or holiday as a number. "
                 "[ex \"12\"] for the 12th or enter \"done\". \n")

    while True:

        logger.debug("Your current missed days are as follows: ")
        for day in days_to_skip:
            logger.debug(str(day))

        missed_work = input("Enter a missed day as a number or \"done\" to move on. \n")
        logger.info(active_user + " added " + missed_work + " to their list of days they did not work ")
        logger.info((active_user + " entered:" + missed_work))
        if missed_work.lower() == "done":
            break
        else:
            days_to_skip.append(int(missed_work))

    return days_to_skip


def get_sessions_subbed(active_user):
    sessions_subbed = []
    logger.debug(("\nHave you subbed any sessions this month? \nInput \"done\" if you haven\"t or when finished entering"
                  " those you have.\n"
                  "If you have enter each session one at a time in the following format [session id length date] \n"
                  "ex: W34 2 13."))
    while True:
        logger.debug("Your current list of sessions you have subbed this month is as follows:")
        for session in sessions_subbed:
            logger.debug(session.code + " ")
        logger.debug("\n")
        subbed = input("Enter a session to add to your subbed sessions, or \"done\" if you are finished:\n")
        logger.info((active_user + " entered:" + subbed))
        if subbed.lower() == "done":
            break
        else:
            try:
                subbed = subbed.split(" ")
                sessions_subbed.append(SubbedSession(subbed[0], subbed[1], subbed[2]))
                logger.info(active_user + " added " + subbed + "to their list of sessions they subbed.")
            except:
                logger.debug("Sorry but you entered that session in incorrectly, it won\"t be added. Please try again")

    return sessions_subbed


def get_monthly_meeting(active_user):
    meeting = input("Did you have a meeting this month? If yes enter the day of the meeting as a number [ex 5th = 5] \n"
                    "or enter \"done\" to create a schedule with no monthly meeting added:\n")
    logger.info(active_user + " to their monthly meeting as " + meeting + ".")
    if meeting.lower() == "done":
        return 100
    else:
        return meeting


def write_day(users_schedule, row_index, col_index, day_and_month, sheet, col, day="Monday"):
    schedule = users_schedule.week
    for weekday in schedule:
        for session in weekday.sessions:
            if weekday.name == day:
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
    return [sheet, row_index, col_index]
