#Lists aircraft that are capable of detecting K band (Pantsir-S1) on their RWRs

import sys
import os
import json
import pandas as pd
import utils


def detects_K_band(data):
    if data.get("type") == "rwr":
        if data.get("band10") == True:
            return True
    return False
    
def has_Krwr(data, rwrs):
    sensors = data.get("sensors")
    if sensors != None:
        for s in sensors.get("sensor"):
            if isinstance(s, dict):
                sensor = os.path.splitext(os.path.basename(s['blk']))[0]
                if sensor in rwrs:
                    return True

def get_aircraft():
    rwrs = []
    aircraft = set()
    sensors_dir = utils.archive.get_file("sensors_dir")
    fm_dir =      utils.archive.get_file("flightmodel_dir")

    for filename in os.listdir(sensors_dir):
        f = os.path.join(sensors_dir, filename)
        if os.path.isfile(f):
            data = utils.read_blkx(f)
            sensor_name = os.path.splitext(os.path.basename(f))[0]

            if detects_K_band(data):
                rwrs.append(sensor_name)


    for filename in os.listdir(fm_dir):
        f = os.path.join(fm_dir, filename)
        if os.path.isfile(f):
            aircraft_name = os.path.splitext(os.path.basename(f))[0]
            data = utils.read_blkx(f)
            if has_Krwr(data, rwrs):
                aircraft.add(aircraft_name)
    return aircraft

def main():
    utils.archive_init(sys.argv[1])

    aircraft = get_aircraft()
    for a in aircraft:
        print(utils.localized_unit(a))

if __name__ == "__main__":
    main()
