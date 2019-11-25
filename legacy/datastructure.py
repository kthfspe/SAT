# Strategy 1: Read all data to individual dict and then store as one list. This list is loaded to json file raw.json.
#             Refine.py reads this creats objects for each record and removes redundant records of each type.
# Strategy 2: Read all data to individual dict and then store as one list. This list is loaded to json file raw.json.
#             We create a reader.py with argument blocktype and it reads the raw file and stores it to your program for further processing.
#             In this case or the first one the reader.py will dynamically remove redundant ones and merge content.
            
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

