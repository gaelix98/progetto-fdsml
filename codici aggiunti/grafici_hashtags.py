import json as js
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import re, datetime

dataset_completo_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/dataset_completo.json"

f = open(dataset_completo_path, "r")
dataset = js.load(f)

hasthags = dict()
for account in dataset:
    if account == "dylanchristopher":
        continue
    for hashtag in dataset[account]["didascalia_hashtags"]:
        if hashtag in hasthags.keys():
            hasthags[hashtag] += 1
        else:
            hasthags[hashtag] = 1

key_to_del = []
for key in hasthags.keys():
    if hasthags[key] < 13:
        key_to_del.append(key)

for k in key_to_del:
    del hasthags[k]

lables = list(hasthags.keys())
values = list(hasthags.values())

fig, ax = plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(15)
plt.barh(lables, values)
ax.set_xticklabels(values,fontsize=12)
ax.set_xticks(values)
ax.set_yticklabels(lables,fontsize=18)

for bar in fig.patches:
    bar.set_linewidth(0.2)
    bar.set_edgecolor(bar.get_facecolor())
plt.show()

print(len(hasthags))