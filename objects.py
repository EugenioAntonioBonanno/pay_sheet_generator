

class Day:
    def __init__(self, name, sessions):
        self.name = name
        self.sessions = sessions


class Session:
    def __init__(self, code, length, time):
        self.code = code
        self.length = length
        self.time = time