import sys
import os
import json
import utils
from pprint import pprint

datamine_dir = os.path.abspath(sys.argv[1])

wpcost_path = os.path.join(datamine_dir, 'char.vromfs.bin_u', 'config', 'wpcost.blkx');

reqExp = dict()

with open(wpcost_path, "r") as f:
    wpcost = json.load(f)

for key in wpcost.keys():
    if key == "economicRankMax":
        continue
    if wpcost[key].get("reqExp") == None:
        reqExp[key] = 0
        continue
    if wpcost[key].get("value") == None or wpcost[key].get("value") == 0:
        reqExp[key] = 0
        continue
    reqExp[key] = wpcost[key].get("reqExp")

shop_path = os.path.join(datamine_dir, 'char.vromfs.bin_u', 'config', 'shop.blkx');
with open(shop_path, "r") as f:
    shop = json.load(f)

total = dict()

for country in shop.keys():
    total[country] = dict()
    for branch in shop[country]:
        total[country][branch] = 0
        for tmp in shop[country][branch]:
            for group in shop[country][branch][tmp]:
                folders = group.keys()
                for folder in folders:
                    if "rank" not in group[folder]:
                        for vehicle in group[folder]:
                            if type(group[folder][vehicle]) is str:
                                continue
                            total[country][branch] += reqExp[vehicle]
                    else:
                        total[country][branch] += reqExp[folder]
                        pass

pprint(total)