import logging
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
    controller.execute(action)
