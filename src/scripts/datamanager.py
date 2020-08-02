import os
import yaml

class DataManager:
    raw_physical = []
    raw_functional = []
    corrected_functional = []
    corrected_physical = []
    physical_nameset = set()
    enclosure_list = set()
    connector_list = []
    cable_list = []
    # connector_types = set()
    function_list = set()
    power_set = set()
    gnd_set = set()
    global_field_set = set()
    error = []
    log = []
    actual_error_count = 0
    iddata = dict()
    rawiddata = dict()
    globaliddata = dict()
    namedata = dict()

    def __init__(self):
        pass

    def buildmodel(self, rf, rp, config):
        self.config = config
        self.error = []
        self.actual_error_count = 0
        self.corrected_functional = []                                          # To store only the valid blocks
        self.corrected_physical = []
        self.raw_physical = rp
        self.raw_functional = rf                                                # Create a dict lookup with raw data to save to db later

        # Read in lookup table for connectors
        with open(self.config['connectorlookuptablefilename'], 'r') as conn_file:
            self.connector_lookup_table = yaml.load(conn_file)
            conn_file.close()

        # Remove ignored blocks from the global block list
        self.error.append("Building Model...")
        self.error.append("Removing blocks from ignorelist...")
        self.removeignoredblocks()
        self.createrawlookup()



        # Status checker function
        if self.actual_error_count>0:
            return self.error, self.actual_error_count

        # Checks for blocktypes outside of global satconfig
        self.error.append("Checking validity of BlockType field...")
        self.checkblockvalidity()

        # Status checker function
        if self.actual_error_count>0:
            return self.error, self.actual_error_count

        # Check name validity: This is done separately from other fields as further checks are not possible
        # if 'Name' is missing
        self.error.append("Checking validity of Name field...")
        self.checknamevalidity()

        # Status checker function
        if self.actual_error_count>0:
            return self.error, self.actual_error_count

        # Checks for floating signals
        self.error.append("Checking for floating signals...")
        self.checkfloatingsignals()

        # Status checker function
        if self.actual_error_count>0:
            return self.error, self.actual_error_count

        # Create nameset
        # Creates a set of all names of all blocks in physical architecture
        self.createphysicalnameset()

        # Create enclosure list
        # Assumes all new parent values not in namelist as an enclosure
        self.createnclosurelist()

        # print(self.enclosure_list)
        # Assigns empty parents to CHASSIS
        # Checks if parent name is valid
        # Checks if parent type is valid
        self.error.append("Checking validity of Parent field...")
        self.checkparentvalidity()

        # Status checker function
        if self.actual_error_count>0:
            return self.error, self.actual_error_count

        # Check if function name is not empty
        self.error.append("Checking validity of Function field...")
        self.checkfunctionvalidity()

        # Status checker function
        if self.actual_error_count>0:
            return self.error, self.actual_error_count

        # Create function list
        self.createfunctionlist()

        # Check if allocation in funcitnla block is a valid name in physical block
        self.error.append("Checking validity of Allocation field...")
        self.checkallocationvalidity()

        # Status checker function
        if self.actual_error_count>0:
            return self.error, self.actual_error_count

        # Update connector names to include the name of the parent
        self.updateconnectornames()

        # Check connector validity
        self.error.append('Checking connectors...')
        self.checkconnectorvalidity()

        # Create a Lookup where the id is the key
        self.createidlookup()

        # Replaces id in sources and targets of all signals to names of the block
        self.replacesourcetargetid()

        # Merging redundant data instances
        self.error.append("Merging data instances..")
        self.mergefunctionaldata()
        self.mergephysicaldata()

        # Add parent and child data
        self.addparentchild()

        # Create a Lookup where the id is the key
        self.createnamelookup()

        # Generate cables
        self.error.append('Generating harness...')
        self.generatecables()

        # Adds a global id to all elements and creates a lookup with globalid as key
        self.createglobalidlookup()

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
            if item['BlockType'] not in self.config["ignore_blocktype"]:
                if 'SATexception' in item:
                    if item['SATexception'] != 'ignore':
                        tempf.append(item)
                else:
                    tempf.append(item)
        self.raw_functional = tempf
        for item in self.raw_physical:
            if item['BlockType'] not in self.config["ignore_blocktype"]:
                if 'SATexception' in item:
                    if item['SATexception'] != 'ignore':
                        tempp.append(item)
                else:
                    tempp.append(item)
        self.raw_physical = tempp

    def checkblockvalidity(self):
        # This function can be refactored to use del operator to remove elements and use the same data structure
        # Physical Architecture - Block Validity Checking
        for item in self.raw_physical:
            if item["BlockType"] not in self.config["physical_blocks"]+self.config["physical_signals"]:
                self.error.append("ERROR: Invalid Block in file " + item["FileName"] + " with BlockType " + item["BlockType"] + \
                   ", Name " + item['Name'] + " and ID " + item["id"]  )
                self.actual_error_count+=1
            else:
                self.corrected_physical.append(item)

        # Functional Architecture - Block Validity Checking
        for item in self.raw_functional:
            if item["BlockType"] not in self.config["functional_blocks"]+self.config["functional_signals"]:
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
            elif " " in item["Name"]:
                self.error.append("ERROR: Name (" + item["Name"] + ") not following correct naming convention for block with ID: " \
                    + item["id"] + " in page " + item["PageName"] + " in file " + item["FileName"])
                self.actual_error_count+=1
                faultf.append(self.corrected_functional[self.corrected_functional.index(item)])
            elif "\n" in item["Name"]:
                item["Name"] = item["Name"].replace("\n","")
        tempf = [item for item in self.corrected_functional if item not in faultf]
        self.corrected_functional = tempf

        for item in self.corrected_physical:
            if ('Name' not in item) or (item['Name']==''):
                self.error.append("ERROR    : No name for block with ID: " + item['id'] + " in page " + item['PageName'] + " in file "\
                    + item['FileName'] )
                self.actual_error_count+=1
                faultp.append(self.corrected_physical[self.corrected_physical.index(item)])
            elif " " in item["Name"]:
                self.error.append("ERROR: Name (" + item["Name"] + ") not following correct naming convention for block with ID: " \
                    + item["id"] + " in page " + item["PageName"] + " in file " + item["FileName"])
                self.actual_error_count+=1
                faultp.append(self.corrected_physical[self.corrected_physical.index(item)])
            elif "\n" in item["Name"]:
                item["Name"] = item["Name"].replace("\n","")
        tempp = [item for item in self.corrected_physical if item not in faultp]
        self.corrected_physical = tempp

    def createphysicalnameset(self):
        namelist = ['CHASSIS']
        for item in self.corrected_physical:
            if item["BlockType"] in self.config["physical_blocks"]:
                namelist.append(item['Name'])
        self.physical_nameset = set(namelist)

    def checkparentvalidity(self):
        for item in self.corrected_physical:

            if item['BlockType'] in self.config["physical_blocks"]:

                if item['Parent'] == '':
                    item['Parent'] = 'CHASSIS'

                if (item['Parent'] not in self.physical_nameset) and (item['Parent'] not in self.enclosure_nameset):
                    self.error.append("ERROR: Invalid parent in block " + item['Name'] + " in page " + item['PageName'] + " in file "\
                    + item['FileName'] )
                    self.actual_error_count+=1
                else:
                    for parentitem in self.corrected_physical:
                        if parentitem['Name'] == item['Parent']:
                            if parentitem['BlockType'] not in self.config["physical_blocks"]:
                                self.error.append("ERROR: Invalid parent type1 ("+ parentitem['Name']+', '+parentitem['BlockType'] +") in block " + item['Name'] + " in page " + item['PageName'] + " in file "\
                        + item['FileName'] )
                                self.actual_error_count+=1
                                break
                            elif (item['BlockType'] == "OTSC" or item['BlockType'] =="SENS" or item['BlockType'] =="ACT" or item['BlockType'] =="HMI"):
                                if ((item['Parent'] != 'CHASSIS') and (parentitem['Name'] not in self.enclosure_nameset)):
                                    self.error.append("ERROR: Invalid parent type2 ("+ parentitem['Name']+', '+parentitem['BlockType'] +") in block " + item['Name'] + " in page " + item['PageName'] + " in file "\
                        + item['FileName'] )
                                    self.actual_error_count+=1
                                    break
                            elif (item['BlockType'] == 'NCU' or item['BlockType'] == 'PCU') and ((item['Parent'] == 'CHASSIS') or (parentitem['Name'] not in self.enclosure_nameset)):
                                self.error.append("ERROR: Invalid parent type3 ("+ parentitem['Name']+', '+parentitem['BlockType'] +") in block " + item['Name'] + " in page " + item['PageName'] + " in file "\
                        + item['FileName'] )
                                self.actual_error_count+=1
                                break

    def checkfunctionvalidity(self):
        for item in self.corrected_functional:
            if item['Function'] == '':
                self.error.append("ERROR: Function name missing in block " + item['Name'] + " in page " + item['PageName'] + \
                    " in file " + item["FileName"] )
                self.actual_error_count+=1

    def checkconnectorvalidity(self):

        # print(self.connector_lookup_table)
        set_of_names = set()
        for item in self.connector_list:
            # Check if connector exist in multiple instances
            if item['Name'] in set_of_names:
                print('Connector {} exists in multiple instances. Check parent name'.format(item['Name']))
                self.error.append('Connector {} exists in multiple instances. Check parent name'.format(item['Name']))
                self.actual_error_count += 1
                continue
            set_of_names.add(item['Name'])
            # Validate connector
            self.validateconnector(item)

    def validateconnector(self, conn):

        # Check if connector type exist in list of connectors
        key = ''


        if conn['BlockType'] == 'LEMO':
            # conn.pop('LocalName')
            for field in self.config['LEMOConnectors_matchfields']:
                key += conn[field]
            if key in self.connector_lookup_table:
                if conn['Pins'] not in self.connector_lookup_table[key]['Pins']:
                    print('Invalid pin count: {} for connector {}'.format(conn['Pins'], conn['Name']))
                conn.update(self.connector_lookup_table[key])
            else:
                print('Invalid connector type {} for {}'.format(key, conn['Name']))
                self.error.append('Invalid connector type {} for {}'.format(key, conn['Name']))
        else:
            for field in self.config['BoardConnectors_matchfields']:
                key += conn[field]
            if key in self.connector_lookup_table:
                Pins = conn['Pins']
                if Pins not in self.connector_lookup_table[key]['Pins']:
                    print('Invalid pin count: {} for connector {}'.format(conn['Pins'], conn['Name']))
                    self.error.append('Invalid pin count: {} for connector {}'.format(conn['Pins'], conn['Name']))
                    # Pins = '?'
                conn.update(self.connector_lookup_table[key])
                conn['Pins'] = Pins
            else:
                print('Invalid connector type {} for {}'.format(key, conn['Name']))
                self.error.append('Invalid connector type {} for {}'.format(key, conn['Name']))

    def generatecables(self):


        '''
        1. Ignore connectors with SATexception = neglect_in_harness
        2. Create lookup dict (using signal tuples as key)
        3. Find matching connector pairs, don't need cable so discard
        4. Find matching connector twins
        5. Generate partner connectors and validate them
        6. Genetare end-to-end cables
        7. Generate nested cables
        8. Split nested cables by parent (if they are board connectors)


        '''

        generated_connectors = []
        Cable_num = 0
        gender_opposite = {'M':'F', 'F':'M'}
        connector_lookup_by_physical_signals = dict()
        connector_lookup_by_individual_signal = dict()
        for connector in self.connector_list:
            # 1
            if 'SATexception' in connector:
                if 'neglect_in_harness' in connector['SATexception']:
                    continue

            # 2a
            physical_signals = []
            for pin_number in range(1, int(connector['Pins'])+1):
                if pin_number < 10:
                    pin_name = 'Pin0' + str(pin_number)
                else:
                    pin_name = 'Pin' + str(pin_number)

                if pin_name in connector:
                    physical_signals.append(connector[pin_name])

            key_tuple = tuple(physical_signals)

            if key_tuple in connector_lookup_by_physical_signals:
                # 3
                if connector_lookup_by_physical_signals[key_tuple]['Connectors'][0]['Gender'] == gender_opposite[connector['Gender']]:
                    connector_lookup_by_physical_signals.pop(key_tuple)
                # 4
                else:
                    connector_lookup_by_physical_signals[key_tuple]['Connectors'].append(connector)
            # 2b
            else:
                connector_lookup_by_physical_signals[key_tuple] = {
                'Connectors': [connector],
                'PhysicalSignals': physical_signals}

        # 5
        for key in connector_lookup_by_physical_signals:
            new_conns = []
            for connector in connector_lookup_by_physical_signals[key]['Connectors']:
                new_connector = dict()
                new_connector.update(connector)
                new_connector['Name'] = connector['Parent'] +'/T'+ connector['LocalName'][1:]
                new_connector['Gender'] = gender_opposite[connector['Gender']]
                new_connector['LocalName'] = 'T'+ connector['LocalName'][1:]
                new_connector['Parent'] = connector['ParentBlock']['Parent']

                if new_connector['BlockType'] in 'FCON, MCON':
                     new_connector['BlockType'] = new_connector['Gender'] + 'CON'
                self.validateconnector(new_connector)
                generated_connectors.append(new_connector)
                new_conns.append(new_connector)
            connector_lookup_by_physical_signals[key]['Connectors'] = new_conns

        self.connector_list += generated_connectors

        keys_for_nested_cables = []
        # 6
        for key in connector_lookup_by_physical_signals:
            if len(connector_lookup_by_physical_signals[key]['Connectors']) == 2:
                Cable_num += 1
                Cable_ID = 'CAB' + str(Cable_num)
                Parent_set = set()
                for conn in connector_lookup_by_physical_signals[key]['Connectors']:
                    # print(conn['Name'])
                    Parent_set.add(conn['Parent'])

                if len(Parent_set) > 1:
                    Parent = 'CHASSIS'
                else:
                    Parent = Parent_set.pop()

                new_cable = {
                'Connectors' : connector_lookup_by_physical_signals[key]['Connectors'],
                'PhysicalSignals': connector_lookup_by_physical_signals[key]['PhysicalSignals'],
                'Name': Cable_ID,
                'Parent': Parent,
                'BlockType': 'CAB'
                }
                self.cable_list.append(new_cable)
                try:
                    self.namedata[new_cable['Parent']]['ChildBlocks'].append(new_cable)
                except KeyError:
                    pass
                self.corrected_physical.append(new_cable) # Add cables to physical data
            else:
                keys_for_nested_cables.append(key)


        for key in keys_for_nested_cables:
            temp_list = []
            for signal in key:
                if signal in connector_lookup_by_individual_signal:
                    connector_lookup_by_individual_signal[signal].add(key)
                else:
                    connector_lookup_by_individual_signal[signal] = {key}



        # 7
        checked_keys = []
        def find_nested_signals(input_signals):
            # global checked_keys
            found_signals = []
            for signal in input_signals:
                conn_with_signal_keys = connector_lookup_by_individual_signal[signal]
                for key in conn_with_signal_keys:
                    if key in keys_for_nested_cables and key not in checked_keys:
                        checked_keys.append(key)
                        found_signals += list(key)
            if len(found_signals) > 0:
                return input_signals + find_nested_signals(found_signals)
            else:
                return input_signals


        for key in connector_lookup_by_physical_signals:

            if key in keys_for_nested_cables:

                Cable_num += 1
                Cable_ID = 'CAB' + str(Cable_num)
                Parent_set = set()
                connectors_in_this_cable = []
                physical_signals_in_this_cable = set(find_nested_signals(list(key)))

                for ps in physical_signals_in_this_cable:
                    for key in connector_lookup_by_individual_signal[ps]:
                        if key in keys_for_nested_cables:
                            connectors_in_this_cable += connector_lookup_by_physical_signals[key]['Connectors']
                            keys_for_nested_cables.remove(key)
                for conn in connectors_in_this_cable:
                    Parent_set.add(conn['Parent'])


                new_cable = {
                'Connectors' : connectors_in_this_cable,
                'PhysicalSignals': physical_signals_in_this_cable,
                'Name': Cable_ID,
                'Parent': Parent,
                'BlockType': 'CAB'
                }

                try:
                    self.namedata[new_cable['Parent']]['ChildBlocks'].append(new_cable) # If parent is 'CHASSIS', then it has no field "ChildBlocks", thus causes KeyError
                except KeyError:
                    pass





                self.corrected_physical.append(new_cable) # Add cables to physical data
                self.cable_list.append(new_cable)

    def createnclosurelist(self):
        raw_enclosurelist = []
        for item in self.corrected_physical:
            if item['BlockType'] in self.config["physical_blocks"]:
                if item['Parent'] not in self.physical_nameset and (item["Parent"] != ""):
                    raw_enclosurelist.append(item['Parent'])
        self.enclosure_nameset = set(raw_enclosurelist)

        self.enclosure_list = []
        enc_num = 0
        for enclosure_name in self.enclosure_nameset:
            enc_num += 1
            newenclosure = {
                "BlockType": "ENC",
                "Parent": "CHASSIS",
                "Name": enclosure_name,
                "id": "ENC" + str(enc_num)
                }
            self.corrected_physical.append(newenclosure)
            self.enclosure_list.append(newenclosure)

    def createfunctionlist(self):
        functionlist = []
        for item in self.corrected_functional:
            if item['BlockType'] in self.config["functional_blocks"]:
                functionlist.append(item['Function'])
        self.function_list = set(functionlist)

    def checkallocationvalidity(self):
        for item in self.corrected_functional:
            if item['BlockType'] in self.config["functional_blocks"]:
                if "\n" in item["Allocation"]:
                    item["Allocation"] = item["Allocation"].replace("\n","")
                if item["Allocation"].lower() == "tbd":
                    item["Allocation"] = "CHASSIS"
                if item['Allocation'] == '':
                    self.error.append("ERROR: Allocation missing in block " + item['Name'] + " in page " + item['PageName']\
                        + " in file " + item['FileName'])
                    self.actual_error_count+=1
                elif (item['Allocation'] not in self.physical_nameset) and (item['Allocation'].lower() not in self.physical_nameset):
                    self.error.append("ERROR: Invalid allocation(" + item["Allocation"]+ ") in block " + item['Name'] + " in page " + item['PageName']\
                        + " in file " + item['FileName'])
                    self.actual_error_count+=1

    def updateconnectornames(self):
        for item in self.corrected_physical:
            if item['BlockType'] in "FCON, MCON, LEMO":
                item['LocalName'] = item['Name']
                item["Name"] = item["Parent"] + "/" + item["Name"]
                # self.connector_types.add(item['Type'])
                self.connector_list.append(item)
            if item['BlockType'] in 'FCON, MCON':
                item['Gender'] = item['BlockType'][0]

    def checkfloatingsignals(self):
        for item in self.corrected_functional:
            if item["BlockType"] in self.config["functional_signals"]:
                if ('source' not in item) or ('target' not in item):
                    self.error.append("ERROR: Floating Signal: " + item["Name"] + " in Page " + item["PageName"] + " in File " + \
                       item["FileName"]  )
                    self.actual_error_count+=1
                elif (item['source'] == '') or (item['target'] == ''):
                    self.error.append("ERROR: Floating Signal: " + item["Name"] + " in Page " + item["PageName"] + " in File " + \
                       item["FileName"]  )
                    self.actual_error_count+=1

        for item in self.corrected_physical:
            if item["BlockType"] in self.config["physical_signals"]:
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

    def createrawlookup(self):
        idphysical = {k['id']:k for k in self.raw_physical }
        idfunctional = {k['id']:k for k in self.raw_functional}
        idphysical.update(idfunctional)
        self.rawiddata = idphysical

    def createnamelookup(self):
        namephysical = {k['Name']:k for k in self.raw_physical }
        namefunctional = {k['Name']:k for k in self.raw_functional}
        namephysical.update(namefunctional)
        self.namedata = namephysical

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
        data["enclosure"] = self.enclosure_list
        data["power"] = self.power_set
        data['rawiddata'] = self.rawiddata
        data['connector'] = self.connector_list
        data['cable'] = self.cable_list

        with open(self.config["dbyamlfilename"], 'w') as file:
            documents = yaml.dump(data, file)
            file.close()

    def replacesourcetargetid(self):
        for item in self.corrected_functional:
            if item['BlockType'] in self.config["functional_signals"]:
                item['SourceName'] = self.iddata[item['source']]['Name']
                item['TargetName'] = self.iddata[item['target']]['Name']
        for item in self.corrected_physical:
            if item['BlockType'] in self.config["physical_signals"]:
                item['SourceName'] = self.iddata[item['source']]['Name']
                item['TargetName'] = self.iddata[item['target']]['Name']

    def mergefunctionaldata(self):
        set_of_names = dict()

        for item in self.corrected_functional:
            key = item['Name'] + item['BlockType']
            if key in set_of_names:
                for field in item:
                    if field not in self.config['mergefields_ignore_functional']:
                        if item[field] != '' and set_of_names[key][field] == '':
                            set_of_names[key][field] = item[field]

                        if field in self.config["mergefields_concat"] and set_of_names[key][field] != item[field]:
                            set_of_names[key][field] += ', ' + item[field]
            else:
                set_of_names[key] = item

        self.corrected_functional = list(set_of_names.values())
    # def mergefunctionaldata(self):
    #     length = len(self.corrected_functional)
    #     i = 0
    #     while i < length:
    #         j = i + 1
    #         while j < length:
    #             if self.corrected_functional[i]['Name'] == self.corrected_functional[j]['Name']:
    #                 if self.corrected_functional[i]['BlockType'] == self.corrected_functional[j]['BlockType']:
    #                     for field in self.corrected_functional[i]:
    #                         if self.corrected_functional[i][field] == '' and self.corrected_functional[j][field] != '':
    #                             self.corrected_functional[i][field] = self.corrected_functional[j][field]
    #
    #                         if field in self.config["mergefields_concat"]:
    #                             self.corrected_functional[i][field] = self.corrected_functional[i][field] + ", " +\
    #                                 self.corrected_functional[j][field]
    #
    #                         if self.corrected_functional[i][field] != '' and self.corrected_functional[j][field] != '':
    #                             if self.corrected_functional[i][field] != self.corrected_functional[j][field]:
    #                                 if field not in self.config["mergefields_ignore_functional"]:
    #                                     self.error.append("ERROR: Merge conflict detected in field: " + field + " between (" + self.corrected_functional[i]["Name"]\
    #                                                 + ", Page: " + self.corrected_functional[i]['PageName'] + ", File: " + self.corrected_functional[i]['FileName'] + \
    #                                                     ") and (" + self.corrected_functional[j]["Name"]\
    #                                                 + ", Page: " + self.corrected_functional[j]['PageName'] + ", File: " + self.corrected_functional[j]['FileName'] + ")")
    #                                     self.actual_error_count+=1
    #
    #                     del self.corrected_functional[j]
    #                     length -= 1
    #             else:
    #                 j += 1
    #         i += 1


    def mergephysicaldata(self):
        set_of_names = dict()

        for item in self.corrected_physical:
            key = item['Name'] + item['BlockType']
            if item['BlockType'] in self.config["physical_blocks"]:
                key += item['Parent']
            if key in set_of_names:
                for field in item:
                    if field not in self.config['mergefields_ignore_physical']:
                        # print(key, field, item['Name'])
                        if item[field] != '' and set_of_names[key][field] == '':
                            set_of_names[key][field] = item[field]

                        if field in self.config["mergefields_concat"] and set_of_names[key][field] != item[field]:
                            set_of_names[key][field] += ', ' + item[field]


            else:
                set_of_names[key] = item

        self.corrected_physical = list(set_of_names.values())

    # def mergephysicaldata(self):
    #     length = len(self.corrected_physical)
    #     i = 0
    #     while i < length:
    #         j = i + 1
    #         while j < length:
    #             if self.corrected_physical[i]['Name'] == self.corrected_physical[j]['Name']:
    #                 if self.corrected_physical[i]['BlockType'] == self.corrected_physical[j]['BlockType']:
    #                     if self.corrected_physical[i]['BlockType'] in self.config["physical_blocks"]:
    #                         if self.corrected_physical[i]['Parent'] == self.corrected_physical[j]['Parent']:
    #                             for field in self.corrected_physical[i]:
    #                                 if self.corrected_physical[i][field] == '' and self.corrected_physical[j][field] != '':
    #                                     self.corrected_physical[i][field] = self.corrected_physical[j][field]
    #                                 if field in self.config["mergefields_concat"]:
    #                                     self.corrected_physical[i][field] = self.corrected_physical[i][field] + ", " +\
    #                                         self.corrected_physical[j][field]
    #                                 if self.corrected_physical[i][field] != '' and self.corrected_physical[j][field] != '':
    #                                     if self.corrected_physical[i][field] != self.corrected_physical[j][field]:
    #                                         if field not in self.config["mergefields_ignore_physical"]:
    #                                             self.error.append("ERROR: Merge conflict detected in field: " + field + " between (" + self.corrected_physical[i]["Name"]\
    #                                                         + ", Page: " + self.corrected_physical[i]['PageName'] + ", File: " + self.corrected_physical[i]['FileName'] + \
    #                                                             ") and (" + self.corrected_physical[j]["Name"]\
    #                                                         + ", Page: " + self.corrected_physical[j]['PageName'] + ", File: " + self.corrected_physical[j]['FileName'] + ")")
    #                                             self.actual_error_count+=1
    #                     else:
    #                         for field in self.corrected_physical[i]:
    #                             if self.corrected_physical[i][field] == '' and self.corrected_physical[j][field] != '':
    #                                 self.corrected_physical[i][field] = self.corrected_physical[j][field]
    #                             if field in self.config["mergefields_concat"]:
    #                                 self.corrected_physical[i][field] = self.corrected_physical[i][field] + ", " +\
    #                                     self.corrected_physical[j][field]
    #                             if self.corrected_physical[i][field] != '' and self.corrected_physical[j][field] != '':
    #                                 if self.corrected_physical[i][field] != self.corrected_physical[j][field]:
    #                                     if field not in self.config["mergefields_ignore_physical"]:
    #                                         self.error.append("ERROR: Merge conflict detected in field: " + field + " between (" + self.corrected_physical[i]["Name"]\
    #                                                     + ", Page: " + self.corrected_physical[i]['PageName'] + ", File: " + self.corrected_physical[i]['FileName'] + \
    #                                                         ") and (" + self.corrected_physical[j]["Name"]\
    #                                                     + ", Page: " + self.corrected_physical[j]['PageName'] + ", File: " + self.corrected_physical[j]['FileName'] + ")")
    #                                         self.actual_error_count+=1
    #                     del self.corrected_physical[j]
    #                     length -= 1
    #             else:
    #                 j += 1
    #         i += 1

    def addparentchild(self):
        for item in self.corrected_physical:
            if item["BlockType"] in self.config["physical_blocks"]:
                for parentitem in self.corrected_physical:
                    if parentitem["Name"].lower() == item["Parent"].lower():
                        item["ParentBlock"] = parentitem
                        break

        for item in self.corrected_physical:
            if item["BlockType"] in self.config["physical_blocks"]:
                item["ChildBlocks"] = []
                for childitem in self.corrected_physical:
                    if "Parent" in childitem:
                        if childitem["Parent"].lower() == item["Name"].lower():
                            item["ChildBlocks"].append(childitem)
                if item["ChildBlocks"] == []:
                    del item["ChildBlocks"]
