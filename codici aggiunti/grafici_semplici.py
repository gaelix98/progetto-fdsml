import json as js
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

keys = {
    #"info_name": 0,
    #"info_locations": 0,
    #"music": 0,
    #"didascalia_location": 0,
    #"didascalia_hashtags": 0,
    #"nlp_name": 0,
    #"didascalia_nlp_name": 0,
    #"nlp_location": 0,
    #"didascalia_nlp_location": 0,
    "nlp_organization": 0,
    "didascalia_nlp_organization": 0,
    #"nlp_number": 0,
    #"didascalia_nlp_number": 0,
    #"nlp_date": 0,
    #"didascalia_nlp_date": 0,
    "nlp_email": 0,
    "didascalia_nlp_email": 0,
    "nlp_url": 0,
    "didascalia_nlp_url": 0,
    "nlp_city": 0,
    "didascalia_nlp_city": 0,
    "nlp_state_or_province": 0,
    "didascalia_nlp_state_or_province": 0,
    "nlp_country": 0,
    "didascalia_nlp_country": 0,
    "nlp_nationality": 0,
    "didascalia_nlp_nationality": 0,
    "nlp_religion": 0,
    "didascalia_nlp_religion": 0,
    "nlp_titles": 0,
    "didascalia_nlp_titles": 0,
    "nlp_ideology": 0,
    "didascalia_nlp_ideology": 0
}

dataset_completo_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/dataset_completo.json"

f = open(dataset_completo_path, "r")
dataset = js.load(f)

for account in dataset.keys():
    for key in keys.keys():
        if key in dataset[account].keys():
            if len(dataset[account][key]) > 0:
                keys[key] += 1


whole_bio_keys = [key for key in keys.keys() if not "didascalia" in key]
whole_bio_values = []

i=0
for k in whole_bio_keys:
    whole_bio_values.append(keys[k])
    whole_bio_keys.remove(k)
    k = k.rsplit("_", 1)[1]
    whole_bio_keys.insert(i, k)
    i+=1

whole_did_keys = [key for key in keys.keys() if "didascalia" in key]
whole_did_values = []

j=0
for k in whole_did_keys:
    whole_did_values.append(keys[k])
    whole_did_keys.remove(k)
    k = k.rsplit("_", 1)[1]
    whole_did_keys.insert(j, k)
    j+=1

fig, ax = plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(15)
plt.barh(whole_bio_keys, whole_bio_values)
plt.title('Attribute frequency in biography')
ax.set_xticklabels(whole_bio_values,fontsize=12)
ax.set_xticks(whole_bio_values)
ax.set_yticklabels(whole_bio_keys,fontsize=18)
plt.show()

fig, ax = plt.subplots()
fig.set_figheight(10)
fig.set_figwidth(15)
plt.barh(whole_did_keys, whole_did_values)
plt.title('Attribute frequency in photo description')
ax.set_xticklabels(whole_did_values,fontsize=12)
ax.set_xticks(whole_did_values)
ax.set_yticklabels(whole_did_keys,fontsize=18)
plt.show()