import os
import xml.etree.ElementTree as ET
import yaml
from github import Github
import base64

class DiagramManager:
    updatelog = []
    gitobject = None
    repo = None
    gitpat = None
    XMLContent = [None]
    config = dict()
    Logged_in = False
    def __init__(self, config):
        self.config = config

        # Validate config file
        if 'config_for' not in self.config:
            print("ERROR! Wrong or corupted config file")
            return
        elif self.config['config_for'] != 'diagramupdate':
            print("ERROR! Wrong config file")
            return

    def gitlogin(self, pat):
        self.gitpat = pat
        self.gitobject = Github(pat)
        try:
            self.repo = self.gitobject.get_repo(self.config["gitaccount"]+"/"+self.config["gitrepo"])
            self.Logged_in = True
        except:
            print("Access Denied. Check your Personal Access Token and your access to repo kthfspe/SA")
            self.Logged_in = False
        return self.Logged_in

    def parse(self):
        if self.config['parsefromgithub']:
            if not self.Logged_in:
                print('ERROR! Not logged in to Github')
                return
            path = self.config['diagram_directory'] + self.config['diagram_filename']
            self.updatelog.append('Parsing file from github directory: ' + self.config["gitaccount"]+"/"+self.config["gitrepo"] + '/' + path)
            self.repo = self.gitobject.get_repo(self.config["gitaccount"]+"/"+self.config["gitrepo"])
            self.contents = self.repo.get_contents(str(path))
            self.stringcontent = base64.b64decode(self.contents.content)
            self.root = ET.fromstring(self.stringcontent)
            self.tree = ET.ElementTree(self.root)
        else:
            path = self.config['diagram_directory'] + self.config['diagram_filename']
            self.updatelog.append('Parsing file from local directory: ' + path)
            try:
                self.tree = ET.parse(path)
            except FileNotFoundError:
                print('ERROR! No such file or directory...')
                return
            self.root = self.tree.getroot()

    def update(self):
        if self.config['create_output_file']:
            outputdir = self.config['output_directory']
            if not os.path.exists(outputdir):
                os.mkdir(outputdir)
            outputfilename = outputdir + self.config['diagram_filename']
            self.tree.write(outputfilename)
            self.updatelog.append('Created output file: ' + outputdir + self.config['diagram_filename'])
        if self.config['commit_to_github']:
            # Commit to github...
            pass

    def update_diagram_to_library(self):

        self.parse()

        # Create backup
        if self.config['create_backup']:
            backupdir = self.config['backup_directory']
            if not os.path.exists(backupdir):
                os.mkdir(backupdir)
            backupfilename = backupdir + self.config['diagram_filename']
            self.tree.write(backupfilename)
            self.updatelog.append('Created backup file: ' + backupdir + self.config['diagram_filename'])

        # do the changes
        for child in self.root.findall('diagram'):
            for item in child.iterfind('mxGraphModel/root/object'):

                if 'BlockType' in item.attrib:

                    # Delete attributes
                    if item.attrib['BlockType'] in self.config['delete_attributes_for']:
                        for attribute in self.config['delete_attributes_for'][item.attrib['BlockType']]:
                            if attribute in item.attrib:
                                item.attrib.pop(attribute)
                                self.updatelog.append('Removed attribute ' + str(attribute) + ' in ' + item.attrib['Name'])


                    # Add new attributes
                    if item.attrib['BlockType'] in self.config['add_attributes_for']:
                        for attribute in self.config['add_attributes_for'][item.attrib['BlockType']]:
                            if attribute not in item.attrib:
                                item.attrib[attribute] = ''
                                self.updatelog.append('Added attribute ' + str(attribute) + ' in ' + item.attrib['Name'])
                else:
                    self.updatelog.append(item.attrib['Name'] + ' is not a valid block')


        # update diagram
        self.updatelog.append('Updating diagram...')
        self.update()


        # Dump log file
        if self.config['log_changes']:
            with open(self.config['logfilename'], 'w') as log:
                documents = yaml.dump(self.updatelog, log)
                log.close()
