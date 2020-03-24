from dbmanager import DBManager

def findfieldapp(fieldtosearch, config):
    dbm = DBManager(config)
    dbm.readdb()
    data = dbm.getdata()
    result = []
    for item in data['globaliddata']:
        for field in data['globaliddata'][item]:
            if data['globaliddata'][item][field] == fieldtosearch:
                result.append(data['globaliddata'][item])
    if result != []:
        return result
    return [{"Message":"Name not found!"}]