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
    db = TinyDB('db.json')
    def __init__(self):
        pass

    def loaddb(self, rp, rf, parentdir):
        self.raw_physical = rp
        self.raw_functional = rf
        print(parentdir)
        #Load to json file locally and return path and status
