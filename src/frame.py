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




# Physical Architecture - Creating Merged Database
merged_pdb = []
        
for rawitem in raw_pdb:
    count = 0
    for mergeditem in merged_pdb:
        if rawitem["Name"].lower() == mergeditem["Name"].lower():
            if rawitem["BlockType"].lower() == mergeditem["BlockType"].lower():
                count = count + 1
                print("merge")
            else:
                print("same name for different block type warning")
    if count>0:
        print(str(count) + " Merges occured")
    if count == 0:
        merged_pdb.append(rawitem)
        print("new item added to merged")

print(len(raw_pdb))
print(len(merged_pdb))



print(errormessage)
