import os

debug = False

if debug == False:
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

