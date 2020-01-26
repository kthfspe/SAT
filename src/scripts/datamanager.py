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
        print(self.warning)

        # check all fields

        # create global lookup
        
        # mergedb

        # check consistency

    def checkblockvalidity(self):
        warning = []
        # Physical Architecture - Block Validity Checking
        for item in self.raw_physical:
            if item != None:
                if item["BlockType"] not in blocklist.physical_blocktypes:
                    warning.append("Invalid Block in physical architecture with BlockType " + item["BlockType"] + " and ID " + item["id"]  )
       
        # Functional Architecture - Block Validity Checking
        for item in self.raw_functional:
            if item != None:
                if item["BlockType"] not in blocklist.functional_blocktypes:
                    warning.append("Invalid Block in functional architecture with BlockType " + item["BlockType"] + " and ID " + item["id"]  )

        return 






