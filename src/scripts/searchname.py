import satconfig
from dbmanager import DBManager

def searchnameapp():
    dbm = DBManager()
    dbm.readdb()
    data = dbm.getdata()
    print("Search Name")