import json


with open("data_file.json", "w") as write_file:
    json.dump(master[0].data, write_file, indent = 4)
    json.dump(master[1].data, write_file, indent = 4)

with open("data_file.json", "r") as read_file:
    readdata = json.load(read_file)

print(type(readdata))