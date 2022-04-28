import json as js, pandas, os, re
from matplotlib import pyplot as plt
from fuzzywuzzy import process

dataset_completo_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/dataset_completo.json"

f = open(dataset_completo_path, "r")
dataset = js.load(f)

location_in_didascalia_con_geo = 0
location_in_didascalia = 0
location_in_bio = 0

for account, info in dataset.items():
    if account == "dylanchristopher":
        continue
    print(account)
    
    if len(info["info_locations"]) > 0:
        location_in_didascalia_con_geo += 1
    if len(info["didascalia_nlp_location"]) > 0:
        location_in_didascalia += 1
    if len(info["nlp_location"]) > 0:
        location_in_bio += 1



def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_autopct

no_location = 107 - location_in_didascalia_con_geo - location_in_didascalia - location_in_bio

labels = ["Locations geolocalizzate", "Location in didascalia", "Nessuna location", "Location in bio",]
data = [location_in_didascalia_con_geo, location_in_didascalia, no_location, location_in_bio]
myexplode = [0.3, 0.3, 0.3, 0.3]
mycolors = ["#82C272", "#0087AC", "#00A88F", "#005FAA"]

plt.pie(data, labels = labels, autopct=make_autopct(data), explode=myexplode, shadow=True, colors=mycolors)

plt.show()