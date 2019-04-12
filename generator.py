import openpyxl
import os

# Code to write to or edit a excel file. Currently under development.

# place = os.getcwd()
# print("Here I AM!", place)


wb = openpyxl.load_workbook('example.xlsx')

print(wb.sheetnames)

sheet = wb['Sheet3']

print(sheet)

active = wb.active

print(active)

