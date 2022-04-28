import os, json, re

dataset_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/"

for account in os.listdir(dataset_path):
    if account == "dataset_completo.json":
        continue

    #if "didascalia_nlp.json" in os.listdir(dataset_path + account):
    #    continue

    info_keys = ["taggati", "testo", "location", "descrizione"]

    print(account)
    js = open(dataset_path + account+ "/info.json")
    try:
        info_arr = json.load(js)
    except:
        continue

    info_js = dict()
    for info_pic in info_arr:
            info_js["pictures"] = []
            pic_metdata = dict()
            for info_k in info_keys:
                if info_k in info_pic.keys():
                    if info_k == "testo" and info_pic["testo"] != None:
                        testo = ""
                        if len(info_pic["testo"]) > 0:
                            testo = info_pic["testo"][0]["node"]["text"]
                            hashtag = re.findall(r"#(\w+)", testo)
                            print(hashtag)