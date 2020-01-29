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
    level = 0

    def __init__(self):
        pass

    def buildmodel(self, rf, rp):
        self.raw_physical = rp
        self.raw_functional = rf

        # Remove ignored blocks from the global block list
        self.removeignoredblocks()

        # Checks for blocktypes outside of global blocklist
        self.checkblockvalidity()

        # Check name validity: This is done separately from other fields as further checks are not possible
        # if 'Name' is missing
        self.checknamevalidity()

        # Checks for all rules applying to attribute fields 
        # Can be split in pre global check, block attribute check, post global check
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
                self.warning.append("Invalid Block in file " + item["Filename"] + " with BlockType " + item["BlockType"] + \
                   ", Name " + item['Name'] + " and ID " + item["id"]  )
            else:
                self.corrected_raw_physical.append(item)
        # Functional Architecture - Block Validity Checking
        for item in self.raw_functional:
            if item["BlockType"] not in blocklist.functional_blocktypes:
                self.warning.append("Invalid Block in file " + item["Filename"] + " with BlockType " + item["BlockType"] + \
                        ", Name " + item['Name'] + " and ID " + item["id"]  )
            else:
                self.corrected_raw_functional.append(item)

    
    def checknamevalidity(self):
        raw_complete = self.corrected_raw_functional + self.corrected_raw_physical

        for item in raw_complete:
            if 'Name' not in item or item['Name']=='':
                self.error.append("No name for block with ID: " + item['id'] + " in page " + item['PageName'])
        
        if self.error != []:
            return 1
        else:
            return 0

    def checkfieldvalidity(self):

        raw_complete = self.corrected_raw_physical + self.corrected_raw_functional

        #namelist = ['CHASSIS']
        #for item in raw_complete:
        #    namelist.append(item['Name'])

        # print(self.warning)
        # for item in raw_complete:
            # Global Rules(GR) - Rules applying to all blocks

            # GR1: Name exists and is non-empty


            # GR2: Check parent validity
            #if 'Parent' in item:
            #    if item['Parent'] not in namelist:
            #        print(item['Parent'])

            
            

            # Rules for each block type







