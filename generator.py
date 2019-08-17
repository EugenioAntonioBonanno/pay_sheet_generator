from lib.controller import CmdInputHandler, Controller
from lib.schedule import ScheduleDataSource
from lib.user import UserDataSource, UserRegistrar

input_handler = CmdInputHandler()
user_ds = UserDataSource()
user_registrar = UserRegistrar(input_handler, user_ds)
schedule_ds = ScheduleDataSource()

user_choice = input_handler.retrieve_user_choice()
if user_choice == 'register':
    user_registrar.register()

active_user = user_registrar.login()
controller = Controller(active_user, input_handler, user_ds, schedule_ds)
while True:
    action = input_handler.retrieve_action()
    controller.execute(action)
