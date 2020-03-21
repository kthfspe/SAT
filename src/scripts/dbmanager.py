import os
import satconfig
import yaml

class DBManager:
    
    data = dict()
    def __init__(self):
        pass

    def readdb(self):
        with open(satconfig.config["dbyamlfilename"], 'r') as file:
            self.data.update(yaml.load(file))

    def getdata(self):
        return self.data


    