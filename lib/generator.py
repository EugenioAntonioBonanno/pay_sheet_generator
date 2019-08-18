import os

from openpyxl.styles import Font

import config
from lib.schedule import ScheduleDataSource


class ExcelSheetFormatter:

    def create_schedule(self, workbook):
        sheet = workbook.active
        sheet.title = "Paysheet"
        return sheet

    def format_schedule(self, sheet, user, month, year):
        sheet.merge_cells("C1:G2")
        sheet.column_dimensions["A"].width = 6
        sheet.column_dimensions["F"].width = 6
        sheet.column_dimensions["B"].width = 17
        sheet.column_dimensions["G"].width = 17
        sheet.column_dimensions["E"].width = 5
        sheet["C1"] = user.name.title() + "'s " + "Paysheet: " + month + "/" + year
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


class ExcelSheetGenerator:
    _schedule_ds: ScheduleDataSource

    def __init__(self, schedule_ds: ScheduleDataSource):
        self._schedule_ds = schedule_ds

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
        for session in extra_sessions_worked:
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

    def export_schedule(self, workbook, user):
        if not os.path.isdir(config.pay_sheet_export_dir):
            os.makedirs(config.pay_sheet_export_dir)
        workbook.save(os.path.join(config.pay_sheet_export_dir, user.name + "_paysheet" + '.xlsx'))