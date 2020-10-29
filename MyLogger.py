import datetime
import logging
import os


def get_date_and_time():
    x = datetime.datetime.now()
    return x.strftime("%d.%m.%Y %H:%M:%S")


def get_only_date():
    x = datetime.datetime.now()
    return x.strftime("%d.%m.%Y")


def get_only_time():
    x = datetime.datetime.now()
    return x.strftime("%H:%M:%S")


class MyLogging:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Tuka namiram tekushtata rabotna direktoriq
        # moe se bugne na laptopa
        # TRQBVA DA IMA PAPKA logs !!!!!!!
        dir_path = os.path.dirname(os.path.realpath(__file__))
        handler = logging.FileHandler(dir_path + '\logs\\' + get_only_date() + ".log")

        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_follow(self, username):
        log_message = get_only_time() + " FOLLOWED   " + username
        self.logger.info(log_message)

    def log_unfollow(self, username):
        log_message = get_only_time() + " UNFOLLOWED " + username
        self.logger.info(log_message)

    def log_like(self):
        log_message = get_only_time() + " LIKED "
        self.logger.info(log_message)
