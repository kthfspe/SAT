import json
import base64
import os
import xml.etree.ElementTree as ET
from scripts import blocklist
raw_physical = []
raw_functional = []
errormessage = []
warningmessage = []
root = ET.parse('LV_functional_architecture').getroot()
for child in root.findall('diagram/mxGraphModel/root/object'):
    a = dict(child.attrib)
    raw_functional.append(a)

root = ET.parse('LV_physical_architecture').getroot()
for child in root.findall('diagram/mxGraphModel/root/object'):
    a = dict(child.attrib)
    raw_physical.append(a)

with open("raw_pdb.json", 'w') as fout:
    json.dump(raw_physical, fout)  

with open("raw_fdb.json", 'w') as fout2:
    json.dump(raw_functional, fout2)


with open('raw_pdb.json', 'r') as fp:
    raw_pdb = json.load(fp)


# Physical Architecture - Block Validity Checking
for item in raw_pdb:
    if item != None:
        if item["BlockType"] not in blocklist.physical_blocktypes:
            errormessage.append("Invalid Block in physical architecture with BlockType " + item["BlockType"] + " and ID " + item["id"]  )


with open('raw_fdb.json', 'r') as fp:
    raw_fdb = json.load(fp)

# Functional Architecture - Block Validity Checking
for item in raw_fdb:
    if item != None:
        if item["BlockType"] not in blocklist.functional_blocktypes:
            errormessage.append("Invalid Block in functional architecture with BlockType " + item["BlockType"] + " and ID " + item["id"]  )


# Set rules for checking each field of each block



# Create global id lookup functional + physical



# Physical Architecture - Creating Merged Database

def mergedb(raw_db):
    merged_db = []
    for rawitem in raw_db:
        rawitem.pop("id")
    for rawitem in raw_db:
        count = 0
        for mergeditem in merged_db:
            if rawitem["Name"].lower() == mergeditem["Name"].lower():
                if rawitem["BlockType"].lower() == mergeditem["BlockType"].lower():
                    count = count + 1
                    if rawitem != mergeditem:
                        print("Not Same block")
                        for field in rawitem:
                            if rawitem[field] != "" and mergeditem[field] == "":
                                mergeditem[field] = rawitem[field]
                            if rawitem[field] != "" and mergeditem[field] != "":
                                print("Conflicting field during merge")                  
                        # If not, compare each field by field
                            # If one is empty, the other one is overwritten
                            # If both are filled, then an error message is added
                    # Add warning message saying what were merged together, the fields
                else:
                    pass
                    # Add warning message for same name used for different block types
        if count>0:
            # Add warning message to see total number of merges per block
            print(str(count) + " Merges occured")
        if count == 0:
            # New item added to merged db
            merged_db.append(rawitem)
            print("new item added to merged")
    return merged_db
    #return errormesg, warningmesg, mergedb


merged_pdb = mergedb(raw_pdb)
merged_fdb = mergedb(raw_fdb)

print(len(raw_pdb))
print(len(merged_pdb))
print(len(raw_fdb))
print(len(merged_fdb))
#print(errormessage)

    def mergedata(self, data):
        # empty ignore list
        ignorelist = []
        for item in data:
            if data.index(item) not in ignorelist:
                mergedinstances = 0
                for i in range(data.index(item)+1, len(data)):
                    if data[i] not in ignorelist:
                        citem = data[i]
                        if item['Name'] == citem['Name'] and item['BlockType'] == citem['BlockType']:
                            ignorelist.append(i)
                            if item != citem:
                                for field in item:
                                    if field not in blocklist.mergefields_ignore:
                                        if item[field] != citem[field]:
                                            if item[field] == "":
                                                item[field] = citem[field]
                                            elif citem[field] == "":
                                                pass
                                            else:
                                                self.error.append("ERROR: Merge conflict detected between (" + item["Name"]\
                                                    + ", Page: " + item['PageName'] + ", File: " + item['Filename'] + \
                                                        ") and (" + citem["Name"]\
                                                    + ", Page: " + citem['PageName'] + ", File: " + citem['Filename'] + ")")
                                                self.status+=1
                                mergedinstances+=1
 
    def sublist(self, match, data):
        sub = []
        for item in data:
            res = all(item.get(key, None) == val for key, val in match.items()) 
            if res:
                sub.append(item)
        return sub

    def mergeblock2(self, data):
        baseitem = data[0]
        data.pop(0)
        for field in data[0].keys():
            if field not in blocklist.mergefields_ignore:
                for item in data:
                    if baseitem[field] == '' and item[field] != '':
                        baseitem[field] = item[field]
                    if baseitem[field] != item[field]:
                        self.error.append("MERGE CONFLICT: Block with Name " + item["Name"] + " in page/file: " + \
                                    item["PageName"] + "/" + item["FileName"] + " and " + baseitem["PageName"] + \
                                        "/" + baseitem["FileName"] + " are conflicting over the field " + field)
                        self.actual_error_count += 1
            if field in blocklist.mergefields_concat:
                baseitem[field] = baseitem[field] + ', ' + item[field]
        return baseitem
                
    def mergef(self):
        merged_f = []
        for item in self.corrected_functional:
            sub = self.sublist({'Name': item['Name'], 'BlockType': item['BlockType']}, self.corrected_functional)
            if len(sub)>1:
                merged = self.mergeblock2(sub)
                merged_f.append(merged)
        cleaned = [dict(t) for t in {tuple(d.items()) for d in merged_f}]
        print(len(merged_f))
        # print(merged_f)
        for item in merged_f:
            print(item['Name'], item['BlockType'])
        print("Hello")
        for item in cleaned:
            print(item['Name'], item['BlockType'])


    def mergephysicaldata(self):
        ignorelist = []
        globalidcounter = 1
        for item in self.corrected_physical:
            if item['BlockType'] not in blocklist.physical_blocks:
                ignorelist.append(item['id'])
                item["global_id"] = "P" + str(globalidcounter)
                globalidcounter += 1
                self.merged_physical.append(item)
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
                merged_block = self.mergeblock(sublist)
                merged_block['global_id'] = "P" + str(globalidcounter)
                globalidcounter += 1
                self.merged_physical.append(merged_block)
            else:
                item['global_id'] = "P" + str(globalidcounter)
                globalidcounter += 1
                self.merged_physical.append(item)


    def mergefunctionaldata(self):
        globalidcounter = 1
        ignorelist = []
        for item in self.corrected_functional:
            #print(item['Name'])
            if item['BlockType'] not in blocklist.functional_blocks:
                ignorelist.append(item['id'])
                item['global_id'] = "F" + str(globalidcounter)
                globalidcounter += 1
                self.merged_functional.append(item)
        for item in self.corrected_functional:
            sublist = []
            if item['id'] not in ignorelist:
                ignorelist.append(item['id'])
                sublist.append(item)
                for i in range(self.corrected_functional.index(item)+1, len(self.corrected_functional)):
                    citem = self.corrected_functional[i]
                    if citem['id'] not in ignorelist:
                        subitem = {k:item[k]  for k in ('Name','BlockType','Function')}
                        subcitem = {k:citem[k] for k in ('Name','BlockType','Function')} 
                        if subitem == subcitem:
                            ignorelist.append(citem['id'])
                            sublist.append(citem)
                if len(sublist)>1:
                    merged_block = self.mergeblock(sublist)
                    merged_block['global_id'] = "F" + str(globalidcounter)
                    globalidcounter+=1
                    #print(merged_block)
                    self.merged_functional.append(merged_block)
            else:
                item['global_id'] = "F" + str(globalidcounter)
                globalidcounter += 1
                self.merged_functional.append(item)

    def mergeblock(self, instances):
        merged_block = {}
        #print(instances)
        for item in instances:
            if len(merged_block) == 0:
                merged_block = item
            else:
                for field in item:
                    if field not in blocklist.mergefields_ignore:
                        if item[field] != '' and merged_block[field] == '':
                            merged_block[field] = item[field]
                        elif item[field] != merged_block[field]:
                            self.error.append("MERGE CONFLICT: Block with Name " + item["Name"] + " in page/file: " + \
                                item["PageName"] + "/" + item["FileName"] + " and " + merged_block["PageName"] + \
                                    "/" + merged_block["FileName"] + " are conflicting over the field " + field)
                            self.actual_error_count += 1
                    if field in blocklist.mergefields_concat:
                        if item[field] != '' and merged_block[field] == '':
                            merged_block[field] = item[field]
                        elif item[field] != merged_block[field]:
                            merged_block[field] = merged_block[field] + ", " + item[field]
        #print(merged_block)
        return merged_block
 