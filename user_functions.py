import pickle
from hashlib import sha256 as hash


def register_user():
    try:
        users = open("users", 'rb')
        all_users = pickle.load(users)
        users.close()

    except:
        all_users = {}

    while True:

        new_user = input("Please tell me your desired user name: \n ")
        if new_user.lower() in all_users:
            print("Sorry that name is taken.")
        else:
            password_1 = input("Hello " + new_user + " please create your password: \n ")
            password_1 = hash(password_1.encode('utf-8'))
            password_2 = input("please enter it one more time: \n ")
            password_2 = hash(password_2.encode('utf-8'))

            if password_1.digest() == password_2.digest():
                all_users[new_user] = password_1.digest()
                users = open('users', 'wb')
                pickle.dump(all_users, users)
                users.close()
                print("You are now registered, you may login next time.")
                break
            else:
                print("Sorry your passwords didn't match, please restart the registration process.")


def login_user():
    try:
        users = open("users", 'rb')
        all_users = pickle.load(users)
        users.close()

    except:
        all_users = {}

    while True:
        name = input("Please enter your user name: \n")

        if name in all_users:
            password = input("Please enter your password: \n")
        else:
            print("Sorry that username isn't registered, please register first.")
            exit()

        if hash(password.encode('utf-8')).digest() == all_users[name]:
            print("Welcome", name + ".")
            break
        else:
            print("Sorry it appears your password is incorrect, please try again")
            break
    return name

