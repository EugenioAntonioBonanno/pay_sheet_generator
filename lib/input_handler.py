import getpass

from lib.logger import Logger
from lib.schedule import Session, ExtraSession

LOGGER = Logger.get_logger(__name__)


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
            LOGGER.info("A user entered: %s", user_choice)
            user_choice_known = user_choice in self.available_user_choices
        return user_choice

    def retrieve_password(self):
        while True:
            password = getpass.getpass("Please enter your password:\n")
            password_confirm = getpass.getpass("Please enter it one more time:\n")
            if password == password_confirm:
                return password
            LOGGER.debug("Sorry your passwords don't match.")

    def retrieve_username(self):
        return input(self.username_input_message).lower()

    def retrieve_action(self):
        action_known = False
        while not action_known:
            action = input(self.action_input_message).lower()
            action_known = action in self.available_actions
            if not action_known:
                LOGGER.debug("Sorry that wasn't one of the options, please try again.")
                LOGGER.info("Could not proceed with option  %s due to invalid input.", action)
        return action

    def retrieve_sessions(self):
        sessions = []
        LOGGER.debug(self.sessions_help)

        while True:
            session_info = input(self.sessions_input_message).lower()
            if session_info == "done":
                return sessions

            session_args = session_info.split()
            if len(session_args) is not 3:
                LOGGER.debug("Sorry it seems the data you entered doesnt the required format. Please try again")
                continue

            sessions.append(Session(session_args[0], session_args[1], session_args[2]))
            LOGGER.debug("You have entered the following sessions:")
            for session in sessions:
                LOGGER.debug("%s day = %s", session.code, session.day)

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
                LOGGER.debug("Sorry I can't make sense of what month you mean. Please try again.")
        return month

    def retrieve_extra_sessions(self):
        extra_sessions = []
        LOGGER.debug(
            "\nHave you subbed any sessions this month? \nInput \"done\" if you haven\"t or when finished entering"
            " those you have.\n"
            "If you have enter each session one at a time in the following format [session id length date] \n"
            "ex: W34 2 13.")
        while True:
            LOGGER.debug("Your current list of sessions you have subbed this month is as follows:")
            for session in extra_sessions:
                LOGGER.debug("%s ", session.code)
            LOGGER.debug("\n")
            extra_session = input("Enter a session to add to your subbed sessions, or \"done\" if you are finished:\n")
            LOGGER.info(("Entered: %s", extra_session))

            if extra_session.lower() == "done":
                return extra_sessions

            session_args = extra_session.split()
            if len(session_args) is not 3:
                LOGGER.debug("Sorry, you entered that session in incorrectly, it won't be added. Please try again.")
                continue

            extra_sessions.append(ExtraSession(session_args[0], session_args[1], session_args[2]))
            LOGGER.info("Added %s to their list of sessions they subbed.", extra_session)

        return extra_sessions

    def retrieve_missed_days(self):
        missed_days = []
        LOGGER.debug("Enter any days you missed work due to sickness or holiday as a number. "
                     "[ex \"12\"] for the 12th or enter \"done\". \n")

        while True:
            LOGGER.debug("Your current missed days are as follows: %s", str(missed_days))
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
                length = "29"
            else:
                length = "28"
        return length

    def get_monthly_meetings(self):
        meetings = []

        while True:
            meeting = input("Did you have any meetings this month? If yes enter the days of the meeting as a number"
                            " [ex 5th = 5] \n or enter \"done\" to move on:\n")
            LOGGER.debug("Current days with meetings are: %s", str(meetings))

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
        return 'login'

    def retrieve_password(self):
        return "1234"

    def retrieve_username(self):
        return "test"

    def retrieve_action(self):
        self.action_count += 1
        if self.action_count is 1:
            return "new"
        if self.action_count is 2:
            return "export"
        return "done"

    def retrieve_sessions(self):
        return [Session("W12", "2", "4")]

    def retrieve_credentials(self):
        return {"name": "test", "password": "1234"}

    def retrieve_day_to_view(self):
        return "all"

    def retrieve_month(self):
        return "08"

    def retrieve_extra_sessions(self):
        return [ExtraSession("W99", "3", "13")]

    def retrieve_missed_days(self):
        return [15]

    def find_month_length(self, month, year):
        return "31"

    def get_monthly_meetings(self):
        return "done"
