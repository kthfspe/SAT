from dbmanager import DBManager

def producttreeapp(config):
    dbm = DBManager(config)
    dbm.readdb()
    data = dbm.getdata()
    output = findallchildren(data, "CHASSIS", config)
    physicalproducttree = []
    functionalproducttree = []
    listprint(output, 0, physicalproducttree)
    return physicalproducttree

def listprint(li, level, output):
    if isinstance(li,list):
        for item in li:
            listprint(item, level+1, output)
    if isinstance(li, str):
        for i in range(0,level-1):
            li = "--> " + li
        print(li)
        output.append(li)

def findallchildren(data, parentname, config):
    childlist = []
    found = 0
    for item in data["globaliddata"]:
        if data["globaliddata"][item]["BlockType"] in config["physical_blocks"]:
            if data["globaliddata"][item]["Parent"] == parentname:
                found +=1
                childlist.append(data["globaliddata"][item]["Name"])
                subchildlist = findallchildren(data,data["globaliddata"][item]["Name"],config)
                if subchildlist != []:
                    childlist.append(subchildlist)
                subfunctionlist = findallfunctions(data, data["globaliddata"][item]["Name"], config)
                if subfunctionlist != []:
                    childlist.append(subfunctionlist)
    return childlist

def findallfunctions(data, name, config):
    output = []
    for item in data["globaliddata"]:
        if (data["globaliddata"][item]["BlockType"] in config["functional_blocks"]):
            if data["globaliddata"][item]["Allocation"] == name:
                output.append("F: " + data["globaliddata"][item]["Name"])
    return output