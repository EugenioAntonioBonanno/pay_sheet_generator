import pickle
from hashlib import sha256 as hash
from objects import Session, Day, User

# Allows a user to register a local account


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


# Allows a user to login well retaining any session objects they had created
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

def create_schedule(active_user):
    sessions = []
    print("\nPlease input your class info in EXACTLY the same format that will be described below: \n"
          "[class (W55) length(in hours) day (as a num)]. \n"
          "Days taught are entered as a number between 1-5 [1 = Monday 5 = Friday] \n"
          "Use the following example to format your input: 'W60 1 3'.\n"
          "The above means class W60, taught for one hour, on Wednesday \n"
          "Do not include '' or a space before W in your input. \n")
    while True:
        session_info = input("Please input class information or type 'done' if you are finished: \n")
        if session_info.lower() == "done":
            break
        else:
            session_list = session_info.split()
            sessions.append(Session(session_list[0], session_list[1], session_list[2]))
            print("You have entered the following classes:", end=" ")
            for session in sessions:
                print(session.code, "day = ", session.day_taught, end=" ")
            print("\n")

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

    schedule = open(active_user, "wb")
    pickle.dump(users_schedule, schedule)
    schedule.close()

