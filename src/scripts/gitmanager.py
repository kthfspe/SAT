from github import Github
import xml.etree.ElementTree as ET
import base64
import os

class GitManager:
    gitobject = None
    repo = None
    gitpat = None
    XMLContent = [None]                                                         # Unused
    config = dict()
    def __init__(self):
        pass

    def gitlogin(self, pat, config):
        self.config = config
        self.gitpat = pat
        self.gitobject = Github(pat)
        try:
            self.repo = self.gitobject.get_repo(self.config["gitaccount"]+"/"+self.config["gitrepo"])
            return True
        except:
            print("Access Denied. Check your Personal Access Token and your access to repo kthfspe/SA")
            return False

    def readfile(self, path):
        blockpositiondata = dict()
        filename = os.path.basename(str(path))
        self.XMLContent = [] #Empties the XMLContent container for reading a new file
        self.repo = self.gitobject.get_repo(self.config["gitaccount"]+"/"+self.config["gitrepo"])
        self.contents = self.repo.get_contents(str(path))
        self.stringcontent = base64.b64decode(self.contents.content)
        self.root = ET.fromstring(self.stringcontent)
        for child in self.root.findall('diagram'):
            pagedata = child.attrib
            if 'name' in pagedata:
                pagedata['PageName'] = pagedata.pop('name')
                pagedata['PageId'] = pagedata.pop('id')
                pagedata['FileName'] = filename
                for item in child.iterfind('mxGraphModel/root/object'):
                    blockdata = item.attrib
                    blockmetadata = item[0].attrib
                    blockpositiondata.clear()
                    for item2 in item.iterfind('mxCell/mxGeometry'):
                        blockpositiondata = item2.attrib
                    signalpositiondata = dict()
                    for item3 in item.iterfind('mxCell/mxGeometry/mxPoint'):
                        if item3.attrib['as'] != 'offset':
                            if item3.attrib['as'] == 'sourcePoint':
                                signalpositiondata['source_x'] = item3.attrib['x']
                                signalpositiondata['source_y'] = item3.attrib['y']
                            if item3.attrib['as'] == 'targetPoint':
                                signalpositiondata['target_x'] = item3.attrib['x']
                                signalpositiondata['target_y'] = item3.attrib['y']
                    if "parent" in blockmetadata:
                        blockmetadata['MetaParent'] = blockmetadata.pop('parent')
                        del blockmetadata['style'] # Removes the style attribute as it is very cluttered when printing out and\
                                               # information is not very readable either
                    blockdata.update(blockmetadata)
                    blockdata.update(pagedata)
                    blockdata.update(blockpositiondata)
                    blockdata.update(signalpositiondata)
                    self.XMLContent.append(blockdata)

        return self.XMLContent
