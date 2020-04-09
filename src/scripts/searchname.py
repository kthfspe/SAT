from dbmanager import DBManager

def searchnameapp(nametosearch, config):
    dbm = DBManager(config)
    dbm.readdb()
    data = dbm.getdata()
    result = []
    for globalid in data['globaliddata'].keys():
        if data['globaliddata'][globalid]['Name'].lower() == nametosearch.lower():
            result.append(data['globaliddata'][globalid])
    if result != []:
        return result
    else:
        return {"Message":"Name not found!"}