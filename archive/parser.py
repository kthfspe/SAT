import xml.etree.ElementTree as ET
import csv
import xlsxwriter


#Test commit
Verbose = 0 # 1: To print processing details or not, 0: For minimal
id = dict()
ecus = dict()
sensors = dict()
actuators = dict()
hmi = dict()
otsc = dict()
enclosures = dict()
connectors = dict()
npc = dict()
pc = dict()
swc = dict()
f_cansignals = dict()
f_analogsignals = dict()
f_digitalsignals = dict()
f_internalsignals = dict()
f_lvsignals = dict()
f_hvsignals = dict()
f_gndsignals = dict()
f_signals = dict()

p_cansignals = dict()
p_analogsignals = dict()
p_digitalsignals = dict()
p_internalsignals = dict()
p_lvsignals = dict()
p_hvsignals = dict()
p_gndsignals = dict()
p_signals = dict()

idcount = 1
ecucount = 0
sensorcount = 0
actuatorcount = 0
otsccount = 0
enclosurecount = 0
hmicount = 0
npccount = 0
pccount = 0
swccount = 0
uniquecount = 0
f_cansignalcount = 0
f_digitalsignalcount = 0
f_analogsignalcount = 0
f_internalsignalcount = 0
f_hvsignalcount = 0
f_lvsignalcount = 0
f_gndsignalcount = 0
f_signalcount = 0

p_cansignalcount = 0
p_digitalsignalcount = 0
p_analogsignalcount = 0
p_internalsignalcount = 0
p_hvsignalcount = 0
p_lvsignalcount = 0
p_gndsignalcount = 0
p_signalcount = 0


# Read data store by BlockType
# Each block is stored in its own dict.
# All signals are stored in one dict
def readid(a):
    global id
    global idcount
    b = dict((k, a[k]) for k in ('Name', 'BlockType', 'id', 'Parent'))
    id.update({idcount:b})
    idcount += 1

def p_readsignal(child):
    global p_signals
    global p_signalcount
    global id
    s = dict()
    b = dict((k, child.attrib[k]) for k in ('Name', 'BlockType')) #Add from connector to connector
    for item in id:
        if id[item]['id'] == child[0].attrib['source']:
            s = {'Source' : id[item]['Name']}
        if id[item]['id'] == child[0].attrib['target']:
            t = {'Target' : id[item]['Name']}
    z = b.copy()
    z.update(s)
    d = z.copy()
    d.update(t)
    p_signals.update({p_signalcount+1:d})
    p_signalcount += 1

def f_readsignal(child):
    global f_signals
    global f_signalcount
    global id

    b = dict((k, child.attrib[k]) for k in ('Name', 'BlockType')) #Add from connector to connector
    for item in id:
        if id[item]['id'] == child[0].attrib['source']:
            s1 = {'Source' : id[item]['Name']}
        if id[item]['id'] == child[0].attrib['target']:
            t = {'Target' : id[item]['Name']}
    z = b.copy()
    z.update(s1)
    d = z.copy()
    d.update(t)
    f_signals.update({f_signalcount+1:d})
    f_signalcount += 1

root = ET.parse('testfiles/physical.xml').getroot()
for child in root.findall('diagram/mxGraphModel/root/object'):
    a = dict(child.attrib)
    #print(child.attrib["BlockType"])
    if child.attrib["BlockType"].lower() == 'sen':
        if sensorcount == 0:
            sensors.update({sensorcount+1:a})
            sensorcount += 1
        else:
            for item in range(1,sensorcount+1):
                if (sensors[item]["Name"].lower() != child.attrib["Name"].lower()):
                    uniquecount += 1
            if uniquecount == sensorcount:
                sensors.update({sensorcount+1:a})
                sensorcount += 1
            uniquecount = 0
        readid(a)

    elif child.attrib["BlockType"].lower() == 'act':
        if actuatorcount == 0:
            actuators.update({actuatorcount+1:a})
            actuatorcount += 1
        else:
            for item in range(1,actuatorcount+1):
                if (actuators[item]["Name"].lower() != child.attrib["Name"].lower()):
                    uniquecount += 1
            if uniquecount == actuatorcount:
                actuators.update({actuatorcount+1:a})
                actuatorcount += 1
            uniquecount = 0
        readid(a)

    elif child.attrib["BlockType"].lower() == 'hmi':
        if hmicount == 0:
            hmi.update({hmicount+1:a})
            hmicount += 1
        else:
            for item in range(1,hmicount+1):
                if (hmi[item]["Name"].lower() != child.attrib["Name"].lower()):
                    uniquecount += 1
            if uniquecount == hmicount:
                hmi.update({hmicount+1:a})
                hmicount += 1
            uniquecount = 0
        readid(a)

    elif child.attrib["BlockType"].lower() == 'otsc':
        if otsccount == 0:
            otsc.update({otsccount+1:a})
            otsccount += 1
        else:
            for item in range(1,otsccount+1):
                if (otsc[item]["Name"].lower() != child.attrib["Name"].lower()):
                    uniquecount += 1
            if uniquecount == otsccount:
                otsc.update({otsccount+1:a})
                otsccount += 1
            uniquecount = 0
        readid(a)


    elif child.attrib["BlockType"].lower() == 'ecu':
        if ecucount == 0:
            ecus.update({ecucount+1:a})
            ecucount += 1
        else:
            for item in range(1,ecucount+1):
                if (ecus[item]["Name"].lower() != child.attrib["Name"].lower()):
                    uniquecount += 1
            if uniquecount == ecucount:
                ecus.update({ecucount+1:a})
                ecucount += 1
            uniquecount = 0
        readid(a)

    elif child.attrib["BlockType"].lower() == 'enc':
        if enclosurecount == 0:
            enclosures.update({enclosurecount+1:a})
            enclosurecount += 1
        else:
            for item in range(1,enclosurecount+1):
                if (enclosures[item]["Name"].lower() != child.attrib["Name"].lower()):
                    uniquecount += 1
            if uniquecount == enclosurecount:
                enclosures.update({enclosurecount+1:a})
                enclosurecount += 1
            uniquecount = 0
        readid(a)

    elif child.attrib["BlockType"].lower() == 'con':
        if connectorcount == 0:
            connectors.update({connectorcount+1:a})
            connectorcount += 1
        else:
            for item in range(1,connectorcount+1):
                if (connectors[item]["Name"].lower() != child.attrib["Name"].lower()):
                    uniquecount += 1
            if uniquecount == connectorcount:
                connectors.update({connectorcount+1:a})
                connectorcount += 1
            uniquecount = 0
        readid(a)


root = ET.parse('testfiles/functional.xml').getroot()
Verbose = 0 # 1: To print processing details or not, 0: For minimal

# Read data store by BlockType
# Each block is stored in its own dict.
# All signals are stored in one dict

for child in root.findall('diagram/mxGraphModel/root/object'):
    a = dict(child.attrib)

    if child.attrib["BlockType"].lower() == 'npc':
        if npccount == 0:
            npc.update({npccount+1:a})
            npccount += 1
        else:
            for item in range(1,npccount+1):
                if (npc[item]["Name"].lower() != child.attrib["Name"].lower()):
                    uniquecount += 1
            if uniquecount == npccount:
                npc.update({npccount+1:a})
                npccount += 1
            uniquecount = 0
        readid(a)

    elif child.attrib["BlockType"].lower() == 'pc':
        if pccount == 0:
            pc.update({pccount+1:a})
            pccount += 1
        else:
            for item in range(1,pccount+1):
                if (pc[item]["Name"].lower() != child.attrib["Name"].lower()):
                    uniquecount += 1
            if uniquecount == pccount:
                pc.update({pccount+1:a})
                pccount += 1
            uniquecount = 0
        readid(a)

    elif child.attrib["BlockType"].lower() == 'swc':
        if swccount == 0:
            swc.update({swccount+1:a})
            swccount += 1
        else:
            for item in range(1,swccount+1):
                if (swc[item]["Name"].lower() != child.attrib["Name"].lower()):
                    uniquecount += 1
            if uniquecount == swccount:
                swc.update({swccount+1:a})
                swccount += 1
            uniquecount = 0
        readid(a)



for child in root.findall('diagram/mxGraphModel/root/object'):
    a = dict(child.attrib)

    if child.attrib["BlockType"].lower() == 'can':
        f_cansignals.update({f_cansignalcount+1:a})
        f_cansignalcount += 1
        f_readsignal(child)

    elif child.attrib["BlockType"].lower() == 'dig':
        f_digitalsignals.update({f_digitalsignalcount+1:a})
        f_digitalsignalcount += 1
        f_readsignal(child)

    elif child.attrib["BlockType"].lower() == 'ana':
        f_analogsignals.update({f_analogsignalcount+1:a})
        f_analogsignalcount += 1
        f_readsignal(child)

    elif child.attrib["BlockType"].lower() == 'iv':
        f_internalsignals.update({f_internalsignalcount+1:a})
        f_internalsignalcount += 1
        f_readsignal(child)

    elif child.attrib["BlockType"].lower() == 'lvs':
        f_lvsignals.update({f_lvsignalcount+1:a})
        f_lvsignalcount += 1
        f_readsignal(child)

    elif child.attrib["BlockType"].lower() == 'hvs':
        f_hvsignals.update({f_hvsignalcount+1:a})
        f_hvsignalcount += 1
        f_readsignal(child)

    elif child.attrib["BlockType"].lower() == 'gnd':
        f_gndsignals.update({f_gndsignalcount+1:a})
        f_gndsignalcount += 1
        f_readsignal(child)

root = ET.parse('testfiles/physical.xml').getroot()
for child in root.findall('diagram/mxGraphModel/root/object'):
    a = dict(child.attrib)
    if child.attrib["BlockType"].lower() == 'can':
        p_cansignals.update({p_cansignalcount+1:a})
        p_cansignalcount += 1
        p_readsignal(child)

    elif child.attrib["BlockType"].lower() == 'dig':
        p_digitalsignals.update({p_digitalsignalcount+1:a})
        p_digitalsignalcount += 1
        p_readsignal(child)

    elif child.attrib["BlockType"].lower() == 'ana':
        p_analogsignals.update({p_analogsignalcount+1:a})
        p_analogsignalcount += 1
        p_readsignal(child)

    elif child.attrib["BlockType"].lower() == 'iv':
        p_internalsignals.update({p_internalsignalcount+1:a})
        p_internalsignalcount += 1
        p_readsignal(child)

    elif child.attrib["BlockType"].lower() == 'lvs':
        p_lvsignals.update({p_lvsignalcount+1:a})
        p_lvsignalcount += 1
        p_readsignal(child)

    elif child.attrib["BlockType"].lower() == 'hvs':
        p_hvsignals.update({p_hvsignalcount+1:a})
        p_hvsignalcount += 1
        p_readsignal(child)

    elif child.attrib["BlockType"].lower() == 'gnd':
        p_gndsignals.update({p_gndsignalcount+1:a})
        p_gndsignalcount += 1
        p_readsignal(child)

# If checks passed, export to CSV, print total number of signals, units etc.


# Else print error message

# Glossary sheet 

workbook = xlsxwriter.Workbook('SysArch.xlsx')
idsheet = workbook.add_worksheet('ID')
for item in id:
    col = 0
    for key in id[item].keys():
        idsheet.write(0, col, key)
        idsheet.write(item, col, id[item][key])
        col += 1

f_signalsheet = workbook.add_worksheet('Signals P')
for item in f_signals:
    col = 0
    for key in f_signals[item].keys():
        f_signalsheet.write(0, col, key)
        f_signalsheet.write(item, col, f_signals[item][key])
        col += 1
p_signalsheet = workbook.add_worksheet('Signals F')
for item in p_signals:
    col = 0
    for key in p_signals[item].keys():
        p_signalsheet.write(0, col, key)
        p_signalsheet.write(item, col, p_signals[item][key])
        col += 1

ecusheet = workbook.add_worksheet('ECUs')
for item in ecus:
    col = 0
    for key in ecus[item].keys():
        ecusheet.write(0, col, key)
        ecusheet.write(item, col, ecus[item][key])
        col += 1

sensorsheet = workbook.add_worksheet('Sensors')
for item in sensors:
    col = 0
    for key in sensors[item].keys():
        sensorsheet.write(0, col, key)
        sensorsheet.write(item, col, sensors[item][key])
        col += 1

actuatorsheet = workbook.add_worksheet('Actuators')
for item in actuators:
    col = 0
    for key in actuators[item].keys():
        actuatorsheet.write(0, col, key)
        actuatorsheet.write(item, col, actuators[item][key])
        col += 1

hmisheet = workbook.add_worksheet('HMI')
for item in hmi:
    col = 0
    for key in hmi[item].keys():
        hmisheet.write(0, col, key)
        hmisheet.write(item, col, hmi[item][key])
        col += 1

otscsheet = workbook.add_worksheet('OTSC')
for item in otsc:
    col = 0
    for key in otsc[item].keys():
        otscsheet.write(0, col, key)
        otscsheet.write(item, col, otsc[item][key])
        col += 1

connectorsheet = workbook.add_worksheet('Connectors')
for item in connectors:
    col = 0
    for key in connectors[item].keys():
        connectorsheet.write(0, col, key)
        connectorsheet.write(item, col, connectors[item][key])
        col += 1

npcsheet = workbook.add_worksheet('NPC')
for item in npc:
    col = 0
    for key in npc[item].keys():
        npcsheet.write(0, col, key)
        npcsheet.write(item, col, npc[item][key])
        col += 1

pcsheet = workbook.add_worksheet('PC')
for item in pc:
    col = 0
    for key in pc[item].keys():
        pcsheet.write(0, col, key)
        pcsheet.write(item, col, pc[item][key])
        col += 1

swcsheet = workbook.add_worksheet('SWC')
for item in swc:
    col = 0
    for key in swc[item].keys():
        swcsheet.write(0, col, key)
        swcsheet.write(item, col, swc[item][key])
        col += 1

dig = workbook.add_worksheet('Digital Signals')
for item in p_digitalsignals:
    col = 0
    for key in p_digitalsignals[item].keys():
        dig.write(0, col, key)
        dig.write(item  , col, p_digitalsignals[item][key])
        col += 1
net = item
for item in f_digitalsignals:
    col = 0
    for key in f_digitalsignals[item].keys():
        dig.write(0, col, key)
        dig.write(item+net  , col, f_digitalsignals[item][key])
        col += 1

analog = workbook.add_worksheet('Analog Signals')
for item in p_analogsignals:
    col = 0
    for key in p_analogsignals[item].keys():
        analog.write(0, col, key)
        analog.write(item  , col, p_analogsignals[item][key])
        col += 1
net = item
for item in f_analogsignals:
    col = 0
    for key in f_analogsignals[item].keys():
        analog.write(0, col, key)
        analog.write(item+net  , col, f_analogsignals[item][key])
        col += 1

can = workbook.add_worksheet('CAN')
for item in f_cansignals:
    col = 0
    for key in f_cansignals[item].keys():
        can.write(0, col, key)
        can.write(item  , col, f_cansignals[item][key])
        col += 1
net = item
for item in p_cansignals:
    col = 0
    for key in p_cansignals[item].keys():
        can.write(0, col, key)
        can.write(item+net  , col, p_cansignals[item][key])
        col += 1

internal = workbook.add_worksheet('Internal Signals')
for item in f_internalsignals:
    col = 0
    for key in f_internalsignals[item].keys():
        internal.write(0, col, key)
        internal.write(item  , col, f_internalsignals[item][key])
        col += 1
net = item
for item in p_internalsignals:
    col = 0
    for key in p_internalsignals[item].keys():
        internal.write(0, col, key)
        internal.write(item+net  , col, p_internalsignals[item][key])
        col += 1
lv = workbook.add_worksheet('LV Supply')
for item in f_lvsignals:
    col = 0
    for key in f_lvsignals[item].keys():
        lv.write(0, col, key)
        lv.write(item  , col, f_lvsignals[item][key])
        col += 1
net = item
for item in p_lvsignals:
    col = 0
    for key in p_lvsignals[item].keys():
        lv.write(0, col, key)
        lv.write(item+net  , col, p_lvsignals[item][key])
        col += 1

hv = workbook.add_worksheet('HV Supply')
for item in p_hvsignals:
    col = 0
    for key in p_hvsignals[item].keys():
        hv.write(0, col, key)
        hv.write(item  , col, p_hvsignals[item][key])
        col += 1
net = item
for item in f_hvsignals:
    col = 0
    for key in f_hvsignals[item].keys():
        hv.write(0, col, key)
        hv.write(item+net  , col, f_hvsignals[item][key])
        col += 1

gnd = workbook.add_worksheet('GND')
for item in f_gndsignals:
    col = 0
    for key in f_gndsignals[item].keys():
        gnd.write(0, col, key)
        gnd.write(item , col, f_gndsignals[item][key])
        col += 1
net = item
for item in p_gndsignals:
    col = 0
    for key in p_gndsignals[item].keys():
        gnd.write(0, col, key)
        gnd.write(item+net  , col, p_gndsignals[item][key])
        col += 1
workbook.close()
#print(digitalsignals)
