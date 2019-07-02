import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(funcName)s:%(levelname)s:%(message)s")

file_handler = logging.FileHandler("logs.txt")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)


class SubbedSession:
    def __init__(self, code, length, date):
        self.code = code
        self.length = length
        self.date = date


class MonthlySpecificData:

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

    def get_classes_subbed(self, active_user):
        classes_subbed = []
        logger.debug(("\nHave you subbed any classes this month? \nInput \"done\" if you haven\"t or when finished entering"
                      " those you have.\n"
                      "If you have enter each class one at a time in the following format [class id length date] \n"
                      "ex: W34 2 13."))
        while True:
            logger.debug("Your current list of classes you have subbed this month is as follows:")
            for session in classes_subbed:
                logger.debug(session.code + " ")
            logger.debug("\n")
            subbed = input("Enter a class to add to your subbed classes, or \"done\" if you are finished:\n")
            logger.info((active_user + " entered:" + subbed))
            if subbed.lower() == "done":
                break
            else:
                try:
                    subbed = subbed.split(" ")
                    classes_subbed.append(SubbedSession(subbed[0], subbed[1], subbed[2]))
                    logger.info(active_user + " added " + subbed + "to their list of classes they subbed.")
                except:
                    logger.debug("Sorry but you entered that class in incorrectly, it won\"t be added. Please try again")

        return classes_subbed

