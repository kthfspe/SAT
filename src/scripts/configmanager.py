import yaml

class ConfigManager:
    configdata = []
    def __init__(self):
        pass

    def loadconfigdata(self):
        with open(satconfig.config["configyamlfilename"], 'r') as file:
            documents = yaml.load(file)

    def saveconfigdata(self):
        if os.path.exists(satconfig.config["configyamlfilename"]):
            os.remove(satconfig.config["configyamlfilename"])
        with open(satconfig.config["configyamlfilename"], 'w') as file:
            documents = yaml.dump(satconfig.config, file)  



    