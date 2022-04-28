import json as js, pandas, os
from matplotlib import pyplot as plt
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

dataset_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/"

dataset_completo_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/dataset_completo.json"

f = open(dataset_completo_path, "r")
dataset = js.load(f)

artists = dict()

for account, info in dataset.items():
    if account == "dylanchristopher":
        continue
    for song in info["music"]:
        artist_name = song["artist_name"]
        was_added = False
        highest = process.extractOne(artist_name.lower(),artists.keys())   
        if highest != None and highest[1] >= 90:
            artists[highest[0]] += 1
            was_added = True
        if not was_added:
            if artist_name in artists:
                artists[artist_name] += 1
            else:
                artists[artist_name] = 1

print(artists)


key_to_del = []
for key in artists.keys():
    if artists[key] < 2:
        key_to_del.append(key)

for k in key_to_del:
    del artists[k]


song_names = list(artists.keys())
song_values = list(artists.values())

fig, ax = plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(15)
plt.barh(song_names, song_values)
ax.set_xticklabels(song_values,fontsize=10)
ax.set_xticks(song_values)
ax.set_yticklabels(song_names,fontsize=13)
plt.show()