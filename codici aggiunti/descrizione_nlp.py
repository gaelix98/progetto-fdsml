from pycorenlp import StanfordCoreNLP
import os, json, sys, re

#os.chdir("C:/Program Files/stanford-corenlp-4.2.2")
#os.system("java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000")


nlp = StanfordCoreNLP('http://localhost:9000')
annotators = "ssplit,ner,depparse"
ner_keys = ["PERSON", "LOCATION", "ORGANIZATION", "NUMBER", "DATE", "EMAIL", 
            "URL", "CITY", "STATE_OR_PROVINCE", "COUNTRY", "NATIONALITY", 
            "RELIGION", "TITLE", "IDEOLOGY"]

info_keys = ["taggati", "testo", "location", "descrizione"]

reference_keys = ["basicDependencies","enhancedDependencies","enhancedPlusPlusDependencies"]

dataset_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/"

for account in os.listdir(dataset_path):
    if account == "dataset_completo.json":
        continue

    #if "didascalia_nlp.json" in os.listdir(dataset_path + account):
    #    continue

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
                        res = nlp.annotate(testo,
                            properties={
                                'annotators': annotators,
                                'outputFormat': 'json',
                                'timeout': 1000,
                            })
            

                        if isinstance(res,str):
                            continue
                        
                        nlp_res = dict()
                        nlp_res["entities"] = []
                        nlp_res["references"] = []

                        for sent in res["sentences"]:
                            check_references = []
                            for m in sent["entitymentions"]:
                                mention = m['text']
                                ner = m["ner"]
                                if "nerConfidences" in m.keys():
                                    ner_confidence = m['nerConfidences']
                                    if isinstance(ner_confidence, dict):
                                        if ner in ner_confidence.keys():
                                            ner_confidence = ner_confidence[ner]
                                else:
                                    ner_confidence = "None"

                                if ner in ner_keys:
                                    find = False
                                    for entity in nlp_res["entities"]:
                                        if ner in entity.keys():
                                            find = True
                                            entity[ner].append(mention)
                                            if ner in ["TITLE", "ORGANIZATION"]:
                                                check_references.append(mention)
                                            break
                                    
                                    if not find:
                                        nlp_res["entities"].append({ner:[]})
                                        find = False
                                        for entity in nlp_res["entities"]:
                                            if ner in entity.keys():
                                                find = True
                                                entity[ner].append(mention)
                                                if ner in ["TITLE", "ORGANIZATION"]:
                                                    check_references.append(mention)
                                                break
                            
                            for k in reference_keys:
                                for dependency in sent[k]:
                                    key = dependency["governorGloss"]
                                    if key in check_references:
                                        find = False
                                        for reference in nlp_res["references"]:
                                            if key in reference.keys():
                                                find = True
                                                item = dependency["dependentGloss"]
                                                if not item in reference[key]:
                                                    reference[key].append(item)
                                                break
                                        
                                        if not find:
                                            nlp_res["references"].append({key:[]})
                                            find = False
                                            for reference in nlp_res["references"]:
                                                if key in reference.keys():
                                                    find = True
                                                    item = dependency["dependentGloss"]
                                                    if not item in reference[key]:
                                                        reference[key].append(item)
                                                    break
                    if testo != "":
                        pic_metdata.update({"didascalia":{"testo":testo, "nlp":nlp_res}})
                elif info_k == "location" and info_pic["location"] != None:
                    pic_metdata.update({info_k:info_pic["location"]["name"]})

                elif info_k == "taggati" and info_pic["taggati"] != None:
                    taggati = []
                    for tag in info_pic["taggati"]:
                        if len(tag) > 0:
                            taggati.append({"full_name": tag["node"]["user"]["full_name"], "username": tag["node"]["user"]["username"]})
                    if len(taggati) > 0:
                        pic_metdata.update({info_k:taggati})
                
                elif info_k == "descrizione" and info_pic["descrizione"] != None:
                    pic_metdata.update({info_k:info_pic["descrizione"]})

        info_js["pictures"].append({"metadata":pic_metdata})

        
                                
    with open(dataset_path+account+"/didascalia_nlp.json", "w") as js:
        json.dump(info_js, js)