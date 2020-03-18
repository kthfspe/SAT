# Main configuration file for SAT app
# This can be used to create a settings page in the app so some of these can be changed via the web interface.

# App status
debug =  True

# GIT related
gitaccount = "kthfspe"
gitrepo = "SA"
gitpath = gitaccount + "/" + gitrepo

import os
from scripts import satconfig

if satconfig.debug == False:
    defaultrepo = "kthfspe/SA"
    defaultLVphy = "LV_architecture/LV_physical_architecture.drawio"
    defaultLVfun = "LV_architecture/LV_functional_architecture.drawio"
    defaultHVphy = "HV_architecture/HV_physical_architecture.drawio"
    defaultHVfun = "HV_architecture/HV_functional_architecture.drawio"
    defaultDVphy = "DV_architecture/DV_physical_architecture.drawio"
    defaultDVfun = "DV_architecture/DV_functional_architecture.drawio"

else:
    defaultrepo = "kthfspe/SA"
    defaultLVphy = "examples/LV_architecture/LV_physical_architecture"
    defaultLVfun = "examples/LV_architecture/LV_functional_architecture"
    defaultHVphy = "examples/HV_architecture/HV_physical_architecture"
    defaultHVfun = "examples/HV_architecture/HV_functional_architecture"
    defaultDVphy = "examples/DV_architecture/DV_physical_architecture"
    defaultDVfun = "examples/DV_architecture/DV_functional_architecture"

localrepo = "kthfspe/SA"
localLVphy = "LV_architecture/LV_physical_architecture.drawio"
localLVfun = "LV_architecture/LV_functional_architecture.drawio"
localHVphy = "HV_architecture/HV_physical_architecture.drawio"
localHVfun = "HV_architecture/HV_functional_architecture.drawio"
localDVfun = "DV_architecture/DV_functional_architecture.drawio"


db_path = os.getcwd() + "/db"
source_path = os.getcwd()
dbyamlfilename = "db/db.yaml"



ignore_blocktype = [ "FRAME", "IGNORE"]

physical_signals = ["DIG", "ANA", "CAN"]
functional_signals = ["FS"]

physical_blocks = ["SENS","OTSC","ECU","NCU","BAT","FCON","MCON","ACT","HMI","PCU"]
functional_blocks = ["ENVIN","ENVOUT","FE"]

physical_blocktypes = physical_blocks + physical_signals
functional_blocktypes = functional_blocks + functional_signals

defaultpowerlist = ["+24V", "+5V"]

mergefields_ignore_physical = ["id", "Filename", "PageName", "PageId", "MetaParent",  \
    "x", "y", "label", "placeholders", "edge", "MetaParent", "width", "relative", "as", "source_x", "source_y",\
       "target_x", "target_y", "target", "source" , "SourceName", "TargetName"]
mergefields_ignore_functional = ["id", "Filename", "PageName", "PageId", "MetaParent", "Allocation", \
    "x", "y", "label", "placeholders", "edge", "MetaParent", "width", "relative", "as", "source_x", "source_y",\
       "target_x", "target_y", "Function", "target" , "TargetName", "SourceName", "source"]
mergefields_concat = ["id", "Function", "target"]

#App list