import yaml


filename1 = 'db/KTH FS Parts and Components - Connectors.tsv'
filename2 = 'db/KTH FS Parts and Components - LEMO Connectors.tsv'


file1 = open(filename1, 'r')
file_data1 = [line.strip().split('\t') for line in file1]
file1.close()
keys1 = file_data1[0]
items1 = file_data1[1:]

file2 = open(filename2, 'r')
file_data2 = [line.strip().split('\t') for line in file2]
file2.close()
keys2 = file_data2[0]
items2 = file_data2[1:]



connectors = {'BoardConnectors':[], 'LEMOConnectors':[]}

for item in items1:
    new_connector = {keys1[i]: item[i] for i in range(len(item))}
    connectors['BoardConnectors'].append(new_connector)

for item in items2:
    new_connector = {keys2[i]: item[i] for i in range(len(item))}
    connectors['LEMOConnectors'].append(new_connector)

with open('db/connectortypes.yaml', 'w') as dumpfile:
    yaml.dump(connectors, dumpfile)
    dumpfile.close()


test_connector = {'MfgPartNumber': 649008113322, 'Family': 'MPC4', 'BlockType': 'FCON', 'Pins': 8, 'VoltageRating': '600', 'CurrentRating': '9'}

ConnExist = False

for conn in connectors['BoardConnectors']:
    if test_connector['Family'] in conn['Family'] and str(test_connector['Pins']) in conn['Pins']:
        if test_connector['BlockType'][0] == conn['Gender']:
            ConnExist = True

print(ConnExist)


test_connector = {'Model': 'HE', 'Series': '0F', 'BlockType': 'LEMO', 'Pins': 4, 'AlignmentKey': 'N', 'Gender': 'F'}

ConnExist = False

for conn in connectors['LEMOConnectors']:
    if test_connector['Model'] in conn['Model'] and str(test_connector['Pins']) in conn['Pins'] and test_connector['Series'] in conn['Series']:
        if test_connector['Gender'][0] == conn['Gender']:
            ConnExist = True

print(ConnExist)
