

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
    def __init__(self, week, days):
        self.days = days
        self.week = week