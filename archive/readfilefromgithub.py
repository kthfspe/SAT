from github import Github
import base64
import os
import xml.etree.ElementTree as ET

# or using an access token
g = Github(os.environ['GITPAT'])
repo = g.get_repo("kthfspe/SA")
contents = repo.get_contents("examples/LV_architecture/LV_physical_architecture")
s = base64.b64decode(contents.content)
root = ET.fromstring(s)

LVphysical = []
for child in root.findall('diagram/mxGraphModel/root/object'):
    LVphysical.append(child.attrib)

print(len(LVphysical))

for child in LVphysical:
    if child['BlockType'] == "ANA":
        print(child)

#tree = ET.ElementTree(root)
#s = ET.tostring(root,encoding='utf-8')
#s = s.decode('utf-8')

#Working Commit line
#repo.update_file("examples/LV_architecture/LV_physical_architecture","Testing commit", s, contents.sha, )
