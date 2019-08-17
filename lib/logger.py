import logging


class Logger:

    @staticmethod
    def get_logger(name):
        logger = logging.getLogger(name)
        logging.basicConfig(format="%(message)s", level=logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s:%(name)s:%(funcName)s:%(levelname)s:%(message)s")

        file_handler = logging.FileHandler("logs.txt")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        logger.addHandler(file_handler)
        return logger
