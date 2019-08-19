import getpass
from hashlib import sha256 as hash

from lib.schedule import Session, ExtraSession
from lib.logger import Logger

logger = Logger.get_logger(__name__)


class CmdInputHandler:
    available_user_choices = ["register", "login"]

    available_actions = ["new", "add", "edit", "export", "view", "remove", "done"]

    username_input_message = """
    Please input your desired user name:
    """

    action_input_message = """
    Enter 'new' create a new schedule, 'add' to add sessions to your current one,
    remove' to remove a session, 'view' to see your current schedule, or 'export' to
    create a copy of it:
    """

    sessions_help = """
    Please input your session info in EXACTLY the same format that will be described below:
    [session (W55) length(in hours) day (as a num)].
    Days taught are entered as a number or written out: [1 = Monday 5 = Friday]
    Use the following example to format your input: "W60 1 3"
    The above means session W60, taught for one hour, on Wednesday
    Do not include "" or a space before W in your input.
    """

    sessions_input_message = """
    Please input session information or type "done" if you are finished:
    """

    view_day_input_message = """
    Please enter the day you wish to view, enter "all" to see your entire
    schedule or "done" to exit.
    """

    def register_or_login(self):
        user_choice_known = False
        while not user_choice_known:
            user_choice = input("Hello, please enter 'login' to login, or type 'register' to create an account:\n")
            logger.info("A user entered: " + user_choice)
            user_choice_known = user_choice in self.available_user_choices
        return user_choice

    def retrieve_password(self):
        while True:
            password_1 = getpass.getpass("Please enter your password:\n")
            password_1 = hash(password_1.encode("utf-8")).digest()
            password_2 = getpass.getpass("Please enter it one more time:\n")
            password_2 = hash(password_2.encode("utf-8")).digest()
            if password_1 == password_2:
                return password_1
            else:
                logger.debug("Sorry your passwords don't match.")

    def retrieve_username(self):
        return input(self.username_input_message).lower()

    def retrieve_action(self):
        action_known = False
        while not action_known:
            action = input(self.action_input_message).lower()
            action_known = action in self.available_actions
            if not action_known:
                logger.debug("Sorry that wasn't one of the options, please try again.")
                logger.info("Could not proceed with option  " + action + " due to invalid input.")
        return action

    def retrieve_sessions(self):
        sessions = []
        logger.debug(self.sessions_help)

        while True:
            session_info = input(self.sessions_input_message).lower()
            if session_info == "done":
                return sessions

            try:
                session_list = session_info.split()
                if len(session_list) == 3:
                    sessions.append(Session(session_list[0], session_list[1], session_list[2]))
                    logger.debug("You have entered the following sessions:")
                    for session in sessions:
                        logger.debug(session.code + " day = " + session.day)
                else:
                    logger.debug("Sorry it seems the data you entered doesnt the required format. Please try again")
            except:
                logger.debug("Sorry it seems the data you entered doesnt the required format. Please try again")

    def retrieve_credentials(self):
        name = input("Please enter your user name:\n").lower()
        password = getpass.getpass("Please enter your password:\n")
        return {"name": name, "password": password}

    def retrieve_day_to_view(self):
        return input(self.view_day_input_message).lower()

    def retrieve_month(self):
        possible_months = ['01', '1', '2', '02', "3", '03', "4", '04', "5", '05', "6", '06', "7", '07', "8", '08',
                           "9", '09', "10", '11', '12']
        valid_month = False
        while not valid_month:
            month = input("Please input a month as a numeric value [E.g. 4 for April]: \n")
            if len(month) == 1:
                month = "0" + month
            valid_month = month in possible_months
            if not valid_month:
                logger.debug("Sorry I can't make sense of what month you mean. Please try again.")
        return month

    def retrieve_extra_sessions(self):
        extra_sessions = []
        logger.debug(
            "\nHave you subbed any sessions this month? \nInput \"done\" if you haven\"t or when finished entering"
            " those you have.\n"
            "If you have enter each session one at a time in the following format [session id length date] \n"
            "ex: W34 2 13.")
        while True:
            logger.debug("Your current list of sessions you have subbed this month is as follows:")
            for session in extra_sessions:
                logger.debug(session.code + " ")
            logger.debug("\n")
            extra_session = input("Enter a session to add to your subbed sessions, or \"done\" if you are finished:\n")
            logger.info(("Entered: " + extra_session))
            if extra_session.lower() == "done":
                break
            else:
                try:
                    extra_session_split = extra_session.split(" ")
                    extra_sessions.append(
                        ExtraSession(extra_session_split[0], extra_session_split[1], extra_session_split[2]))
                    logger.info("Added " + extra_session + " to their list of sessions they subbed.")
                except:
                    logger.debug(
                        "Sorry but you entered that session in incorrectly, it won\"t be added. Please try again")

        return extra_sessions

    def retrieve_missed_days(self):
        missed_days = []
        logger.debug("Enter any days you missed work due to sickness or holiday as a number. "
                     "[ex \"12\"] for the 12th or enter \"done\". \n")

        while True:
            logger.debug("Your current missed days are as follows: " + str(missed_days))
            missed_day = input("Enter a missed day as a number or \"done\" to move on. \n")
            if missed_day.lower() == "done":
                break
            else:
                missed_days.append(int(missed_day))

        return missed_days

    def find_month_length(self, month, year):
        if month in ["01", "1" "03", "3", "05", "5", "07", "7", "08", "8", "10"]:
            length = "31"
        elif month in ["04", "4", "06", "6", "09", "9", "11", "12"]:
            length = "30"
        else:
            if int(year) % 4 == 0:
                length = 29
            else:
                length = 28
        return length

    def get_monthly_meetings(self):
        meetings = []

        while True:
            meeting = input("Did you have any meetings this month? If yes enter the days of the meeting as a number"
                            " [ex 5th = 5] \n or enter \"done\" to move on:\n")
            logger.debug("Current days with meetings are: " + str(meetings))

            if meeting.lower() == "done":
                break
            else:
                meetings.append(meeting)

        return meetings


class FakeInputHandler(CmdInputHandler):

    user_choice_count = 0

    action_count = 0

    def register_or_login(self):
        self.user_choice_count += 1
        if self.user_choice_count is 1:
            return 'register'
        else:
            return 'login'

    def retrieve_password(self):
        return "1234"

    def retrieve_username(self):
        return "test"

    def retrieve_action(self):
        self.action_count += 1
        if self.action_count is 1:
            return "new"
        else:
            return "done"

    def retrieve_sessions(self):
        return [Session("W12", "2", "4")]

    def retrieve_credentials(self):
        return {"name": "test", "password": "1234"}

    def retrieve_day_to_view(self):
        return "all"


