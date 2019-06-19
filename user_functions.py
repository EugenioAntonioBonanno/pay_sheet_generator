import pickle
from hashlib import sha256 as hash
from objects import Session, Day, User
from pathlib import Path
import getpass
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(message)s', level=logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(funcName)s:%(levelname)s:%(message)s')

file_handler = logging.FileHandler('logs.txt')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)


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
            logger.debug("Sorry that name is taken.")
        else:
            password_1 = getpass.getpass("Hello " + new_user + " please create your password: \n ")
            password_1 = hash(password_1.encode('utf-8'))
            password_2 = getpass.getpass("please enter it one more time: \n ")
            password_2 = hash(password_2.encode('utf-8'))

            if password_1.digest() == password_2.digest():
                all_users[new_user] = password_1.digest()
                users = open(users_info_path, 'wb')
                pickle.dump(all_users, users)
                users.close()
                logger.debug("You are now registered, you may run the program again and login.")
                logger.info(new_user + " has been created successfully")
                break
            else:
                logger.debug("Sorry your passwords didn't match, please restart the registration process.")
                logger.info(new_user + " tired to create a user, but entered passwords that don't match ")


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
            logger.debug("Sorry we don't have a user by that name. Please try again, or register a new account")
    return name


def check_password(name):
    try:
        users = open(users_info_path, 'rb')
        all_users = pickle.load(users)
        users.close()
    except:
        all_users = {}


    while True:
        password = getpass.getpass("Please enter your password: \n")

        if password:
            if hash(password.encode('utf-8')).digest() == all_users[name]:
                logger.debug("Welcome " + name + ".")
                logger.info(name + " has successfully logged in")
                break
            else:
                logger.debug("Sorry it appears your password is incorrect, please try again")
                logger.info(name + " entered the wrong password ")

    return name


def create_schedule(active_user, make_or_write):
    sessions = []
    users_object_path = root / "user_objects" / active_user

    logger.debug("\nPlease input your class info in EXACTLY the same format that will be described below: \n"
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
                            logger.debug("You have entered the following classes:", end=" ")
                            for session in sessions:
                                logger.debug(session.code, "day = ", session.day_taught, end=" ")
                            logger.debug("\n")
                            logger.info(active_user + " added the class", session_info, "to there schedule.")
                    else:
                        logger.debug("Sorry it seems the data you entered doesnt the required format. Please try again")
                        logger.info(active_user + "attempted to add the incorrect format: " + session_info + " to their schedule.")
                except:
                        logger.debug("Sorry it seems the data you entered doesnt the required format. Please try again")
                        logger.info(active_user + "attempted to add the incorrect format:" + session_info + " to their schedule.")


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

        logger.debug("\nYour schedule has been successfully created, the program will now return you to the previous menu.. \n \n")
        logger.info(active_user + "has successfully set up their schedule.")


def add_class(active_user):
    classes_to_add = []
    users_object_path = root / "user_objects" / active_user
    schedule = open(users_object_path, 'rb')
    users_schedule = pickle.load(schedule)

    while True:

        class_to_add = input("Please enter the class you wish to add in the same format you entered it"
                                "[class, length' day] ex: W60 1 3. Or type 'done': \n")

        if class_to_add.lower() == 'done':
            break

        try:
            class_list = class_to_add.split()
            if len(class_list) == 3:
                classes_to_add.append(Session(class_list[0], class_list[1], class_list[2]))
                logger.debug("You have entered the following classes:", end=" ")
                for session in classes_to_add:
                    logger.debug(session.code, "day = " + session.day_taught, end=" ")
                logger.debug("\n")
                logger.info(active_user + "added the class", class_to_add, 'to their schedule.')

            else:
                logger.debug("Sorry it seems the data you entered doesnt match the required format. Please try again")
                logger.info(active_user + "attempted to add incorrect input " + class_to_add + ' to their schedule.')
        except:
            logger.debug("Sorry it seems the data you entered doesnt match the required format. Please try again")
            logger.info(active_user + " attempted to add incorrect input " + class_to_add + ' to their schedule.')

    for add_session in classes_to_add:
        for user_day in users_schedule.week:
            for user_session in user_day.sessions:
                if user_session.day_taught == add_session.day_taught:
                    user_day.sessions.append(add_session)
                    break


    schedule = open(users_object_path, "wb")
    pickle.dump(users_schedule, schedule)
    schedule.close()


def remove_class(active_user):
    classes_to_remove = []
    users_object_path = root / "user_objects" / active_user
    schedule = open(users_object_path, 'rb')
    users_schedule = pickle.load(schedule)

    while True:

        class_to_remove = input("Please enter the class you wish to remove in the same format you entered it"
                            "[class, length' day] ex: W60 1 3. Or type 'done': \n")

        if class_to_remove.lower() == 'done':
            break

        try:
            class_list = class_to_remove.split()
            if len(class_list) == 3:
                classes_to_remove.append(Session(class_list[0], class_list[1], class_list[2]))
                logger.debug("You have entered the following classes:", end=" ")
                for session in classes_to_remove:
                    logger.debug(session.code, "day = " + session.day_taught, end=" ")
                logger.debug("\n")
                logger.info(active_user + "removed the class" + class_to_remove + ' from their schedule.')
            else:
                logger.debug("Sorry it seems the data you entered doesnt match the required format. Please try again")
                logger.info(active_user + "attempted to removed the class via incorrect input " + class_to_remove + ' from their schedule.')
        except:
            logger.debug("Sorry it seems the data you entered doesnt match the required format. Please try again")
            logger.info(active_user + "attempted to removed the class via incorrect input" + class_to_remove + ' from their schedule.')

    for day in users_schedule.week:
        for user_session in day.sessions:
            for delete_session in classes_to_remove:
                if user_session.code == delete_session.code and user_session.length == delete_session.length and user_session.day_taught == delete_session.day_taught:
                    day.sessions.remove(user_session)

    schedule = open(users_object_path, "wb")
    pickle.dump(users_schedule, schedule)
    schedule.close()


def view_schedule(active_user):
    users_object_path = root / "user_objects" / active_user
    schedule = open(users_object_path, 'rb')
    users_schedule = pickle.load(schedule)

    while True:
        day_to_see = input("Please enter the day you wish to view as a number, enter 'all' to see your entire schedule or 'done' to exit. \n [1 = Monday 5 = Friday]:\n")
        logger.info(active_user + ' is about to view the day ' + day_to_see + ' from their schedule')

        to_view = []

        if day_to_see == '1':
            to_view.append("Monday")
        elif day_to_see == '2':
            to_view.append("Tuesday")
        elif day_to_see == '3':
            to_view.append("Wednesday")
        elif day_to_see == '4':
            to_view.append("Thursday")
        elif day_to_see == '5':
            to_view.append("Friday")
        elif day_to_see.lower() == 'all':
            to_view = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        elif day_to_see.lower() == 'done':
            break
        else:
            logger.debug("Sorry that isn't a valid option please try again")
            logger.info(active_user + 'failed to view ' + day_to_see + ' from their schedule due to incorrect input')
            pass

        for day in users_schedule.week:
            if day.name in to_view:
                logger.debug("")
                for session in day.sessions:
                    logger.debug("Day: " + day.name + ' Class Code: ' + session.code + ' Class length: ' + session.length)
                logger.debug("")







