# Utility to be used inside other scripts

import csv
import os
import json

class datamine:
    localization_initialized = False
    files = {
        "localization_units" : os.path.join('lang.vromfs.bin_u', 'lang', 'units.csv'),
        "flightmodel_dir"    : os.path.join('aces.vromfs.bin_u', 'gamedata', 'flightmodels'),
        "sensors_dir"        : os.path.join('aces.vromfs.bin_u', 'gamedata', 'sensors')
    
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