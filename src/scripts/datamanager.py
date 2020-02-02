import os
from scripts import filepath, blocklist


class DataManager:
    raw_physical = []
    raw_functional = []
    corrected_functional = []
    corrected_physical = []
    physical_nameset = set()
    enclosure_list = set()
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

        # Check name validity: This is done separately from other fields as further checks are not possible
        # if 'Name' is missing
        self.checknamevalidity()

        # Create nameset
        # Creates a set of all names of all blocks in physical architecture
        self.createphysicalnameset()

        # Create enclosure list
        # Assumes all new parent values not in namelist as an enclosure
        self.createnclosurelist()

        # Assigns empty parents to CHASSIS
        # Checks if parent name is valid
        # Checks if parent type is valid
        self.checkparentvalidity()

        return self.error, self.warning
        # Create function list

        # Check function validity

        # Check allocations in functional architecture are vaild and in physical

        # Generate power supply list

        # Merge database

        # Block wise checks



    def removeignoredblocks(self):  
        # Remove blocks to be ignored
        # This function can be refactored to use del operator to remove elements
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
        # This function can be refactored to use del operator to remove elements and use the same data structure
        # Physical Architecture - Block Validity Checking
        for item in self.raw_physical:
            if item["BlockType"] not in blocklist.physical_blocktypes:
                self.warning.append("REMOVED: Invalid Block in file " + item["Filename"] + " with BlockType " + item["BlockType"] + \
                   ", Name " + item['Name'] + " and ID " + item["id"]  )
            else:
                self.corrected_physical.append(item)
        # Functional Architecture - Block Validity Checking
        for item in self.raw_functional:
            if item["BlockType"] not in blocklist.functional_blocktypes:
                self.warning.append("REMOVED: Invalid Block in file " + item["Filename"] + " with BlockType " + item["BlockType"] + \
                        ", Name " + item['Name'] + " and ID " + item["id"]  )
            else:
                self.corrected_functional.append(item)

    
    def checknamevalidity(self):
        faultf = []
        faultp = []
        for item in self.corrected_functional:
            if 'Name' not in item or item['Name']=='':
                self.error.append("REMOVED: No name for block with ID: " + item['id'] + " in page " + item['PageName'] + " in file "\
                    + item['Filename'] )
                faultf.append(self.corrected_functional[self.corrected_functional.index(item)])
        tempf = [item for item in self.corrected_functional if item not in faultf]
        self.corrected_functional = tempf

        for item in self.corrected_physical:
            if ('Name' not in item) or (item['Name']==''):
                self.error.append("REMOVED: No name for block with ID: " + item['id'] + " in page " + item['PageName'] + " in file "\
                    + item['Filename'] )
                faultp.append(corrected_physical[self.corrected_physical.index(item)])
        tempp = [item for item in self.corrected_physical if item not in faultp]
        self.corrected_physical = tempp

    def createphysicalnameset(self):
        namelist = ['CHASSIS']
        for item in self.corrected_physical:
            if item['BlockType'] in blocklist.physical_blocks:
                namelist.append(item['Name'])
        self.physical_nameset = set(namelist)

    
    def checkparentvalidity(self):
        for item in self.corrected_physical:
            if item['BlockType'] in blocklist.physical_blocks:
                if item['Parent'] == '':
                    item['Parent'] == 'CHASSIS'
                if (item['Parent'] not in self.physical_nameset) and (item['Parent'] not in self.enclosure_list):
                    self.error.append("ERROR: Invalid parent in block " + item['Name'] + " in page " + item['PageName'] + " in file "\
                    + item['Filename'] )
                else:
                    for parentitem in self.corrected_physical:
                        if parentitem['Name'] == item['Parent']:
                            if parentitem['BlockType'] not in blocklist.physical_blocks:
                                self.error.append("ERROR: Invalid parent type in block " + item['Name'] + " in page " + item['PageName'] + " in file "\
                        + item['Filename'] )
                            elif (item['BlockType'] == "OTSC" or "SENS" or "ACT" or "HMI") and ((parentitem['BlockType'] != 'CHASSIS') or \
                                (parentitem['BlockType'] not in self.enclosure_list)):
                                self.error.append("ERROR: Invalid parent type in block " + item['Name'] + " in page " + item['PageName'] + " in file "\
                        + item['Filename'] )
                            elif (item['BlockType'] == 'NCU' or 'PCU') and ((item['Parent'] == 'CHASSIS') or (parenitem['Name'] not in self.enclosure_list)):
                                self.error.append("ERROR: Invalid parent type in block " + item['Name'] + " in page " + item['PageName'] + " in file "\
                        + item['Filename'] )
                                

    def createnclosurelist(self):
        enclosurelist = []
        for item in self.corrected_physical:
            if item['BlockType'] in blocklist.physical_blocks:
                if item['Parent'] not in self.physical_nameset:
                    enclosurelist.append(item['Parent'])
        self.enclosure_list = set(enclosurelist)



