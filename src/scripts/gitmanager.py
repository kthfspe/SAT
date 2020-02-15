from github import Github    
import xml.etree.ElementTree as ET
import base64  
import os

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

        filename = os.path.basename(path)
        self.XMLContent = [] #Empties the XMLContent container for reading a new file
        self.repo = self.gitobject.get_repo("kthfspe/SA")
        self.contents = self.repo.get_contents(path)
        self.stringcontent = base64.b64decode(self.contents.content)
        self.root = ET.fromstring(self.stringcontent)       
        for child in self.root.findall('diagram'):
            pagedata = child.attrib
            if 'name' in pagedata:
                pagedata['PageName'] = pagedata.pop('name')
                pagedata['PageId'] = pagedata.pop('id')
                pagedata['Filename'] = filename
                for item in child.iterfind('mxGraphModel/root/object'):
                    blockdata = item.attrib
                    blockmetadata = item[0].attrib
                    blockmetadata['MetaParent'] = blockmetadata.pop('parent')
                    del blockmetadata['style'] # Removes the style attribute as it is very cluttered when printing out and\
                                               # information is not very readable either             
                    blockdata.update(pagedata)
                    blockdata.update(blockmetadata)
                    self.XMLContent.append(blockdata)

        return self.XMLContent

