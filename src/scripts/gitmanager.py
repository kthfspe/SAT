from github import Github    
import xml.etree.ElementTree as ET
import base64  

class GitManager:
    gitobject = None
    repo = None
    gitpat = None
    XMLContent = [None]
    def __init__(self):
        pass
    
    def gitlogin(self, pat):
        self.gitpat = pat
        self.gitobject = Github(pat)
        try:
            self.repo = self.gitobject.get_repo("kthfspe/SA")
            return True
        except:
            print("Access Denied. Check your Personal Access Token and your access to repo kthfspe/SA")
            return False

    def readfile(self, path):
        self.XMLContent = [] #Empties the XMLContent container for reading a new file
        self.repo = self.gitobject.get_repo("kthfspe/SA")
        self.contents = self.repo.get_contents(path)
        self.stringcontent = base64.b64decode(self.contents.content)
        self.root = ET.fromstring(self.stringcontent)       
        for child in self.root.findall('diagram'):
            if 'name' in child.attrib:
                print(child.attrib['name'], child.attrib['id'])

        for child in self.root.findall('diagram/mxGraphModel/root/object'):
            if 'parent' in child[0].attrib:
                print(child[0].attrib['parent'])
            # print(child[0].attrib)
            self.XMLContent.append(child.attrib)
        return self.XMLContent

