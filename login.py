import openpyxl
from hashlib import sha256 as hash

# Allow users to register or login
user_names = ['gino']

new_users = {}
user = input("Hello, please enter your username to login, or type 'register' to register: ")

if user.lower() == 'register':
    open_name = False

    while not open_name:
        new_user = input("Please tell me your desired user name: ")
        if new_user.lower() in user_names:
            print("Sorry that name is taken.")
        else:
            password_1 = input("Hello " + new_user + " please create your password: ")
            password_1 = hash(password_1.encode('utf-8'))
            password_2 = input("please enter it one more time: ")
            password_2 = hash(password_2.encode('utf-8'))

            if password_1.digest() == password_2.digest():
                new_users[new_user] = password_1.digest()
                open_name = True
            else:
                print("Sorry your passwords didn't match, please restart the registration process.")