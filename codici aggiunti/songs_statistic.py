import json as js, pandas, os
from matplotlib import pyplot as plt
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

dataset_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/"

dataset_completo_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/dataset_completo.json"

f = open(dataset_completo_path, "r")
dataset = js.load(f)

songs = dict()

for account, info in dataset.items():
    if account == "dylanchristopher":
        continue
    for song in info["music"]:
        song_name = song["song_name"]
        was_added = False
        highest = process.extractOne(song_name.lower(),songs.keys())   
        if highest != None and highest[1] >= 90:
            songs[highest[0]] += 1
            was_added = True
        if not was_added:
            if song_name in songs:
                songs[song_name] += 1
            else:
                songs[song_name] = 1

print(songs)


key_to_del = []
for key in songs.keys():
    if songs[key] < 2:
        key_to_del.append(key)

for k in key_to_del:
    del songs[k]

song_names = list(songs.keys())
song_values = list(songs.values())

fig, ax = plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(15)
plt.barh(song_names, song_values)
ax.set_xticklabels(song_values,fontsize=12)
ax.set_xticks(song_values)
ax.set_yticklabels(song_names,fontsize=12.8)
plt.show()