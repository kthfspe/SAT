class digital:
    data = dict()

    def __str__(self):
        return "Digital"

test = digital()
test.data = dict([
    ('Colorado', 'Rockies'),
    ('Boston', 'Red Sox'),
    ('Colorado2', 'Rockies'),
    ('Bostone', 'Red Sox'),

])

class analog:
    data = dict()

    def __str__():
        return "Analog"

test2 = analog()
test2.data = dict([
    ('Colorado', 'Rockies'),
    ('Boston', 'Red Sox'),
])
master = []
master.append(test)
master.append(test2)
print (master[0])

import json

with open("data_file.json", "w") as write_file:
    json.dump(master[0].data, write_file)
    json.dump(master[1].data, write_file)

