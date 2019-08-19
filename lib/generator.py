import os

from openpyxl import Workbook
from openpyxl.styles import Font

import config
from lib.logger import Logger

LOGGER = Logger.get_logger(__name__)


class ExcelSheetGenerator:
    weekdays_map = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday",
    }

    def _create_preformatted_workbook(self, user_name, month, year):
        workbook = Workbook()
        workbook.active.title = "Paysheet"
        workbook.active.merge_cells("C1:G2")
        workbook.active.column_dimensions["A"].width = 6
        workbook.active.column_dimensions["F"].width = 6
        workbook.active.column_dimensions["B"].width = 17
        workbook.active.column_dimensions["G"].width = 17
        workbook.active.column_dimensions["E"].width = 5
        workbook.active["C1"] = user_name.title() + "'s " + "Paysheet: " + month + "/" + year
        workbook.active["C1"].font = Font(name="Times New Roman", bold=True, size=20, italic=True)
        workbook.active["A3"] = "Date"
        workbook.active["B3"] = "session name"
        workbook.active["C3"] = "Length"
        workbook.active["D3"] = "Signature"
        workbook.active["F3"] = "Date"
        workbook.active["G3"] = "session name"
        workbook.active["H3"] = "Length"
        workbook.active["I3"] = "Signature"
        return workbook

    def generate(self, user_name, month, year, user_schedule, days_to_schedule, monthly_meetings, extra_sessions):
        workbook = self._create_preformatted_workbook(user_name, month, year)
        workbook.active = self.write_sessions(days_to_schedule, workbook.active, user_schedule, monthly_meetings,
                                              extra_sessions)
        return workbook

    def write_sessions(self, to_schedule, sheet, user_schedule, monthly_meetings, extra_sessions):
        col = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        col_index = 0
        row_index = 4

        for day in to_schedule:
            day_and_month = str(day.month) + "/" + str(day.day)

            weekday = self.weekdays_map[day.weekday()]
            [sheet, row_index, col_index] = self.write_day(user_schedule, row_index, col_index, day_and_month,
                                                           sheet, col,
                                                           day=weekday)

            if str(day.day) in monthly_meetings:
                [sheet, row_index, col_index] = self._write_monthly_meeting(sheet, col, col_index, row_index,
                                                                            day_and_month)

            if len(extra_sessions) > 0:
                [sheet, row_index, col_index] = self._write_extra_sessions(extra_sessions, day, sheet, col,
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

    def _write_monthly_meeting(self, sheet, col, col_index, row_index, day_and_month):
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

    def _write_extra_sessions(self, extra_sessions, day, sheet, col, col_index, row_index, day_and_month):
        for session in extra_sessions:
            if int(session.date) == int(day.day):
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

    def export(self, workbook, user_name):
        try:
            if not os.path.isdir(config.PAY_SHEET_EXPORT_DIR):
                os.makedirs(config.PAY_SHEET_EXPORT_DIR)
            workbook.save(os.path.join(config.PAY_SHEET_EXPORT_DIR, user_name + "_paysheet" + '.xlsx'))
            LOGGER.debug("Your Paysheet has been created and saved and should be available in a folder name '%s'"
                         " located inside the folder containing this program." % config.PAY_SHEET_EXPORT_DIR)
            LOGGER.info(user_name + ' successfully generated a paysheet.')
        except:
            LOGGER.debug("An error occurred when attempting to save your Paysheet. Make sure no spreadsheets are "
                         "currently open. If they are close them, and then retry well paying careful attention to "
                         "the on screen instructions.")
            LOGGER.info(user_name + ' encountered an error well generating a paysheet.')
