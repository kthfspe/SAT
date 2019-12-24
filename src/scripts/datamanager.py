from github import Github
import base64
import os
import xml.etree.ElementTree as ET
from tinydb import TinyDB   
from scripts import filepath


class DataManager:
    raw_physical = []
    raw_functional = []
    merged_physical = []
    merged_functional = []
    data_physical = []
    data_functional = []
    raw_db = TinyDB(filepath.db_path+"/raw_db.json")
    merged_db = TinyDB(filepath.db_path+"/merged_db.json")
    db = TinyDB(filepath.db_path+"/db.json")

    def __init__(self):
        pass

    def loadrawdb(self, rp, rf):
        self.raw_physical = rp
        self.raw_functional = rf
        #Load to json file locally and return path and status
