# encoding = utf-8

from pyscs.email import Email
from pyscs.telegram import Telegram
from pyscs.rocket import Rocket
from pyscs.weixin import WeiXin


class AlertTo():
    def __init__(self):
        self.email = Email()
        self.rocket = Rocket()
        self.telegram = Telegram()
        self.weixin = WeiXin()

    def dump(self):
        self.email = self.email.dump()
        self.rocket = self.rocket.dump()
        self.telegram = self.telegram.dump()
        self.weixin = self.weixin.dump()
        return self.__dict__