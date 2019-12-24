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
    raw_pdb = TinyDB(filepath.db_path+"/raw_pdb.json")
    merged_pdb = TinyDB(filepath.db_path+"/merged_pdb.json")
    pdb = TinyDB(filepath.db_path+"/pdb.json")
    raw_fdb = TinyDB(filepath.db_path+"/raw_fdb.json")
    merged_fdb = TinyDB(filepath.db_path+"/merged_fdb.json")
    fdb = TinyDB(filepath.db_path+"/fdb.json")

    def __init__(self):
        pass

    def loadrawdb(self, rp, rf):
        self.raw_physical = rp
        self.raw_functional = rf
        
        #Load to json file locally and return path and status
