import pickle
from hashlib import sha256 as hash
from objects import Session, Day, User
from pathlib import Path

# Allows a user to register a local account
root = Path(".")

users_info_path = root / "user_info" / 'users'


def register_user():
    try:
        users = open(users_info_path, 'rb')
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
                users = open(users_info_path, 'wb')
                pickle.dump(all_users, users)
                users.close()
                print("You are now registered, you may login next time.")
                break
            else:
                print("Sorry your passwords didn't match, please restart the registration process.")


# Allows a user to login well retaining any session objects they had created
def login_user():

    name = check_username()

    name = check_password(name)

    return name


def check_username():
    try:
        users = open(users_info_path, 'rb')
        all_users = pickle.load(users)
        users.close()

    except:
        all_users = {}

    while True:
        name = input("Please enter your user name: \n")

        if name in all_users:
            break
        else:
            print("Sorry we don't have a user by that name. Please try again, or register a new account")
    return name


def check_password(name):
    try:
        users = open(users_info_path, 'rb')
        all_users = pickle.load(users)
        users.close()
    except:
        all_users = {}


    while True:
        password = input("Please enter your password: \n")

        if password:
            if hash(password.encode('utf-8')).digest() == all_users[name]:
                print("Welcome", name + ".")
                break
            else:
                print("Sorry it appears your password is incorrect, please try again")

    return name


def create_schedule(active_user, make_or_write):
    sessions = []
    users_object_path = root / "user_objects" / active_user

    print("\nPlease input your class info in EXACTLY the same format that will be described below: \n"
          "[class (W55) length(in hours) day (as a num)]. \n"
          "Days taught are entered as a number between 1-5 [1 = Monday 5 = Friday] \n"
          "Use the following example to format your input: 'W60 1 3'.\n"
          "The above means class W60, taught for one hour, on Wednesday \n"
          "Do not include '' or a space before W in your input. \n")


    if make_or_write.lower() == "set":

        while True:
            session_info = input("Please input class information or type 'done' if you are finished: \n")
            if session_info.lower() == "done":
                break
            else:
                try:
                    session_list = session_info.split()
                    if len(session_list) == 3:
                            sessions.append(Session(session_list[0], session_list[1], session_list[2]))
                            print("You have entered the following classes:", end=" ")
                            for session in sessions:
                                print(session.code, "day = ", session.day_taught, end=" ")
                            print("\n")
                    else:
                        print("Sorry it seems the data you entered doesnt the required format. Please try again")
                except:
                        print("Sorry it seems the data you entered doesnt the required format. Please try again")


        monday_sessions = []
        tuesday_sessions = []
        wednesday_sessions = []
        thursday_sessions = []
        friday_sessions = []

        for session in sessions:
            if session.day_taught == '1':
                monday_sessions.append(session)
            elif session.day_taught == '2':
                tuesday_sessions.append(session)
            elif session.day_taught == '3':
                wednesday_sessions.append(session)
            elif session.day_taught == '4':
                thursday_sessions.append(session)
            elif session.day_taught == '5':
                friday_sessions.append(session)

        week = []
        monday = Day("Monday", monday_sessions)
        week.append(monday)
        tuesday = Day("Tuesday", tuesday_sessions)
        week.append(tuesday)
        wednesday = Day("Wednesday", wednesday_sessions)
        week.append(wednesday)
        thursday = Day("Thursday", thursday_sessions)
        week.append(thursday)
        friday = Day("Friday", friday_sessions)
        week.append(friday)

        users_schedule = User(active_user, week)

        schedule = open(users_object_path, "wb")
        pickle.dump(users_schedule, schedule)
        schedule.close()

        print("\nYour schedule has been successfully created, the program will now return you to the previous menu.. \n \n")

    elif make_or_write.lower() == "add":
        while True:
            session_info = input("Please input class information or type 'done' if you are finished: \n")
            if session_info.lower() == "done":
                break
            else:
                try:
                    session_list = session_info.split()
                    if len(session_list) == 3:
                        sessions.append(Session(session_list[0], session_list[1], session_list[2]))
                        print("You have entered the following classes:", end=" ")
                        for session in sessions:
                            print(session.code, "day = ", session.day_taught, end=" ")
                        print("\n")
                    else:
                        print("Sorry it seems the data you entered doesnt match the required format. Please try again")
                except:
                    print("Sorry it seems the data you entered doesnt match the required format. Please try again")


        monday_sessions = []
        tuesday_sessions = []
        wednesday_sessions = []
        thursday_sessions = []
        friday_sessions = []

        for session in sessions:
            if session.day_taught == '1':
                monday_sessions.append(session)
            elif session.day_taught == '2':
                tuesday_sessions.append(session)
            elif session.day_taught == '3':
                wednesday_sessions.append(session)
            elif session.day_taught == '4':
                thursday_sessions.append(session)
            elif session.day_taught == '5':
                friday_sessions.append(session)

        week = []
        monday = Day("Monday", monday_sessions)
        week.append(monday)
        tuesday = Day("Tuesday", tuesday_sessions)
        week.append(tuesday)
        wednesday = Day("Wednesday", wednesday_sessions)
        week.append(wednesday)
        thursday = Day("Thursday", thursday_sessions)
        week.append(thursday)
        friday = Day("Friday", friday_sessions)
        week.append(friday)

        users_schedule = User(active_user, week)

        schedule = open(users_object_path, "ab")
        pickle.dump(users_schedule, schedule)
        schedule.close()
        print("\nYour schedule has been successfully edited, the program will now return you to the previous menu \n \n")


def remove_class(active_user):
    classes_to_remove = []
    users_object_path = root / "user_objects" / active_user
    schedule = open(users_object_path, 'rb')
    users_schedule = pickle.load(schedule)

    while True:
        try:
            added_days = (pickle.load(schedule))
            for day in added_days.week:
                for user_day in users_schedule.week:
                    if day.name == user_day.name:
                        for session in day.sessions:
                            user_day.sessions.append(session)
        except EOFError:
            schedule.close()
            break

    while True:

        class_to_remove = input("Please enter the class you wish to remove in the same format you entered it"
                            "[class, length' day] ex: W60 1 3. Or type 'done': \n")

        if class_to_remove.lower() == 'done':
            break

        try:
            class_list = class_to_remove.split()
            if len(class_list) == 3:
                classes_to_remove.append(Session(class_list[0], class_list[1], class_list[2]))
                print("You have entered the following classes:", end=" ")
                for session in classes_to_remove:
                    print(session.code, "day = ", session.day_taught, end=" ")
                print("\n")
            else:
                print("Sorry it seems the data you entered doesnt match the required format. Please try again")
        except:
            print("Sorry it seems the data you entered doesnt match the required format. Please try again")

    for day in users_schedule.week:
        for user_session in day.sessions:
            for delete_session in classes_to_remove:
                if user_session.code == delete_session.code and user_session.length == delete_session.length and user_session.day_taught == delete_session.day_taught:
                    day.sessions.remove(user_session)

    schedule = open(users_object_path, "wb")
    pickle.dump(users_schedule, schedule)
    schedule.close()





class Day:
    def __init__(self, name, sessions):
        self.name = name
        self.sessions = sessions


class Session:
    def __init__(self, code, length, day_taught):
        self.code = code
        self.length = length
        self.day_taught = day_taught


class User:
    def __init__(self, user_name, week):
        self.user_name = user_name
        self.week = week  #list of day objects


