import json as js, pandas, os
from matplotlib import pyplot as plt
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

dataset_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/"

dataset_completo_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/dataset_completo.json"

f = open(dataset_completo_path, "r")
dataset = js.load(f)

user_with_music = 0

for account, info in dataset.items():
    if account == "dylanchristopher":
        continue
    if len(info["music"]) > 0:
        user_with_music += 1

keys = ["Info sulla musica", "Nessuna info sulla musica"]
values = [user_with_music, 107-user_with_music]

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_autopct

myexplode = [0.4, 0.4]
mycolors = ["#82C272", "#0087AC"]
fig, ax = plt.subplots()
ax.set_xticklabels(keys,fontsize=8)
plt.pie(values, labels = keys, autopct=make_autopct(values), explode=myexplode, shadow=True, colors=mycolors)

plt.show()