#Lists aircraft that are capable of detecting K band (Pantsir-S1) on their RWRs

import sys
import os
import json
import pandas as pd
import utils

def has_band(data, band):
    rwrs = utils.get_rwrs(data)
    for r in rwrs:
        bands = utils.rwr_bands(r)
        if bands[10] == 1:
            return True
    return False

def get_aircraft(band):
    aircraft = set()
    fm_dir = utils.archive.get_file("flightmodel_dir")

    for filename in os.listdir(fm_dir):
        f = os.path.join(fm_dir, filename)
        if os.path.isfile(f):
            aircraft_name = os.path.splitext(os.path.basename(f))[0]
            data = utils.read_blkx(f)
            if has_band(data, band):
                aircraft.add(aircraft_name)
    return aircraft

def main():
    utils.archive_init(sys.argv[1])
    band = sys.argv[2];
    if (len(band) != 1 or (band < 'A' or band > 'Z')):
        print("Input a band in it's uppercase letter form (A, B, C...)")
        return

    aircraft = get_aircraft(band)
    for a in aircraft:
        print(utils.localized_unit(a))

if __name__ == "__main__":
    main()
