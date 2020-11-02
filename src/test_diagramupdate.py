import sys
import os
sys.path.insert(0,os.getcwd()+"/scripts")
#from flask import Flask, url_for, render_template, request, redirect           # lirbrary used to make the web application
# from gitmanager import GitManager                                               # class that can read in github files and parse xml files
#from datamanager import DataManager                                             # manages the parsed data, checks validity nad merges data
#from dbmanager import DBManager                                                 # managing of database
from configmanager import ConfigManager                                         # managing all the block configurations, defaults and things that makes it compatible with the used draw.io library
import yaml                                                                     # to enable the use of yaml files (data structures)
import searchname, findfield, producttree                                       # developed tools
from diagrammanager import DiagramManager                                       # managing diagrams


# gitman = GitManager()
#dataman = DataManager()
configman = ConfigManager()

update_configman = ConfigManager()
update_configman.configfilepath = 'scripts/diagramupdate_config.yaml'
update_configman.loadconfigdata()


# Steal Access Token
with open('AccessToken.txt', 'r') as AT:
    my_access_token = AT.readline()
    AT.close()

# Logging in to Github
diagramman = DiagramManager(update_configman.configdata)
Logged_in = diagramman.gitlogin(my_access_token)
diagramman.update_diagram_to_library()

#diagram_filepath = update_configman.configdata['diagram_directory'] + update_configman.configdata['diagram_filename']
#diagram_filepath = 'examples/LV_architecture/LV_physical_architecture'

# diagram_stringcontents = gitman.file2stringcontents(diagram_filepath)
# diagram_xml_contents = gitman.readfile(diagram_filepath)
