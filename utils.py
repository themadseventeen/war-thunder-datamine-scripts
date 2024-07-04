# Utility to be used inside other scripts

import csv
import os
import json

class datamine:
    localization_initialized = False
    files = {
        "localization_units" : os.path.join('lang.vromfs.bin_u', 'lang', 'units.csv'),
        "flightmodel_dir"    : os.path.join('aces.vromfs.bin_u', 'gamedata', 'flightmodels'),
        "sensors_dir"        : os.path.join('aces.vromfs.bin_u', 'gamedata', 'sensors'),
        "aces"               : os.path.join('aces.vromfs.bin_u')
    
    }
    def __init__(self, datamine_path):
        self.path = datamine_path
    def get_file(self, file):
        return os.path.join(self.path, self.files[file])


def archive_init(path):
    global archive
    archive = datamine(path)

def read_blkx(file):
    with open(file, "r") as f:
        data = json.load(f)
        return data

# Localization

localization_file = None

def localization_init():
    global localization_file
    with open(archive.get_file("localization_units"), "rt", encoding="utf8", errors="ignore") as source:
        localization_file = list(csv.reader(source, delimiter = ';'))

def localized_unit(string):
    global localization_file
    if localization_file == None:
        localization_init()
        
    string += "_0"

    for row in localization_file:
        if string == row[0].casefold():
            if row[1] == "":
                lstring = string
            else:
                lstring = row[1]
    if lstring == "":
        lstring = string
    return lstring

# FM related

def get_sensors(fm_blkx):
    ret = []
    sensors_dict = fm_blkx.get("sensors")
    if sensors_dict != None:
        sensors = sensors_dict.get("sensor")
        if isinstance(sensors, list): # multiple sensors
            # print("TYPE : list")
            # print(sensors)
            for s in sensors:
                # print(s)
                ret.append(s)
        elif isinstance(sensors, dict): # one sensor
            # print("TYPE : dict")
            # print(sensors)
            ret.append(sensors)
    return ret

def get_rwrs(fm_blkx):
    ret = []
    sensors = get_sensors(fm_blkx)
    for s in sensors:
        path = os.path.join(archive.get_file('aces'), s['blk'].lower()) + 'x'
        blk = read_blkx(path)
        if blk.get("type") == "rwr":
            ret.append(blk)
    cockpit = fm_blkx.get("cockpit")
    if cockpit != None:
        rwr = cockpit.get("rwr")
        if rwr != None:
            # print(rwr)
            ret.append(rwr)
    return ret

def rwr_bands(rwr):
    ret = [0] * 16
    for i in range(16):
        if rwr.get("band" + str(i)) != None:
            ret[i] = 1
    return ret