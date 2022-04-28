import os, json, pandas

dataset_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/"

complete_dataset = dict()
i = 0
for account in os.listdir(dataset_path):
    print("#"+str(i)+" "+account)
    i+=1
    if account == "dylanchristopher":
        complete_dataset[account] = dict()
        continue
    f_json = open(dataset_path+account+"/general.json")
    js = json.load(f_json)
    complete_dataset[account] = js

with open(dataset_path+"/dataset_completo.json", "w") as general_js:
    json.dump(complete_dataset, general_js)

