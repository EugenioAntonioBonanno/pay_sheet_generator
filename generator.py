import logging
from pathlib import Path
from lib.user import UserDataSource
from lib.schedule_data import CmdInputHandler, Controller, UserRegistrar

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(funcName)s:%(levelname)s:%(message)s")

file_handler = logging.FileHandler("logs.txt")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)

input_handler = CmdInputHandler()
user_ds = UserDataSource()
user_registrar = UserRegistrar(input_handler, user_ds)

user_choice = input_handler.retrieve_user_choice()
if user_choice == 'register':
    user_registrar.register()

active_user = user_registrar.login()
controller = Controller(active_user, input_handler, user_ds)
while True:
    action = input_handler.retrieve_action()
    if action == "new":
        controller.new()
    elif action == "add":
        controller.add()
    elif action == "view":
        controller.view()
    elif action == "export":
        controller.export()
    elif action == "remove":
        controller.remove()
    elif action == "done":
        exit()
    else:
        logger.debug("Sorry that wasn't one of the options, please try again.")
        logger.info("Could not proceed with option  " + action + " due to invalid input.")

