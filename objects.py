
class Day:
    def __init__(self, name, sessions):
        self.name = name
        self.sessions = sessions


class Session:
    def __init__(self, code, length, day_taught):
        self.code = code
        self.length = length
        self.day_taught = day_taught


class User:
    def __init__(self, user_name, week):
        self.user_name = user_name
        self.week = week  #list of day objects

class SubbedSession:
    def __init__(self, code, length, date):
        self.code = code
        self.length = length
        self.date = date
