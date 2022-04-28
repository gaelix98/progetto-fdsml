import json as js, pandas, os, re
from matplotlib import pyplot as plt

dataset_completo_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/dataset_completo.json"
cf_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/cf.json"

f = open(dataset_completo_path, "r")
dataset = js.load(f)

dictionary = dict()

for account, info in dataset.items():
    if account == "dylanchristopher":
        continue
    
    locations = []
    max_location = None
    if len(info["info_locations"]) > 0:
        max_location = info["info_locations"][0]
        for loc in info["info_locations"]:
            if loc == max_location:
                continue
            if loc["occurrences"] > max_location["occurrences"]:
                max_location = loc
            elif loc["occurrences"] == max_location["occurrences"]:
                locations.append(loc)

    remove_obj = []
    for locs in locations:
        if locs["occurrences"] < max_location["occurrences"]:
            remove_obj.append(locs)
    
    for obj in remove_obj:
        locations.remove(obj)
     
    if max_location != None:
        locations.insert(0,max_location)

    if len(locations) > 0:
        dictionary[account] = {"name": info["info_name"], "locations": locations}
    
    

with open(cf_path, "w") as cf:
    js.dump(dictionary, cf)