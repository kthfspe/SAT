from github import Github
import base64

# or using an access token
g = Github("blablablablabla")

# for repo in g.get_user().get_repos():
    # print(repo.name)
    # repo.edit(has_wiki=False)
    # to see all the available attributes and methods
    #print(dir(repo))

#repo = g.get_repo("kthfspe/SA")
#contents = repo.get_contents("HV_architecture/HV_functional_architecture.drawio")
#s = base64.b64decode(contents.content)
# print()

import xml.etree.ElementTree as ET
#parser = ET.XMLParser(encoding="base64")


repo = g.get_repo("kthfspe/SAT")
contents = repo.get_contents("archive/testfiles/physical.xml")
#print(type(contents.content))
s = base64.b64decode(contents.content)
#print(s)
root = ET.fromstring(s)
for child in root.findall('diagram/mxGraphModel/root/object'):
    print(child.attrib["BlockType"])
    
#print(type(root))

tree = ET.ElementTree(root)
#tree.write("filename.xml")
#print("hellooooooooooooooooooooooooooooooooooooo")
#root = ET.parse('filename.xml').getroot()

s = ET.tostring(root,encoding='utf-8')
#print(s)
s = s.decode('utf-8')
print(type(s))
#s = base64.b64encode(s)



#Working Commit line
repo.update_file("archive/testfiles/physical.xml","Testing commit", s, contents.sha, )
