import os

debug = True

if debug == False:
    defaultrepo = "kthfspe/SA"
    defaultLVphy = "LV_architecture/LV_physical_architecture"
    defaultLVfun = "LV_architecture/LV_functional_architecture"
    defaultHVphy = "HV_architecture/HV_physical_architecture"
    defaultHVfun = "HV_architecture/HV_functional_architecture"
    defaultDVphy = "DV_architecture/DV_physical_architecture"
    defaultDVfun = "DV_architecture/DV_functional_architecture"

else:
    defaultrepo = "kthfspe/SA"
    defaultLVphy = "examples/LV_architecture/LV_physical_architecture"
    defaultLVfun = "examples/LV_architecture/LV_functional_architecture"
    defaultHVphy = "examples/HV_architecture/HV_physical_architecture"
    defaultHVfun = "examples/HV_architecture/HV_functional_architecture"
    defaultDVphy = "examples/DV_architecture/DV_physical_architecture"
    defaultDVfun = "examples/DV_architecture/DV_functional_architecture"


os.chdir("..")
db_path = os.getcwd() + "/db"
source_path = os.getcwd()
os.chdir("src")
