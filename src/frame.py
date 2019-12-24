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


# Set rules for checking each field of ecah block


# Create glovbal id lookup functional + physical



# Physical Architecture - Creating Merged Database
merged_pdb = []

for rawitem in raw_pdb:
    rawitem.pop("id")
for rawitem in raw_pdb:
    count = 0
    for mergeditem in merged_pdb:
        if rawitem["Name"].lower() == mergeditem["Name"].lower():
            if rawitem["BlockType"].lower() == mergeditem["BlockType"].lower():
                count = count + 1
                if rawitem == mergeditem:
                    print("Same block")
                # Add merge logic here
                    # If everything except the id's are the same then skip
               
                    # If not, compare each field by field
                        # If one is empty, the other one is overwritten
                        # If both are filled, then an error message is added

                # Add warning message saying what were merged together, the fields
                print("merge")
            else:
                pass
                # Add warning message for same name used for different block types
    if count>0:
        # Add warning message to see total number of merges per block
        print(str(count) + " Merges occured")
    if count == 0:
        # New item added to merged db
        merged_pdb.append(rawitem)
        print("new item added to merged")






print(len(raw_pdb))
print(len(merged_pdb))
print(errormessage)

