import json

def readdrawiofile():
    pass

def writetextfile():
    pass

def writecsvfile():
    pass

def loadrawdb( rp, rf):
    raw_physical = rp
    raw_functional = rf
    with open("raw_pdb.json", 'w') as fout:
        json.dump(raw_physical, fout)

    with open('raw_pdb.json', 'r') as fp:
        data = json.load(fp)


    with open("raw_fdb.json", 'w') as fout:
        json.dump(raw_functional, fout)

    with open('raw_fdb.json', 'r') as fp:
        data = json.load(fp)
    #self.raw_pdb.insert_multiple(rp)
    #Load to json file locally and return path and status