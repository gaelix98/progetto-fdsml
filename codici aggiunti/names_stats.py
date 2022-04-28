import json as js, pandas, os, re
from matplotlib import pyplot as plt
from fuzzywuzzy import process

dataset_completo_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/dataset_completo.json"

f = open(dataset_completo_path, "r")
dataset = js.load(f)

df = pandas.read_csv("C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/nomi.csv")

nome_esatto = 0
nome_vuoto = 0

index_names = df[ df['Downloaded'] != 1 ].index
df.drop(index_names, inplace = True)

nomi = df.drop(columns = ["nome", "cognome", "Downloaded"])
only_names = nomi["nome completo"].tolist()

for account, info in dataset.items():
    if account == "dylanchristopher":
        continue
    
    if info["info_name"] == "":
        nome_vuoto += 1

    highest = process.extractOne(info["info_name"], only_names)  
    if highest != None and highest[1] >= 90:
        nome_esatto += 1

nome_non_completo = 107 - nome_esatto - nome_vuoto

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_autopct


labels = ["Esatti", "Non completi", "Vuoti"]
data = [nome_esatto, nome_non_completo, nome_vuoto]
myexplode = [0.4, 0.4, 0.4]
mycolors = ["#82C272", "#0087AC", "#00A88F"]

plt.pie(data, labels = labels, autopct=make_autopct(data), explode=myexplode, shadow=True, colors=mycolors, startangle=180)

plt.show()