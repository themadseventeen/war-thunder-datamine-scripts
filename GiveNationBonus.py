#Lists vehicles that give next nation bonus

import sys
import os
import json
import pandas as pd

#MAIN

datamine_dir = os.path.abspath(sys.argv[1])

wpcost_path = os.path.join(datamine_dir, 'char.vromfs.bin_u', 'config', 'wpcost.blkx');

vehicles = []

with open(wpcost_path, "r") as f:
    wpcost = json.load(f)

i = 0
for key in wpcost.keys():
    if key == "economicRankMax":
        continue
    if wpcost[key].get("doesItGiveNationBonus") == True:
        vehicles.append(key)       

loc_units_file = os.path.join(datamine_dir, 'lang.vromfs.bin_u', 'lang', 'units.csv')

units_localization = pd.read_csv(loc_units_file, on_bad_lines='skip', delimiter=';')

for v in vehicles:
    key = v + '_0'
    if key in units_localization.iloc[:, 0].values:
        row_index = units_localization.index[units_localization.iloc[:, 0] == key].tolist()[0]
        string_in_first_language = units_localization.iloc[row_index, 1]
        print(string_in_first_language. encode('ascii', 'ignore').decode('ascii') + " (" + v + ")")