import openpyxl
from hashlib import sha256 as hash
import pickle

# Code to write to or edit a excel file. Currently under development.


password = "godberry5"

greeting = input("Hello please put in the password to continue: ")

if password == greeting:
    print("Hello, and welcome!")
else:
    print("Wrong password program will terminate")
    exit()











