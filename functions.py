from openpyxl.styles import Font


def find_month_length(month, year):
    if month in ["01", "03", "05", "07", "08", "10"]:
        length = "31"
    elif month in ["04", "06", "09", "11", "12"]:
        length = "30"
    else:
        if year % 4 == 0:
            length = 29
        else:
            length = 28
    return length


def format_sheet(workbook, month, year):
    sheet = workbook.active
    font_obj = Font(name="Times New Roman", bold=True, size=25, italic=True)
    sheet.title = "Paysheet"
    sheet.merge_cells("D1:J2")
    sheet.column_dimensions["B"].width = 20
    sheet.column_dimensions['F'].width = 20

    sheet["D1"] = "Ginos Paysheet for " + month + "/" + year
    sheet['D1'].font = font_obj

    sheet["A3"] = "Date"
    sheet["B3"] = "Class name"
    sheet["C3"] = "Length"
    sheet["D3"] = "Signature"
    sheet["E3"] = "Date"
    sheet['F3'] = "Class name"
    sheet['G3'] = "Length"
    sheet['H3'] = "Signature"
    return sheet

def write_schedule(to_schedule, sheet, mon, wed, fri):
    col = ["A", 'B', "C", "D", "E", "F", "G", "H"]

    col_index = 0
    row_index = 4

    for day in to_schedule:
        day_and_month = str(day.month) + '/' + str(day.day)
        if day.weekday() == 0:
            schedule = mon
            for session in schedule:
                sheet[col[col_index] + str(row_index)] = day_and_month
                col_index += 1
                sheet[col[col_index] + str(row_index)] = session.code
                col_index += 1
                sheet[col[col_index] + str(row_index)] = session.length
                col_index += 2

                if col_index == 4:

                    pass
                else:
                    col_index = 0
                    row_index += 1

        elif day.weekday() == 2:
            schedule = wed
            for session in schedule:
                sheet[col[col_index] + str(row_index)] = day_and_month
                col_index += 1
                sheet[col[col_index] + str(row_index)] = session.code
                col_index += 1
                sheet[col[col_index] + str(row_index)] = session.length
                col_index += 2

                if col_index == 4:
                    pass
                else:
                    col_index = 0
                    row_index += 1

        elif day.weekday() == 4:
            schedule = fri
            for session in schedule:
                sheet[col[col_index] + str(row_index)] = day_and_month
                col_index += 1
                sheet[col[col_index] + str(row_index)] = session.code
                col_index += 1
                sheet[col[col_index] + str(row_index)] = session.length
                col_index += 2

                if col_index == 4:
                    pass
                else:
                    col_index = 0
                    row_index += 1
    return sheet

