# Main configuration file for SAT app
# This can be used to create a settings page in the app so some of these can be changed via the web interface.
config = dict()
# App status
config["debug"] = True #To choose between example files or default files
config["appdebug"] = True #to run flask server in debug mode with verbose error pages

# GIT related
config["gitaccount"] = "kthfspe"
config["gitrepo"] = "SA"

config["defaultLVphy"] = "LV_architecture/LV_physical_architecture.drawio"
config["defaultLVfun"] = "LV_architecture/LV_functional_architecture.drawio"
config["defaultHVphy"] = "HV_architecture/HV_physical_architecture.drawio"
config["defaultHVfun"] = "HV_architecture/HV_functional_architecture.drawio"
config["defaultDVphy"] = "DV_architecture/DV_physical_architecture.drawio"
config["defaultDVfun"] = "DV_architecture/DV_functional_architecture.drawio"
config["exampleLVphy"] = "examples/LV_architecture/LV_physical_architecture"
config["exampleLVfun"] = "examples/LV_architecture/LV_functional_architecture"
config["exampleHVphy"] = "examples/HV_architecture/HV_physical_architecture"
config["exampleHVfun"] = "examples/HV_architecture/HV_functional_architecture"
config["exampleDVphy"] = "examples/DV_architecture/DV_physical_architecture"
config["exampleDVfun"] = "examples/DV_architecture/DV_functional_architecture"

config["settingspagefields"] = ["debug","gitaccount", "gitrepo", "defaultLVphy", "defaultLVfun", "defaultHVphy",\
     "defaultHVfun", "defaultDVfun", "defaultDVphy", "exampleLVphy", "exampleLVfun", "exampleHVphy",\
     "exampleHVfun", "exampleDVfun", "exampleDVphy", "dbyamlfilename"     ]

config["settingspagelistfields"] = ["ignore_blocktype", "physical_signals", "physical_blocks", "functional_signals",\
    "functional_blocks","defaultpowerlist", "mergefields_ignore_physical", "mergefields_ignore_functional",\
        "mergefields_concat"]

config["dbyamlfilename"] = "db/db.yaml"
config["configyamlfilename"] = "config.yaml"

config["ignore_blocktype"] = [ "FRAME", "IGNORE"]

config["physical_signals"] = ["DIG", "ANA", "CAN"]
config["functional_signals"] = ["FS"]

config["physical_blocks"] = ["SENS","OTSC","ECU","NCU","BAT","FCON","MCON","ACT","HMI","PCU"]
config["functional_blocks"] = ["ENVIN","ENVOUT","FE"]


config["defaultpowerlist"] = ["+24V", "+5V"]

config["mergefields_ignore_physical"] = ["id", "Filename", "PageName", "PageId", "MetaParent",  \
    "x", "y", "label", "placeholders", "edge", "MetaParent", "width", "relative", "as", "source_x", "source_y",\
       "target_x", "target_y", "target", "source" , "SourceName", "TargetName"]
config["mergefields_ignore_functional"] = ["id", "Filename", "PageName", "PageId", "MetaParent", "Allocation", \
    "x", "y", "label", "placeholders", "edge", "MetaParent", "width", "relative", "as", "source_x", "source_y",\
       "target_x", "target_y", "Function", "target" , "TargetName", "SourceName", "source"]
config["mergefields_concat"] = ["id", "Function", "target"]

config["appdata"] = [{
    "appname": "Search By Name",
    "apptitle":"searchbyname",
    "appsubtitle":"Search any block or signal by name",
    "appbutton":"Go",
    "appfunctionname":"searchname.searchnameapp",
    "apppage":"/searchbyname",
    "apphelptext":"Only the exact string match will be searched for. Not case sensitive",
}, {
    "appname": "Find",
    "apptitle":"findfield",
    "appsubtitle":"Find a string in any field in the DB",
    "appbutton":"Go",
    "appfunctionname":"findfield.findfieldapp",
    "apppage":"/findfield",
    "apphelptext": "Checks for all fields",
}
]