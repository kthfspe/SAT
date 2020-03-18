import os
from scripts import satconfig
import yaml

class DataManager:
    raw_physical = []
    raw_functional = []
    corrected_functional = []
    corrected_physical = []
    physical_nameset = set()
    enclosure_list = set()
    function_list = set()
    power_set = set()
    gnd_set = set()
    error = []
    log = []
    actual_error_count = 0
    iddata = dict()
    globaliddata = dict()
    namedata = dict()

    def __init__(self):
        pass

    def buildmodel(self, rf, rp):
        self.error = []
        self.actual_error_count = 0
        self.corrected_functional = []
        self.corrected_physical = []
        self.raw_physical = rp
        self.raw_functional = rf

        # Remove ignored blocks from the global block list
        self.error.append("Building Model...")
        self.error.append("Removing blocks from ignorelist...")
        self.removeignoredblocks()

        # Status checker function

        # Checks for blocktypes outside of global satconfig
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

        # Create a Lookup where the id is the key
        self.createidlookup()

        # Replaces id in sources and targets of all signals to names of the block
        self.replacesourcetargetid()

        # Merging redundant data instances
        self.error.append("Merging data instances..")
        self.mergefunctionaldata() 
        self.mergephysicaldata()

        # Adds a global id to all elements and creates a lookup with globalid as key      
        self.createglobalidlookup()

        # Creates a lookup with the name as the key
        self.createnamelookup()

        # Creates a set of all power supply elements
        self.createpowerset()

        # Blockwise checks

        # Creates final data structure and writes it to yaml files
        self.createdatafile()      

        return self.error, self.actual_error_count

    def removeignoredblocks(self):  
        # Remove blocks to be ignored
        # This function can be refactored to use del operator to remove elements
        tempf = []
        tempp = []
        for item in self.raw_functional:
            if item['BlockType'] not in satconfig.ignore_blocktype:
                tempf.append(item)
        self.raw_functional = tempf
        for item in self.raw_physical:
            if item['BlockType'] not in satconfig.ignore_blocktype:
                tempp.append(item)
        self.raw_physical = tempp

    def checkblockvalidity(self):
        # This function can be refactored to use del operator to remove elements and use the same data structure
        # Physical Architecture - Block Validity Checking
        for item in self.raw_physical:
            if item["BlockType"] not in satconfig.physical_blocktypes:
                self.error.append("ERROR: Invalid Block in file " + item["FileName"] + " with BlockType " + item["BlockType"] + \
                   ", Name " + item['Name'] + " and ID " + item["id"]  )
                self.actual_error_count+=1
            else:
                self.corrected_physical.append(item)

        # Functional Architecture - Block Validity Checking
        for item in self.raw_functional:
            if item["BlockType"] not in satconfig.functional_blocktypes:
                self.error.append("ERROR: Invalid Block in file " + item["FileName"] + " with BlockType " + item["BlockType"] + \
                        ", Name " + item['Name'] + " and ID " + item["id"]  )
                self.actual_error_count+=1
            else:
                self.corrected_functional.append(item)

    
    def checknamevalidity(self):
        faultf = []
        faultp = []
        for item in self.corrected_functional:
            if 'Name' not in item or item['Name']=='':
                self.error.append("ERROR: No name for block with ID: " + item['id'] + " in page " + item['PageName'] + " in file "\
                    + item['FileName'] )
                self.actual_error_count+=1
                faultf.append(self.corrected_functional[self.corrected_functional.index(item)])
        tempf = [item for item in self.corrected_functional if item not in faultf]
        self.corrected_functional = tempf

        for item in self.corrected_physical:
            if ('Name' not in item) or (item['Name']==''):
                self.error.append("ERROR    : No name for block with ID: " + item['id'] + " in page " + item['PageName'] + " in file "\
                    + item['FileName'] )
                self.actual_error_count+=1
                faultp.append(self.corrected_physical[self.corrected_physical.index(item)])
        tempp = [item for item in self.corrected_physical if item not in faultp]
        self.corrected_physical = tempp

    def createphysicalnameset(self):
        namelist = ['CHASSIS']
        for item in self.corrected_physical:
            if item['BlockType'] in satconfig.physical_blocks:
                namelist.append(item['Name'])
        self.physical_nameset = set(namelist)

    
    def checkparentvalidity(self):
        for item in self.corrected_physical:

            if item['BlockType'] in satconfig.physical_blocks:

                if item['Parent'] == '':
                    item['Parent'] = 'CHASSIS'

                if (item['Parent'] not in self.physical_nameset) and (item['Parent'] not in self.enclosure_list):
                    self.error.append("ERROR: Invalid parent in block " + item['Name'] + " in page " + item['PageName'] + " in file "\
                    + item['FileName'] )
                    self.actual_error_count+=1
                else:
                    for parentitem in self.corrected_physical:
                        if parentitem['Name'] == item['Parent']:
                            if parentitem['BlockType'] not in satconfig.physical_blocks:
                                self.error.append("ERROR: Invalid parent type ("+ parentitem['Name']+', '+parentitem['BlockType'] +") in block " + item['Name'] + " in page " + item['PageName'] + " in file "\
                        + item['FileName'] )
                                self.actual_error_count+=1
                                break
                            elif (item['BlockType'] == "OTSC" or item['BlockType'] =="SENS" or item['BlockType'] =="ACT" or item['BlockType'] =="HMI"):
                                if ((parentitem['BlockType'] != 'CHASSIS') or (parentitem['BlockType'] not in self.enclosure_list)):
                                    self.error.append("ERROR: Invalid parent type ("+ parentitem['Name']+', '+parentitem['BlockType'] +") in block " + item['Name'] + " in page " + item['PageName'] + " in file "\
                        + item['FileName'] )
                                    self.actual_error_count+=1
                                    break
                            elif (item['BlockType'] == 'NCU' or item['BlockType'] == 'PCU') and ((item['Parent'] == 'CHASSIS') or (parentitem['Name'] not in self.enclosure_list)):
                                self.error.append("ERROR: Invalid parent type ("+ parentitem['Name']+', '+parentitem['BlockType'] +") in block " + item['Name'] + " in page " + item['PageName'] + " in file "\
                        + item['FileName'] )
                                self.actual_error_count+=1
                                break

    
                                
    def checkfunctionvalidity(self):
        for item in self.corrected_functional:
            if item['Function'] == '':
                self.error.append("ERROR: Function name missing in block " + item['Name'] + " in page " + item['PageName'] + \
                    " in file " + item["FileName"] )
                self.actual_error_count+=1


    def createnclosurelist(self):
        enclosurelist = []
        for item in self.corrected_physical:
            if item['BlockType'] in satconfig.physical_blocks:
                if item['Parent'] not in self.physical_nameset:
                    enclosurelist.append(item['Parent'])
        self.enclosure_list = set(enclosurelist)

    def createfunctionlist(self):
        functionlist = []
        for item in self.corrected_functional:
            if item['BlockType'] in satconfig.functional_blocks:
                functionlist.append(item['Function'])
        self.function_list = set(functionlist)

    def checkallocationvalidity(self):
        for item in self.corrected_functional:
            if item['BlockType'] in satconfig.functional_blocks:
                if item['Allocation'] == '':
                    self.error.append("ERROR: Allocation missing in block " + item['Name'] + " in page " + item['PageName']\
                        + " in file " + item['FileName'])
                    self.actual_error_count+=1
                elif (item['Allocation'] not in self.physical_nameset): 
                    self.error.append("ERROR: Invalid allocation in block " + item['Name'] + " in page " + item['PageName']\
                        + " in file " + item['FileName'])
                    self.actual_error_count+=1


    def updateconnectornames(self):
        for item in self.corrected_physical:
            if item['BlockType'] == "FCON" or item["BlockType"] == "MCON":
                item["Name"] = item["Parent"] + "/" + item["Name"]
    

    def checkfloatingsignals(self):
        for item in self.corrected_functional:
            if item["BlockType"] in satconfig.functional_signals:
                if ('source' not in item) or ('target' not in item):
                    self.error.append("ERROR: Floating Signal: " + item["Name"] + " in Page " + item["PageName"] + " in File " + \
                       item["FileName"]  )
                    self.actual_error_count+=1
                elif (item['source'] == '') or (item['target'] == ''):
                    self.error.append("ERROR: Floating Signal: " + item["Name"] + " in Page " + item["PageName"] + " in File " + \
                       item["FileName"]  )
                    self.actual_error_count+=1

        for item in self.corrected_physical:
            if item["BlockType"] in satconfig.physical_signals:
                if ('source' not in item) or ('target' not in item):
                    self.error.append("ERROR: Floating Signal: " + item["Name"] + " in Page " + item["PageName"] + " in File " + \
                       item["FileName"]  )
                    self.actual_error_count+=1   
                elif (item['source'] == '') or (item['target'] == ''):
                    self.error.append("ERROR: Floating Signal: " + item["Name"] + " in Page " + item["PageName"] + " in File " + \
                       item["FileName"]  )
                    self.actual_error_count+=1

    
    def createidlookup(self):
        idphysical = {k['id']:k for k in self.corrected_physical }
        idfunctional = {k['id']:k for k in self.corrected_functional}
        idphysical.update(idfunctional)
        self.iddata = idphysical

    def createnamelookup(self):
        idphysical = {k['Name']:k for k in self.corrected_physical }
        idfunctional = {k['Name']:k for k in self.corrected_functional}
        idphysical.update(idfunctional)
        self.namedata = idphysical

    def createpowerset(self):
        powerlist = []
        gndlist = []
        for item in self.corrected_physical:
            if "Supply" in item:
                powerlist.append(item['Supply'])
            if "GND" in item:
                gndlist.append(item['GND'])

        self.power_set = set(powerlist)
        self.gnd_set = set(gndlist)


    def createglobalidlookup(self):
        counter = 1
        prefix = "F"
        for item in self.corrected_functional:
            item['global_id'] = prefix + str(counter)
            counter += 1
        counter = 1
        prefix = "P"
        for item in self.corrected_physical:
            item['global_id'] = prefix + str(counter)
            counter += 1

        idphysical = {k['global_id']:k for k in self.corrected_physical }
        idfunctional = {k['global_id']:k for k in self.corrected_functional}
        idphysical.update(idfunctional)
        self.globaliddata = idphysical

    
    def createdatafile(self):
        data = dict()
        data["iddata"] = self.iddata
        data["globaliddata"] = self.globaliddata
        data["namedata"] = self.namedata
        data["enclosure"] = self.enclosure_list
        data["power"] = self.power_set

        if os.path.exists(satconfig.dbyamlfilename):
            os.remove(satconfig.dbyamlfilename)
        with open(satconfig.dbyamlfilename, 'w') as file:
            documents = yaml.dump(data, file)
        



    def replacesourcetargetid(self):
        for item in self.corrected_functional:
            if item['BlockType'] in satconfig.functional_signals:
                item['SourceName'] = self.iddata[item['source']]['Name']
                item['TargetName'] = self.iddata[item['target']]['Name']
        for item in self.corrected_physical:
            if item['BlockType'] in satconfig.physical_signals:
                item['SourceName'] = self.iddata[item['source']]['Name']
                item['TargetName'] = self.iddata[item['target']]['Name']


    def mergefunctionaldata(self):
        length = len(self.corrected_functional)
        i = 0
        while i < length:
            j = i + 1
            while j < length:
                if self.corrected_functional[i]['Name'] == self.corrected_functional[j]['Name']:
                    if self.corrected_functional[i]['BlockType'] == self.corrected_functional[j]['BlockType']:
                        for field in self.corrected_functional[i]:
                            if self.corrected_functional[i][field] == '' and self.corrected_functional[j][field] != '':
                                self.corrected_functional[i][field] = self.corrected_functional[j][field]
                            if field in satconfig.mergefields_concat:
                                self.corrected_functional[i][field] = self.corrected_functional[i][field] + ", " +\
                                    self.corrected_functional[j][field]
                            if self.corrected_functional[i][field] != '' and self.corrected_functional[j][field] != '':
                                if self.corrected_functional[i][field] != self.corrected_functional[j][field]:
                                    if field not in satconfig.mergefields_ignore_functional:
                                        print(self.corrected_functional[i], self.corrected_functional[j])
                                        self.error.append("ERROR: Merge conflict detected in field: " + field + " between (" + self.corrected_functional[i]["Name"]\
                                                    + ", Page: " + self.corrected_functional[i]['PageName'] + ", File: " + self.corrected_functional[i]['FileName'] + \
                                                        ") and (" + self.corrected_functional[j]["Name"]\
                                                    + ", Page: " + self.corrected_functional[j]['PageName'] + ", File: " + self.corrected_functional[j]['FileName'] + ")")
                                        self.actual_error_count+=1

                        del self.corrected_functional[j]
                        length -= 1
                else:
                    j += 1
            i += 1

    def mergephysicaldata(self):
        length = len(self.corrected_physical)
        i = 0
        while i < length:
            j = i + 1
            while j < length:
                if self.corrected_physical[i]['Name'] == self.corrected_physical[j]['Name']:
                    if self.corrected_physical[i]['BlockType'] == self.corrected_physical[j]['BlockType']:
                        if self.corrected_physical[i]['BlockType'] in satconfig.physical_blocks:
                            if self.corrected_physical[i]['Parent'] == self.corrected_physical[j]['Parent']:
                                for field in self.corrected_physical[i]:
                                    if self.corrected_physical[i][field] == '' and self.corrected_physical[j][field] != '':
                                        self.corrected_physical[i][field] = self.corrected_physical[j][field]
                                    if field in satconfig.mergefields_concat:
                                        self.corrected_physical[i][field] = self.corrected_physical[i][field] + ", " +\
                                            self.corrected_physical[j][field]
                                    if self.corrected_physical[i][field] != '' and self.corrected_physical[j][field] != '':
                                        if self.corrected_physical[i][field] != self.corrected_physical[j][field]:
                                            if field not in satconfig.mergefields_ignore_physical:
                                                self.error.append("ERROR: Merge conflict detected in field: " + field + " between (" + self.corrected_physical[i]["Name"]\
                                                            + ", Page: " + self.corrected_physical[i]['PageName'] + ", File: " + self.corrected_physical[i]['FileName'] + \
                                                                ") and (" + self.corrected_physical[j]["Name"]\
                                                            + ", Page: " + self.corrected_physical[j]['PageName'] + ", File: " + self.corrected_physical[j]['FileName'] + ")")
                                                self.actual_error_count+=1
                        else:
                            for field in self.corrected_physical[i]:
                                if self.corrected_physical[i][field] == '' and self.corrected_physical[j][field] != '':
                                    self.corrected_physical[i][field] = self.corrected_physical[j][field]
                                if field in satconfig.mergefields_concat:
                                    self.corrected_physical[i][field] = self.corrected_physical[i][field] + ", " +\
                                        self.corrected_physical[j][field]
                                if self.corrected_physical[i][field] != '' and self.corrected_physical[j][field] != '':
                                    if self.corrected_physical[i][field] != self.corrected_physical[j][field]:
                                        if field not in satconfig.mergefields_ignore_physical:
                                            self.error.append("ERROR: Merge conflict detected in field: " + field + " between (" + self.corrected_physical[i]["Name"]\
                                                        + ", Page: " + self.corrected_physical[i]['PageName'] + ", File: " + self.corrected_physical[i]['FileName'] + \
                                                            ") and (" + self.corrected_physical[j]["Name"]\
                                                        + ", Page: " + self.corrected_physical[j]['PageName'] + ", File: " + self.corrected_physical[j]['FileName'] + ")")
                                            self.actual_error_count+=1                           
                        del self.corrected_physical[j]
                        length -= 1
                else:
                    j += 1
            i += 1

    