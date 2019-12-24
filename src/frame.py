import json
import base64
import os
import xml.etree.ElementTree as ET

raw_physical = []
raw_functional = []
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
    data = json.load(fp)

for item in data:
    if item != None:
        print(item["BlockType"])
        pass

with open('raw_fdb.json', 'r') as fp:
    data2 = json.load(fp)

for item in data2:
    if item != None:
        # print(item['BlockType'])
        pass
