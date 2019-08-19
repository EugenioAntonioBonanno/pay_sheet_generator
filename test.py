import os

from lib.application import ApplicationFactory
import config


def test():
    test_pay_sheet = os.path.join(config.PAY_SHEET_EXPORT_DIR, "test_pay_sheet.xlsx")
    if os.path.isfile(test_pay_sheet):
        os.remove(test_pay_sheet)

    if os.path.isfile(config.USER_DB_PATH):
        os.remove(config.USER_DB_PATH)

    test_schedule_path = os.path.join(config.USER_SCHEDULES_DIR, "test")
    if os.path.isfile(test_schedule_path):
        os.remove(test_schedule_path)

    app = ApplicationFactory.mock()
    app.run()


if __name__ == "__main__":
    test()
