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
    warning = []
    error = []

    def __init__(self):
        pass

    def buildmodel(self, rf, rp):
        self.raw_physical = rp
        self.raw_functional = rf

        # Remove ignored blocks from the global block list
        self.removeignoredblocks()

        # Checks for blocktypes outside of global blocklist
        self.checkblockvalidity()

        # Checks for all rules applying to attribute fields
        self.checkfieldvalidity()
        
        # create global lookup

        # mergedb

        # check consistency

        # self.status == 0 if all ok, else == 1
        # return self.error, self.warning

    def removeignoredblocks(self):  
        # Remove blocks to be ignored
        tempf = []
        tempp = []
        for item in self.raw_functional:
            if item['BlockType'] not in blocklist.ignore_blocktype:
                tempf.append(item)
        self.raw_functional = tempf
        for item in self.raw_physical:
            if item['BlockType'] not in blocklist.ignore_blocktype:
                tempp.append(item)
        self.raw_physical = tempp

    def checkblockvalidity(self):
        # Physical Architecture - Block Validity Checking
        for item in self.raw_physical:
            if item["BlockType"] not in blocklist.physical_blocktypes:
                self.warning.append("Invalid Block in Physical Architecture with BlockType " + item["BlockType"] + \
                   ", Name " + item['Name'] + " and ID " + item["id"]  )
            else:
                self.corrected_raw_physical.append(item)
        # Functional Architecture - Block Validity Checking
        for item in self.raw_functional:
            if item["BlockType"] not in blocklist.functional_blocktypes:
                self.warning.append("Invalid Block in Functional Architecture with BlockType " + item["BlockType"] + \
                        ", Name " + item['Name'] + " and ID " + item["id"]  )
            else:
                self.corrected_raw_functional.append(item)

    


    def checkfieldvalidity(self):

        raw_complete = self.corrected_raw_physical + self.corrected_raw_functional
        print(raw_complete)
        #namelist = ['CHASSIS']
        #for item in raw_complete:
        #    namelist.append(item['Name'])

        # print(self.warning)
        for item in raw_complete:
            # Global Rules(GR) - Rules applying to all blocks

            # GR1: Name exists and is non-empty
            if 'Name' not in item or item['Name']=='':
                self.error.append("No name for block with ID: " + item['id'] + " in page " + item['pagename'])

            # GR2: Check parent validity
            #if 'Parent' in item:
            #    if item['Parent'] not in namelist:
            #        print(item['Parent'])

            
            

            # Rules for each block type







