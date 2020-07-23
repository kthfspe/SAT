import sys
import os
sys.path.insert(0,os.getcwd()+"/scripts")
#from flask import Flask, url_for, render_template, request, redirect           # lirbrary used to make the web application
from gitmanager import GitManager                                               # class that can read in github files and parse xml files
from datamanager import DataManager                                             # manages the parsed data, checks validity nad merges data
from dbmanager import DBManager                                                 # managing of database
from configmanager import ConfigManager                                         # managing all the block configurations, defaults and things that makes it compatible with the used draw.io library
import yaml                                                                     # to enable the use of yaml files (data structures)
import searchname, findfield, producttree                                       # developed tools



gitman = GitManager()
dataman = DataManager()
configman = ConfigManager()


# Steal Access Token
with open('AccessToken.txt', 'r') as AT:
    my_access_token = AT.readline()
    AT.close()

# Logging in to Github
Logged_in = gitman.gitlogin(my_access_token, configman.configdata)


if configman.configdata["debug"] == True:
    prefix = 'example'
else:
    prefix = 'default'

raw_functional =\
    gitman.readfile(configman.configdata[prefix + "LVfun"])+\
    gitman.readfile(configman.configdata[prefix + "HVfun"])+\
    gitman.readfile(configman.configdata[prefix + "DVfun"])

raw_physical =\
    gitman.readfile(configman.configdata[prefix + "LVphy"])+\
    gitman.readfile(configman.configdata[prefix + "HVphy"])+\
    gitman.readfile(configman.configdata[prefix + "DVphy"])
# with open('spy.yaml', 'w') as spy_file:
#     documents = yaml.dump(raw_functional, spy_file)
#     spy_file.close()

# Build model
buildmodelerror, buildmodelstatus = dataman.buildmodel(raw_functional, raw_physical, configman.configdata)

# Log errors to file
with open('db/errors.yaml', 'w') as errorlog:
    documents = yaml.dump(buildmodelerror, errorlog)
    errorlog.close()


# print(buildmodelerror, buildmodelstatus)
# for item in dataman.corrected_physical:
#     if item['BlockType'] == 'ENC':
#         print(item['Name'])
