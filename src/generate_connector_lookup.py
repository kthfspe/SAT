import yaml
import sys
import os
sys.path.insert(0,os.getcwd()+"/scripts")
from configmanager import ConfigManager

configman = ConfigManager()



BC_filename = 'db/KTH FS Parts and Components - Connectors.tsv'
LEMO_filename = 'db/KTH FS Parts and Components - LEMO Connectors.tsv'


BC_file = open(BC_filename, 'r')
BC_file_data = [line.strip().split('\t') for line in BC_file]
BC_file.close()
BC_keys = BC_file_data[0]
BC_list = BC_file_data[1:]

LEMO_file = open(LEMO_filename, 'r')
LEMO_file_data = [line.strip().split('\t') for line in LEMO_file]
LEMO_file.close()
LEMO_keys = LEMO_file_data[0]
LEMO_list = LEMO_file_data[1:]


connector_lookup_table = dict()


for item in LEMO_list:
    newkey = ''
    newconn = {LEMO_keys[i]: item[i] for i in range(len(item))}

    for field in configman.configdata['LEMOConnectors_matchfields']:
        newkey += newconn[field]
    connector_lookup_table[newkey] = newconn

for item in BC_list:
    newkey = ''
    newconn = {BC_keys[i]: item[i] for i in range(len(item))}
    # print(newconn)
    for field in configman.configdata['BoardConnectors_matchfields']:
        newkey += newconn[field]
    connector_lookup_table[newkey] = newconn


with open(configman.configdata['connectorlookuptablefilename'], 'w') as lookup_table_file:
    yaml.dump(connector_lookup_table, lookup_table_file)
    lookup_table_file.close()
