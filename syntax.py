import openpyxl

# Create a workbook object
wb = openpyxl.load_workbook('example.xlsx')

# Create a sheet object
sheet = wb['Sheet1']

# Access the value of a location on a sheet. Using "A1" format.  This value being column "A" and row "1".

print(sheet["A2"].value)

