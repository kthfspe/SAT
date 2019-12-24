import json
import base64
import os
import xml.etree.ElementTree as ET
from scripts import blocklist
raw_physical = []
raw_functional = []
errormessage = []
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


# Physical Architecture - Removing exactly same instances
print(len(raw_pdb))
merged_pdb = []
for i in range(0,len(raw_pdb)):
    temp = raw_pdb[i+1:len(raw_pdb)]
    if (raw_pdb[i] not in temp) and (raw_pdb[i] not in merged_pdb):
        merged_pdb.append(raw_pdb[i])


print(len(raw_pdb))
print(len(merged_pdb))


print(errormessage)
