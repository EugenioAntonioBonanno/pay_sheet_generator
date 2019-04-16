from openpyxl.styles import Font


def find_month_length(month):
    if month in ["01", "03", "05", "07", "08", "10"]:
        length = "31"
    elif month in ["04", "06", "09", "11", "12"]:
        length = "30"
    else:
        length = "28"
    return length


def format_sheet(workbook, month, year):
    sheet = workbook.active
    font_obj = Font(name="Times New Roman", bold=True, size=25, italic=True)
    sheet.title = "Paysheet"
    sheet.merge_cells("D1:J2")
    sheet.column_dimensions["B"].width = 20
    sheet["D1"] = "Ginos Paysheet for " + month + "/" + year
    sheet['D1'].font = font_obj
    sheet["A1"] = "Date"
    sheet["B1"] = "Class name"
    sheet["C1"] = "Length"
    return sheet


