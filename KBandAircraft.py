#Lists aircraft that are capable of detecting K band (Pantsir-S1) on their RWRs

import sys
import os
import json
import pandas as pd

rwrs = []
aircraft = set()


def detects_K_band(name, data):
    if data.get("type") == "rwr":
        if data.get("band10") == True:
            return True
    return False

def read_blkx(file):
    with open(file, "r") as f:
        data = json.load(f)
        return data
    
def has_Krwr(name, data):
    sensors = data.get("sensors")
    if sensors != None:
        for s in sensors.get("sensor"):
            if isinstance(s, dict):
                sensor = os.path.splitext(os.path.basename(s['blk']))[0]
                if sensor in rwrs:
                    aircraft.add(name)

#MAIN

datamine_dir = os.path.abspath(sys.argv[1])

sensors_dir = os.path.join(datamine_dir, 'aces.vromfs.bin_u', 'gamedata', 'sensors');

for filename in os.listdir(sensors_dir):
    f = os.path.join(sensors_dir, filename)
    if os.path.isfile(f):
        data = read_blkx(f)
        sensor_name = os.path.splitext(os.path.basename(f))[0]

        if detects_K_band(sensor_name, data):
            rwrs.append(sensor_name)

fm_dir = os.path.join(datamine_dir, 'aces.vromfs.bin_u', 'gamedata', 'flightmodels');

for filename in os.listdir(fm_dir):
    f = os.path.join(fm_dir, filename)
    if os.path.isfile(f):
        aircraft_name = os.path.splitext(os.path.basename(f))[0]
        data = read_blkx(f)
        has_Krwr(aircraft_name, data)


loc_units_file = os.path.join(datamine_dir, 'lang.vromfs.bin_u', 'lang', 'units.csv')

units_localization = pd.read_csv(loc_units_file, on_bad_lines='skip', delimiter=';')

for a in aircraft:
    key = a + '_0'
    if key in units_localization.iloc[:, 0].values:
        row_index = units_localization.index[units_localization.iloc[:, 0] == key].tolist()[0]
        string_in_first_language = units_localization.iloc[row_index, 1]
        print(string_in_first_language. encode('ascii', 'ignore').decode('ascii'))