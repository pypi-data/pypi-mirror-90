# encoding = utf-8

class Telegram():
    def __init__(self):
        self.server = ""
        self.username = ""
        self.password = ""
        self.to = [] # string list

    def dump(self):
        return self.__dict__