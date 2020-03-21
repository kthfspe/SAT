import satconfig
from dbmanager import DBManager

def searchnameapp(nametosearch):
    dbm = DBManager()
    dbm.readdb()
    data = dbm.getdata()
    return data['namedata'][nametosearch]