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
    blocks = []
    block_lookup = dict()

    def __init__(self, config):
        self.config = config



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

        self.diagrams = self.root.findall('diagram')
        self.blocks = self.root.findall('diagram/mxGraphModel/root/object')
        for item in self.blocks:
            block = item.attrib
            if 'BlockType' in block and 'Parent' in block:
                if block['Parent'] not in self.block_lookup:
                    self.block_lookup[block['Parent']] = dict()
                self.block_lookup[block['Parent']][block['Name']] = block

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

        # Dump log file
        if self.config['log_changes']:
            with open(self.config['logfilename'], 'w') as log:
                documents = yaml.dump(self.updatelog, log)
                log.close()

    def backup(self):
        backupdir = self.config['backup_directory']
        if not os.path.exists(backupdir):
            os.mkdir(backupdir)
        backupfilename = backupdir + self.config['diagram_filename']
        self.tree.write(backupfilename)
        self.updatelog.append('Created backup file: ' + backupdir + self.config['diagram_filename'])

    def delete_attributes(self, block, instructions):
        blocktype = block['BlockType']
        if blocktype in instructions:
            for attribute in instructions[blocktype]:
                if attribute in block:
                    block.pop(attribute)
                    self.updatelog.append('Removed attribute ' + str(attribute) + ' in ' + block['Name'])

    def add_attributes(self, block, instructions):
        blocktype = block['BlockType']
        if blocktype in instructions:
            for attribute in instructions[blocktype]:
                if attribute not in block:
                    block[attribute] = instructions[blocktype][attribute]
                    self.updatelog.append('Added attribute ' + str(attribute) + ' in ' + block['Name'])

    def replace_attribute_name(self, block, instructions):
        blocktype = block['BlockType']
        for name_replacement in instructions:
            if blocktype in name_replacement['BlockTypes'] or 'ALL' in name_replacement['BlockTypes']:
                OldAttribName = name_replacement['OldName']
                NewAttribName = name_replacement['NewName']
                if OldAttribName in block:
                    block[NewAttribName] = block[OldAttribName]
                    block.pop(OldAttribName)
                    self.updatelog.append('Replaced attribute name ' + OldAttribName + ' with ' + NewAttribName + ' in ' + block['Name'])

    def replace_property_value(self, block, instructions):
        blocktype = block['BlockType']
        for value_replacement in instructions:
            if blocktype in value_replacement['BlockTypes'] or 'ALL' in value_replacement['BlockTypes']:
                OldValue = value_replacement['OldValue']
                NewValue = value_replacement['NewValue']
                OldVal_len = len(OldValue)
                for attribute in block:
                    while OldValue in block[attribute]:
                        index = block[attribute].find(OldValue)
                        block[attribute] = block[attribute][:index] + NewValue + block[attribute][index+OldVal_len:]
                        self.updatelog.append('Replaced property value ' + OldValue + ' with ' + NewValue + ' in ' + block['Name'] + '/' + attribute)

    def update_diagram_to_library(self):
        # Validate config file
        if 'config_for' not in self.config:
            print("ERROR! Wrong or corupted config file")
            return
        elif self.config['config_for'] != 'diagramupdate':
            print("ERROR! Wrong config file")
            return

        self.parse()

        # Create backup
        if self.config['create_backup']:
            self.backup()

        # do the changes
        for item in self.blocks:
            block = item.attrib
            if 'BlockType' in block:


                # Delete attributes
                if not self.config['keep_attributes']:
                    self.delete_attributes(block, self.config['delete_attributes_for'])

                # Add new attributes
                if self.config['add_new_attributes']:
                    self.add_attributes(block, self.config['add_attributes_for'])

                # Replace attribute names
                if self.config['replace_attributes']:
                    self.replace_attribute_name(block, self.config['replace_attribute_name'])

                # Replace property values
                if self.config['replace_properties']:
                    self.replace_property_value(block, self.config['replace_property_value'])
            else:
                self.updatelog.append(block['Name'] + ' is not a valid block')

        # update diagram
        self.updatelog.append('Updating diagram...')
        self.update()

    def insert_property(self, block_object, attribute_name, property_value):
        name = block_object['Name']
        parent = block_object['Parent']
        self.block_lookup[parent][name][attribute_name] = property_value

    def update_block(self, block_object):
        try:
            name = block_object['Name']
            parent = block_object['Parent']
        except KeyError:
            self.updatelog.append('Failed to update block, invalid block object inserted, name or parent missing')
            return
        try:
            diagram_block = self.block_lookup[parent][name]
        except KeyError:
            self.updatelog.append('Failed to update! Block: ' + parent + '/' + name + '  does not exist in diagram')
            return

        for attribute in block_object.keys():
            insert_made = False
            if attribute not in diagram_block:
                if self.config['add_new_attributes']:
                    diagram_block[attribute] = block_object[attribute]
                    insert_made = True
            elif diagram_block[attribute] != '' and not self.config['keep_properties']:
                diagram_block[attribute] = block_object[attribute]
                insert_made = True
            else:
                diagram_block[attribute] = block_object[attribute]
                insert_made = True
            if insert_made:
                self.updatelog.append('Inserted ' attribute + ': ' + block_object[attribute] + ' into' + parent + '/' + name)

        attributes_to_remove = []
        for attribute in diagram_block:
            if attribute not in block_object and not self.config['keep_attributes']:
                attributes_to_remove.append(attribute)
        for attribute in attributes_to_remove:
            diagram_block.pop(attribute)
