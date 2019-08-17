import pickle
import os
from pathlib import Path
from openpyxl.styles import Font
from lib.logger import Logger

root = Path(".")

logger = Logger.get_logger(__name__)


class ScheduleDataSource:
    def save_users_schedule(self, schedule, active_user):
        users_object_path = ScheduleDataSource._create_user_object_path(active_user)
        self._ensure_database_exists(active_user)
        schedule_file = open(users_object_path, "wb")
        pickle.dump(schedule, schedule_file)
        schedule_file.close()
        logger.debug("\nYour schedule has been successfully saved \n")
        logger.info(active_user + "has successfully saved their schedule.")

    def load_users_schedule(self, active_user):
        self._ensure_database_exists(active_user)

        users_object_path = ScheduleDataSource._create_user_object_path(active_user)
        schedule = open(users_object_path, "rb")
        users_schedule = pickle.load(schedule)
        schedule.close()

        return users_schedule

    def _ensure_database_exists(self, active_user):
        if self._schedule_database_exists(active_user):
            return
        self._create_user_database(active_user)

    @staticmethod
    def _create_user_object_path(active_user):
        return root / "user_objects" / active_user

    @staticmethod
    def _schedule_database_exists(active_user):
        return Path(ScheduleDataSource._create_user_object_path(active_user)).is_file()

    @staticmethod
    def _create_user_database(active_user):
        try:
            users = open(ScheduleDataSource._create_user_object_path(active_user), "wb")
            pickle.dump({}, users)
        except Exception as error:
            logger.error("database creation failed: " + str(error))
            raise ScheduleDataException("Sorry but database creation has failed.")


class ScheduleFormatter:

    def create_schedule(self, workbook):
        sheet = workbook.active
        sheet.title = "Paysheet"
        return sheet

    def format_schedule(self, sheet, active_user, month, year):
        sheet.merge_cells("C1:G2")
        sheet.column_dimensions["A"].width = 6
        sheet.column_dimensions["F"].width = 6
        sheet.column_dimensions["B"].width = 17
        sheet.column_dimensions["G"].width = 17
        sheet.column_dimensions["E"].width = 5
        sheet["C1"] = active_user.title() + "\"s " + "Paysheet: " + month + "/" + year
        font_obj = Font(name="Times New Roman", bold=True, size=20, italic=True)
        sheet["C1"].font = font_obj
        return sheet

    def label_schedule(self, sheet):
        sheet["A3"] = "Date"
        sheet["B3"] = "session name"
        sheet["C3"] = "Length"
        sheet["D3"] = "Signature"
        sheet["F3"] = "Date"
        sheet["G3"] = "session name"
        sheet["H3"] = "Length"
        sheet["I3"] = "Signature"
        return sheet


class ScheduleWriter:

    _schedule_data_service: ScheduleDataSource

    def __init__(self, schedule_data_service):
        self._schedule_data_service = schedule_data_service

    def write_sessions(self, to_schedule, sheet, users_schedule, monthly_meetings, extra_sessions_worked):
        col = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        col_index = 0
        row_index = 4

        for day in to_schedule:
            day_and_month = str(day.month) + "/" + str(day.day)

            if day.weekday() == 0:
                [sheet, row_index, col_index] = self.write_day(users_schedule, row_index, col_index, day_and_month, sheet, col,
                                                               day="Monday")

            elif day.weekday() == 1:
                [sheet, row_index, col_index] = self.write_day(users_schedule, row_index, col_index, day_and_month, sheet, col,
                                                               day="Tuesday")

            elif day.weekday() == 2:
                [sheet, row_index, col_index] = self.write_day(users_schedule, row_index, col_index, day_and_month, sheet, col,
                                                               day="Wednesday")

            elif day.weekday() == 3:
                [sheet, row_index, col_index] = self.write_day(users_schedule, row_index, col_index, day_and_month, sheet, col,
                                                               day="Thursday")

            elif day.weekday() == 4:
                [sheet, row_index, col_index] = self.write_day(users_schedule, row_index, col_index, day_and_month, sheet, col,
                                                               day="Friday")
            elif day.weekday() == 5:
                [sheet, row_index, col_index] = self.write_day(users_schedule, row_index, col_index, day_and_month, sheet, col,
                                                               day="Saturday")
            elif day.weekday() == 4:
                [sheet, row_index, col_index] = self.write_day(users_schedule, row_index, col_index, day_and_month, sheet, col,
                                                               day="Sunday")

            if str(day.day) in monthly_meetings:
                [sheet, row_index, col_index] = self.write_monthly_meeting(sheet, col, col_index, row_index, day_and_month)

            if len(extra_sessions_worked) > 0:
                [sheet, row_index, col_index] = self.write_extra_sessions(extra_sessions_worked, day, sheet, col,
                                                                          col_index, row_index, day_and_month)
        return sheet

    def write_day(self, schedule, row_index, col_index, day_and_month, sheet, col, day="Monday"):
        for weekday, sessions in schedule.week.items():
            for session in sessions:
                if weekday == day:
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

    def write_monthly_meeting(self, sheet, col, col_index, row_index, day_and_month):
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

        return [sheet, row_index, col_index]

    def write_extra_sessions(self, extra_sessions_worked, day, sheet, col, col_index, row_index, day_and_month):
        for worked in extra_sessions_worked:
            if int(worked.date) == int(day.day):
                sheet[col[col_index] + str(row_index)] = day_and_month
                col_index += 1
                sheet[col[col_index] + str(row_index)] = worked.code
                col_index += 1
                sheet[col[col_index] + str(row_index)] = worked.length
                col_index += 3

                if col_index == 5:
                    pass
                else:
                    col_index = 0
                    row_index += 1

        return [sheet, row_index, col_index]

    def export_schedule(self, workbook, active_user):

        if not os.path.isdir("paysheets"):
            os.makedirs("paysheets")
        workbook.save(os.path.join('paysheets', active_user + "paysheet" + '.xlsx'))


class Schedule:

    def __init__(self):
        self.week = {
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
        }

    def add_sessions(self, sessions):
        for session in sessions:
            if session.day_taught == "monday" or session.day_taught == "1":
                self.week["Monday"].append(session)
            elif session.day_taught == "tuesday" or session.day_taught == "2":
                self.week["Tuesday"].append(session)
            elif session.day_taught == "wednesday" or session.day_taught == "3":
                self.week["Wednesday"].append(session)
            elif session.day_taught == "thursday" or session.day_taught == "4":
                self.week["Thursday"].append(session)
            elif session.day_taught == "friday" or session.day_taught == "5":
                self.week["Friday"].append(session)
        return self

    def remove_sessions(self, sessions):
        for sessionToRemove in sessions:
            for weekday in self.week:
                if sessionToRemove.day_taught != weekday:
                    continue
                self.week[weekday].remove(sessionToRemove)


class ScheduleDataException(Exception):
    pass

