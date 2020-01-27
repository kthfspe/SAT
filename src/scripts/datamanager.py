import os
from scripts import filepath, blocklist


class DataManager:
    raw_physical = []
    raw_functional = []
    corrected_raw_functional = []
    corrected_raw_physical = []
    merged_physical = []
    merged_functional = []
    data_physical = []
    data_functional = []


    def __init__(self):
        pass

    def buildmodel(self, rf, rp):
        self.raw_physical = rp
        self.raw_functional = rf

        # check blockvalidity
        self.warning = self.checkblockvalidity()

        # check all fields
        self.error, w = self.checkfieldvalidity()
        self.warning = self.warning + w

        # add source and destination to all signals


        # create global lookup

        # mergedb

        # check consistency

    def checkblockvalidity(self):
        warning = []
        # Physical Architecture - Block Validity Checking
        for item in self.raw_physical:
            if item != None and item["BlockType"] not in blocklist.ignore_blocktype:
                if item["BlockType"] not in blocklist.physical_blocktypes:
                    warning.append("Invalid Block in Physical Architecture with BlockType " + item["BlockType"] + ", Name " + item['Name'] + " and ID " + item["id"]  )
                else:
                    self.corrected_raw_physical.append(item)
        # Functional Architecture - Block Validity Checking
        for item in self.raw_functional:
            if item != None and item["BlockType"] not in blocklist.ignore_blocktype:
                if item["BlockType"] not in blocklist.functional_blocktypes:
                    warning.append("Invalid Block in Functional Architecture with BlockType " + item["BlockType"] + ", Name " + item['Name'] + " and ID " + item["id"]  )
                else:
                    self.corrected_raw_functional.append(item)
        return warning

    def checkfieldvalidity(self):
        warning = []
        error = []

        raw_complete = self.corrected_raw_physical + self.corrected_raw_functional

        namelist = ['CHASSIS']
        for item in raw_complete:
            namelist.append(item['Name'])

        # print(namelist)
        
        for item in raw_complete:
            # Global Rules(GR) - Rules applying to all blocks

            # GR1: Check parent validity
            if 'Parent' in item:
                if item['Parent'] not in namelist:
                    # print(item['Parent'])
                    pass

            # Rules for each block type

        return error, warning





