from dbmanager import DBManager

def searchnameapp(nametosearch, config):
    dbm = DBManager(config)
    dbm.readdb()
    data = dbm.getdata()
    for item in data['globaliddata']:
        if item.lower() == nametosearch.lower():
            return data['globaliddata'][item]
    return {"Message":"Name not found!"}