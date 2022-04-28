import json as js
dataset_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/"

js_hash = open(dataset_path + "/hashtags.json")
js_dataset = open(dataset_path + "/dataset_completo.json")

try:
    hash_arr = js.load(js_hash)
    dataset_arr = js.load(js_dataset)
except:
    pass

for key in hash_arr.keys():
    dataset_arr[key]["didascalia_hashtags"].extend(hash_arr[key])

with open(dataset_path + "/dataset_completo2.json", "w") as dat:
    js.dump(dataset_arr,dat)