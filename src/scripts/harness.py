from dbmanager import DBManager

def harnessapp(config):
    dbm = DBManager(config)
    dbm.readdb()
    data = dbm.getdata()

    cables = data['cable']
    output = []
    for cable in cables:
        output.append(cable['Parent'] + '/' + cable['Name'])

        # output.append('\tConnectors:')
        for conn in cable['Connectors']:
            output.append('-'*4 + conn['Name'] + ':' + conn['BlockType'])
            try:
                output.append('-'*8 + 'Family: ' + conn['Family'])
            except KeyError:
                output.append('-'*8 +'Part number: ' + conn['PartNumber'])
            for pin in range(1, int(conn['Pins'])+1):
                if pin < 10:
                    pin_key = 'Pin0' + str(pin)
                else:
                    pin_key = 'Pin' + str(pin)
                try:
                    output.append('-'*8 + pin_key + ': ' + conn[pin_key])
                except KeyError:
                    pass
    return output
