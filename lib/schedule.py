import pickle
import os
from pathlib import Path
from openpyxl.styles import Font

import config
from lib.logger import Logger
from lib.user import User

logger = Logger.get_logger(__name__)


class ScheduleDataSource:
    def save_users_schedule(self, schedule, active_user):
        users_object_path = ScheduleDataSource._create_user_object_path(active_user)
        self._ensure_database_exists(active_user)
        schedule_file = open(users_object_path, "wb")
        pickle.dump(schedule, schedule_file)
        schedule_file.close()
        logger.debug("\nYour schedule has been successfully saved \n")
        logger.info(active_user.name + "has successfully saved their schedule.")

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
    def _create_user_object_path(active_user: User):
        return os.path.join(config.user_schedules_dir, active_user.name)

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
        sheet["C1"] = active_user.name.title() + "\"s " + "Paysheet: " + month + "/" + year
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
                [sheet, row_index, col_index] = self.write_day(users_schedule, row_index, col_index, day_and_month,
                                                               sheet, col,
                                                               day="Monday")

            elif day.weekday() == 1:
                [sheet, row_index, col_index] = self.write_day(users_schedule, row_index, col_index, day_and_month,
                                                               sheet, col,
                                                               day="Tuesday")

            elif day.weekday() == 2:
                [sheet, row_index, col_index] = self.write_day(users_schedule, row_index, col_index, day_and_month,
                                                               sheet, col,
                                                               day="Wednesday")

            elif day.weekday() == 3:
                [sheet, row_index, col_index] = self.write_day(users_schedule, row_index, col_index, day_and_month,
                                                               sheet, col,
                                                               day="Thursday")

            elif day.weekday() == 4:
                [sheet, row_index, col_index] = self.write_day(users_schedule, row_index, col_index, day_and_month,
                                                               sheet, col,
                                                               day="Friday")
            elif day.weekday() == 5:
                [sheet, row_index, col_index] = self.write_day(users_schedule, row_index, col_index, day_and_month,
                                                               sheet, col,
                                                               day="Saturday")
            elif day.weekday() == 4:
                [sheet, row_index, col_index] = self.write_day(users_schedule, row_index, col_index, day_and_month,
                                                               sheet, col,
                                                               day="Sunday")

            if str(day.day) in monthly_meetings:
                [sheet, row_index, col_index] = self.write_monthly_meeting(sheet, col, col_index, row_index,
                                                                           day_and_month)

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
        if not os.path.isdir(config.pay_sheet_export_dir):
            os.makedirs(config.pay_sheet_export_dir)
        workbook.save(os.path.join(config.pay_sheet_export_dir, active_user.name + "_paysheet" + '.xlsx'))


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
            if session.day == "monday" or session.day == "1":
                self.week["Monday"].append(session)
            elif session.day == "tuesday" or session.day == "2":
                self.week["Tuesday"].append(session)
            elif session.day == "wednesday" or session.day == "3":
                self.week["Wednesday"].append(session)
            elif session.day == "thursday" or session.day == "4":
                self.week["Thursday"].append(session)
            elif session.day == "friday" or session.day == "5":
                self.week["Friday"].append(session)
        return self

    def remove_sessions(self, sessions):
        for sessionToRemove in sessions:
            for weekday in self.week:
                if sessionToRemove.day != weekday:
                    continue
                self.week[weekday].remove(sessionToRemove)


class ScheduleDataException(Exception):
    pass


class Session:
    def __init__(self, code, length, day):
        self.code = code
        self.length = length
        self.day = day

    def __eq__(self, other):
        return isinstance(other, Session) \
               and self.code == other.code \
               and self.length == other.length \
               and self.day == other.day
