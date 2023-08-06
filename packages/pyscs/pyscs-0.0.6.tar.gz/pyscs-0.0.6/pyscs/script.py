# encoding=utf-8

import requests
import json

from pyscs.alertto import AlertTo



class Cron():
    def __init__(self):
        self.start = ""
        self.loop = 0
        self.isMonth = False


class LookPath():
    def __init__(self):
        self.command = ""
        self.path = ""
        self.install = ""

    def dump(self):
        return self.__dict__

class Script():
    def __init__(self, name, command):
        self.name = name                      
        self.dir = ""                      
        self.command = command                      
        self.get = ""                      
        self.replicate = 1                      
        self.always = False                      
        self.disableAlert = False                      
        self.env = {}                      
        self.continuityInterval = 3600                   
        self.port = 0                              
        self.loop = 0                           
        self.version = ""   
        self.disable = False                          
        # alert                 AlertTo           
        self.alert = AlertTo()
        self.cron = Cron()
        self.lookPath = []

    def add_lookPath(self, params: LookPath):
        self.lookPath.append(params.dump())

    def dump(self):
        # data = self.__dict__
        # print(self.alert.__dict__)
        self.alert = self.alert.dump()
        self.cron = self.cron.__dict__

        return self.__dict__
        
