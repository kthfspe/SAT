from github import Github
import base64
import os
import xml.etree.ElementTree as ET
from tinydb import TinyDB   
from scripts import filepath
import json

class DataManager:
    raw_physical = []
    raw_functional = []
    merged_physical = []
    merged_functional = []
    data_physical = []
    data_functional = []


    def __init__(self):
        pass

    def buildmodel(self, rp, rf):
        pass

    def loadrawdb(self, rp, rf):
        self.raw_physical = rp
        self.raw_functional = rf
        with open("raw_pdb.json", 'w') as fout:
            json.dump(self.raw_physical, fout)

        with open('raw_pdb.json', 'r') as fp:
            data = json.load(fp)


        with open("raw_fdb.json", 'w') as fout:
            json.dump(self.raw_functional, fout)

        with open('raw_fdb.json', 'r') as fp:
            data = json.load(fp)
        #self.raw_pdb.insert_multiple(rp)
        #Load to json file locally and return path and status

