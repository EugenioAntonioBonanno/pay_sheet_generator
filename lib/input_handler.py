import getpass

from lib.logger import Logger
from hashlib import sha256 as hash

from lib.schedule import Session

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

    def retrieve_user_choice(self):
        user_choice_known = False
        while not user_choice_known:
            user_choice = input("Hello, please enter 'login' to login, or type 'register' to create an account:\n")
            logger.info("A user entered: " + user_choice)
            user_choice_known = user_choice in self.available_user_choices

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
                        logger.debug(session.code + " day = " + session.day_taught)
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
