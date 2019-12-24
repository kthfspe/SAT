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
        for child in self.root.findall('diagram/mxGraphModel/root/object'):
            self.XMLContent.append(child.attrib)
        return self.XMLContent

