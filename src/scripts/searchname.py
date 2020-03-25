from dbmanager import DBManager

def searchnameapp(nametosearch, config):
    dbm = DBManager(config)
    dbm.readdb()
    data = dbm.getdata()
    result = []
    for item in data['globaliddata'].keys():
        if data['globaliddata'][item]['Name'].lower() == nametosearch.lower():
            result.append(data['globaliddata'][item])
    if result != []:
        return result
    else:
        return {"Message":"Name not found!"}