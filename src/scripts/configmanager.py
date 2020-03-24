import yaml
import os


class ConfigManager:
    configdata = []
    configfilepath = "config.yaml"
    def __init__(self):
        pass

    def loadconfigdata(self):
        with open(self.configfilepath, 'r') as file:
            self.configdata = yaml.load(file)

    def saveconfigdata(self):
        if os.path.exists(self.configfilepath):
            os.remove(self.configfilepath)
        with open(self.configfilepath, 'w') as file:
            yaml.dump(self.configdata, file)  

    def getappdata(self):
        return self.configdata["appdata"]

    def getappbyname(self, appname):
        for item in self.configdata["appdata"]:
            if item["apptitle"] == appname:
                return item



    