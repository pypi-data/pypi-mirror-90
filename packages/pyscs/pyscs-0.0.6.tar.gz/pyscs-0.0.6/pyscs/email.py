# encoding = utf-8

class Email():
    def __init__(self):
        self.nickname = ""
        self.host = ""
        self.port = ""
        self.username = ""
        self.password = ""
        self.to = [] # string list

    def dump(self):
        return self.__dict__