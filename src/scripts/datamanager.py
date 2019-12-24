from github import Github
import base64
import os
import xml.etree.ElementTree as ET

class DataManager:
    raw_physical = []
    raw_functional = []
    merged_physical = []
    merged_functional = []
    data_physical = []
    data_functional = []
    def __init__(self):
        pass

    def loaddb(self, raw_physical, raw_functional, parentdir):
        print(parentdir)