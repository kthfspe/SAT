import satconfig
from dbmanager import DBManager

def searchnameapp(nametosearch):
    dbm = DBManager()
    dbm.readdb()
    data = dbm.getdata()
    for item in data['namedata']:
        if item.lower() == nametosearch.lower():
            return data['namedata'][item]
    return {"Message":"Name not found!"}