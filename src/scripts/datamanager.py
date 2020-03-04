import os
from scripts import filepath, blocklist

class DataManager:
    raw_physical = []
    raw_functional = []
    corrected_functional = []
    corrected_physical = []
    physical_nameset = set()
    enclosure_list = set()
    function_list = set()
    error = []
    log = []
    status = 0
    iddata = dict()

    def __init__(self):
        pass

    def buildmodel(self, rf, rp):
        self.error = []
        self.status = 0
        self.corrected_functional = []
        self.corrected_physical = []
        self.raw_physical = rp
        self.raw_functional = rf

        # Remove ignored blocks from the global block list
        self.error.append("Building Model...")
        self.error.append("Removing blocks from ignorelist...")
        self.removeignoredblocks()
        # Status checker function

        # Checks for blocktypes outside of global blocklist
        self.error.append("Checking validity of BlockType field...")
        self.checkblockvalidity()

        # Check name validity: This is done separately from other fields as further checks are not possible
        # if 'Name' is missing
        self.error.append("Checking validity of Name field...")
        self.checknamevalidity()
        
        # Checks for floating signals
        self.error.append("Checking for floating signals...")
        self.checkfloatingsignals()
        
        
        # Create nameset
        # Creates a set of all names of all blocks in physical architecture
        self.createphysicalnameset()
        # Create enclosure list
        # Assumes all new parent values not in namelist as an enclosure
        self.createnclosurelist()
 
        # Assigns empty parents to CHASSIS
        # Checks if parent name is valid
        # Checks if parent type is valid
        self.error.append("Checking validity of Parent field...")
        self.checkparentvalidity()
        
       # Check if function name is not empty
        self.error.append("Checking validity of Function field...")
        self.checkfunctionvalidity()

        # Create function list
        self.createfunctionlist()

        # Check if allocation in funcitnla block is a valid name in physical block
        self.error.append("Checking validity of Allocation field...")
        self.checkallocationvalidity()

        # Update connector names to include the name of the parent
        self.updateconnectornames()

        # self.error.append("Merging data instances..")
        self.merge()
        self.createidlookup()
        return self.error, self.status

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
                self.error.append("ERROR: Invalid Block in file " + item["Filename"] + " with BlockType " + item["BlockType"] + \
                   ", Name " + item['Name'] + " and ID " + item["id"]  )
                self.status+=1
            else:
                self.corrected_physical.append(item)
        # Functional Architecture - Block Validity Checking
        for item in self.raw_functional:
            if item["BlockType"] not in blocklist.functional_blocktypes:
                self.error.append("ERROR: Invalid Block in file " + item["Filename"] + " with BlockType " + item["BlockType"] + \
                        ", Name " + item['Name'] + " and ID " + item["id"]  )
                self.status+=1
            else:
                self.corrected_functional.append(item)

    
    def checknamevalidity(self):
        faultf = []
        faultp = []
        for item in self.corrected_functional:
            if 'Name' not in item or item['Name']=='':
                self.error.append("ERROR: No name for block with ID: " + item['id'] + " in page " + item['PageName'] + " in file "\
                    + item['Filename'] )
                self.status+=1
                faultf.append(self.corrected_functional[self.corrected_functional.index(item)])
        tempf = [item for item in self.corrected_functional if item not in faultf]
        self.corrected_functional = tempf

        for item in self.corrected_physical:
            if ('Name' not in item) or (item['Name']==''):
                self.error.append("ERROR    : No name for block with ID: " + item['id'] + " in page " + item['PageName'] + " in file "\
                    + item['Filename'] )
                self.status+=1
                faultp.append(self.corrected_physical[self.corrected_physical.index(item)])
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
                    item['Parent'] = 'CHASSIS'

                if (item['Parent'] not in self.physical_nameset) and (item['Parent'] not in self.enclosure_list):
                    self.error.append("ERROR: Invalid parent in block " + item['Name'] + " in page " + item['PageName'] + " in file "\
                    + item['Filename'] )
                    self.status+=1
                else:
                    for parentitem in self.corrected_physical:
                        if parentitem['Name'] == item['Parent']:
                            if parentitem['BlockType'] not in blocklist.physical_blocks:
                                self.error.append("ERROR: Invalid parent type ("+ parentitem['Name']+', '+parentitem['BlockType'] +") in block " + item['Name'] + " in page " + item['PageName'] + " in file "\
                        + item['Filename'] )
                                self.status+=1
                                break
                            elif (item['BlockType'] == "OTSC" or item['BlockType'] =="SENS" or item['BlockType'] =="ACT" or item['BlockType'] =="HMI"):
                                if ((parentitem['BlockType'] != 'CHASSIS') or (parentitem['BlockType'] not in self.enclosure_list)):
                                    self.error.append("ERROR: Invalid parent type ("+ parentitem['Name']+', '+parentitem['BlockType'] +") in block " + item['Name'] + " in page " + item['PageName'] + " in file "\
                        + item['Filename'] )
                                    self.status+=1
                                    break
                            elif (item['BlockType'] == 'NCU' or item['BlockType'] == 'PCU') and ((item['Parent'] == 'CHASSIS') or (parentitem['Name'] not in self.enclosure_list)):
                                self.error.append("ERROR: Invalid parent type ("+ parentitem['Name']+', '+parentitem['BlockType'] +") in block " + item['Name'] + " in page " + item['PageName'] + " in file "\
                        + item['Filename'] )
                                self.status+=1
                                break

    
                                
    def checkfunctionvalidity(self):
        for item in self.corrected_functional:
            if item['Function'] == '':
                self.error.append("ERROR: Function name missing in block " + item['Name'] + " in page " + item['PageName'] + \
                    " in file " + item["Filename"] )
                self.status+=1


    def createnclosurelist(self):
        enclosurelist = []
        for item in self.corrected_physical:
            if item['BlockType'] in blocklist.physical_blocks:
                if item['Parent'] not in self.physical_nameset:
                    enclosurelist.append(item['Parent'])
        self.enclosure_list = set(enclosurelist)

    def createfunctionlist(self):
        functionlist = []
        for item in self.corrected_functional:
            if item['BlockType'] in blocklist.functional_blocks:
                functionlist.append(item['Function'])
        self.function_list = set(functionlist)

    def checkallocationvalidity(self):
        for item in self.corrected_functional:
            if item['BlockType'] in blocklist.functional_blocks:
                if item['Allocation'] == '':
                    self.error.append("ERROR: Allocation missing in block " + item['Name'] + " in page " + item['PageName']\
                        + " in file " + item['Filename'])
                    self.status+=1
                elif (item['Allocation'] not in self.physical_nameset): 
                    self.error.append("ERROR: Invalid allocation in block " + item['Name'] + " in page " + item['PageName']\
                        + " in file " + item['Filename'])
                    self.status+=1


    def updateconnectornames(self):
        for item in self.corrected_physical:
            if item['BlockType'] == "FCON" or item["BlockType"] == "MCON":
                item["Name"] = item["Parent"] + "/" + item["Name"]

    def merge(self):
        self.mergephysicaldata() 
        #self.mergedata(self.corrected_functional)

    def mergephysicaldata(self):
        ignorelist = []
        for item in self.corrected_physical:
            if item['BlockType'] not in blocklist.physical_blocks:
                ignorelist.append(item['id'])
        for item in self.corrected_physical:
            sublist = []
            if item['id'] not in ignorelist:
                ignorelist.append(item['id'])
                sublist.append(item)
                for i in range(self.corrected_physical.index(item)+1, len(self.corrected_physical)):
                    citem = self.corrected_physical[i]
                    if citem['id'] not in ignorelist:
                        subitem = {k:item[k]  for k in ('Name','BlockType','Parent')}
                        subcitem = {k:citem[k] for k in ('Name','BlockType','Parent')} 
                        if subitem == subcitem:
                            ignorelist.append(citem['id'])
                            sublist.append(citem)
            self.mergeblock(sublist)

    def mergeblock(self, instances):
        pass



    



                       
        # for each item as focus object
            # if index not in ignore list
                # set mergedinstances to zero
                # for all items after the focus object
                    # if current item not in ignore list
                        # if focus item and current item have same name and blocktype
                            # add index of current item to ignore list
                            # if focus item not equal to current item
                                # merge all fields
                                # add id of current item to focus item
                                # increment mergedinstances
                # add mergedinstances to focus item
        # remove all elements that are in index ignorelist
        # CHECK: Length of original data = length of final data + sum(merged instaces)
        

    def checkfloatingsignals(self):
        for item in self.corrected_functional:
            if item["BlockType"] == blocklist.functional_signals:
                if item["source"] == "" or item["target"] == "" or "source" not in item or "target" not in item:
                    self.error.append("ERROR: Floating Signal: " + item["Name"] + " in Page " + item["PageName"] + " in File " + \
                       item["Filename"]  )
                    self.status+=1
        for item in self.corrected_physical:
            if item["BlockType"] == blocklist.physical_signals:
                if item["source"] == "" or item["target"] == "" or "source" not in item or "target" not in item:
                    self.error.append("ERROR: Floating Signal: " + item["Name"] + " in Page " + item["PageName"] + " in File " + \
                       item["Filename"]  )
                    self.status+=1   

    
    def createidlookup(self):
        idphysical = {k['id']:k for k in self.corrected_physical }
        idfunctional = {k['id']:k for k in self.corrected_functional}
        idphysical.update(idfunctional)
        self.iddata = idphysical
