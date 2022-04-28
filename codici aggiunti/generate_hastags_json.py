import os, json, re

dataset_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/"


hashtags_dict = dict()

for account in os.listdir(dataset_path):
    if account == "dataset_completo.json":
        continue

    #if "didascalia_nlp.json" in os.listdir(dataset_path + account):
    #    continue

    info_keys = ["taggati", "testo", "location", "descrizione"]

    print(account)
    js_info = open(dataset_path + account+ "/info.json")
    try:
        info_arr = json.load(js_info)
    except:
        continue
    
    eliminated = 0
    hashtags_dict[account] = []
    len_info_arr = len(info_arr)
    da_eliminare = []
    for i in range(len_info_arr):
        if i in da_eliminare:
            continue
        testo_i = ""
        for node_i in info_arr[i]["testo"]:
            testo_i += node_i["node"]["text"]
        for j in range(len_info_arr):
            if i == j: continue
            testo_j = ""
            for node_j in info_arr[j]["testo"]:
                testo_j += node_j["node"]["text"]
            if testo_i == testo_j:
                if len(testo_i) > 0 and len(testo_j) > 0:
                    if not j in da_eliminare:
                        da_eliminare.append(j)
                        eliminated += 1
        
        hashtag = re.findall(r"#(\w+)", testo_i)
        hashtags_dict[account].extend(hashtag)

with open(dataset_path+ "/hashtags.json", "w") as js_hashtags:
    json.dump(hashtags_dict, js_hashtags)
        
        