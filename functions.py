

def find_month_length(month):
    if month in ["01", "03", "05", "07", "08", "10"]:
        length = "31"
    elif month in ["04", "06", "09", "11", "12"]:
        length = "30"
    else:
        length = "28"
    return length

# def create_workbook()