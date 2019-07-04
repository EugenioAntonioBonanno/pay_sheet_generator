import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(funcName)s:%(levelname)s:%(message)s")

file_handler = logging.FileHandler("logs.txt")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)


class ExtraSession:
    def __init__(self, code, length, date):
        self.code = code
        self.length = length
        self.date = date


class MonthSpecificData:

    def get_days_missed(self, active_user):
        days_to_skip = []
        logger.debug("Enter any days you missed work due to sickness or holiday as a number. "
                     "[ex \"12\"] for the 12th or enter \"done\". \n")

        while True:

            logger.debug("Your current missed days are as follows: " + str(days_to_skip))
            missed_work = input("Enter a missed day as a number or \"done\" to move on. \n")
            logger.info(active_user + " added " + missed_work + " to their list of days they did not work ")
            logger.info((active_user + " entered:" + missed_work))
            if missed_work.lower() == "done":
                break
            else:
                days_to_skip.append(int(missed_work))

        return days_to_skip

    def get_extra_session_worked(self, active_user):
        extra_sessions_worked = []
        logger.debug(("\nHave you subbed any classes this month? \nInput \"done\" if you haven\"t or when finished entering"
                      " those you have.\n"
                      "If you have enter each class one at a time in the following format [class id length date] \n"
                      "ex: W34 2 13."))
        while True:
            logger.debug("Your current list of classes you have subbed this month is as follows:")
            for session in extra_sessions_worked:
                logger.debug(session.code + " ")
            logger.debug("\n")
            extra_session = input("Enter a class to add to your subbed classes, or \"done\" if you are finished:\n")
            logger.info((active_user + " entered:" + extra_session))
            if extra_session.lower() == "done":
                break
            else:
                try:
                    extra_session_split = extra_session.split(" ")
                    extra_sessions_worked.append(ExtraSession(extra_session_split[0], extra_session_split[1], extra_session_split[2]))
                    logger.info(active_user + " added " + extra_session + "to their list of classes they subbed.")
                except:
                    logger.debug("Sorry but you entered that class in incorrectly, it won\"t be added. Please try again")

        return extra_sessions_worked


    def get_days_missed(self, active_user):
        days_to_skip = []
        logger.debug("Enter any days you missed work due to sickness or holiday as a number. "
                     "[ex \"12\"] for the 12th or enter \"done\". \n")

        while True:

            logger.debug("Your current missed days are as follows: " + str(days_to_skip))
            missed_work = input("Enter a missed day as a number or \"done\" to move on. \n")
            logger.info(active_user + " added " + missed_work + " to their list of days they did not work ")
            logger.info((active_user + " entered:" + missed_work))
            if missed_work.lower() == "done":
                break
            else:
                days_to_skip.append(int(missed_work))

        return days_to_skip

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

    def get_monthly_meetings(self, active_user):
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