import os

from lib.application import ApplicationFactory
import config

test_pay_sheet = os.path.join(config.pay_sheet_export_dir, "test_pay_sheet.xlsx")
if os.path.isfile(test_pay_sheet):
    os.remove(test_pay_sheet)

if os.path.isfile(config.user_db_path):
    os.remove(config.user_db_path)

test_schedule_path = os.path.join(config.user_schedules_dir, "test")
if os.path.isfile(test_schedule_path):
    os.remove(test_schedule_path)


app = ApplicationFactory.mock()
app.run()
