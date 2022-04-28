import json as js, pandas, os, re
from matplotlib import pyplot as plt

dataset_completo_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/dataset_completo.json"

f = open(dataset_completo_path, "r")
dataset = js.load(f)

phone_number_regex = r'(0|91)?[7-9][0-9]{10}'

phone_numbers = 0
ages = 0

for account, info in dataset.items():
    if account == "dylanchristopher":
        continue
    for occ in info["nlp_number"]:
        number = occ["number"]
        if len(number) > 0:
            try:
                if len(number) == 2:
                    number = int(number)
                    if 14<number<60:
                        ages += 1
                else:
                    if re.match(phone_number_regex, number):
                        phone_numbers += 1
            except:
                continue

fig, ax = plt.subplots()
fig.set_figheight(5)
fig.set_figwidth(10)
chiavi = ["età", "numero telefonico"]
valori = [ages, phone_numbers]
plt.barh(chiavi, valori)
ax.set_xticklabels(valori,fontsize=12)
ax.set_xticks(valori)
ax.set_yticklabels(chiavi,fontsize=18)
plt.show()