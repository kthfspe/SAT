import os
from scripts import filepath, blocklist


class DataManager:
    raw_physical = []
    raw_functional = []
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

        # create global lookup

        # mergedb

        # check consistency

    def checkblockvalidity(self):
        warning = []
        # Physical Architecture - Block Validity Checking
        for item in self.raw_physical:
            if item != None:
                if item["BlockType"] not in blocklist.physical_blocktypes:
                    warning.append("Invalid Block in Physical Architecture with BlockType " + item["BlockType"] + ", Name " + item['Name'] + " and ID " + item["id"]  )
       
        # Functional Architecture - Block Validity Checking
        for item in self.raw_functional:
            if item != None:
                if item["BlockType"] not in blocklist.functional_blocktypes:
                    warning.append("Invalid Block in Functional Architecture with BlockType " + item["BlockType"] + ", Name " + item['Name'] + " and ID " + item["id"]  )
        return warning

    def checkfieldvalidity(self):
        warning = []
        error = []

        raw_complete = self.raw_physical + self.raw_functional

        namelist = ['CHASSIS']
        for item in raw_complete:
            namelist.append(item['Name'])

        # print(namelist)
        
        for item in raw_complete:
            # Rules applying to all blocks

            # Check parent validity
            

            if 'Parent' in item:
                if item['Parent'] not in namelist:
                    print(item['Parent'])

            # Add source and destination for signals


            # Rules for each block type

        return error, warning





