from pycorenlp import StanfordCoreNLP
import os, json, sys

#os.chdir("C:/Program Files/stanford-corenlp-4.2.2")
#os.system("java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000")


nlp = StanfordCoreNLP('http://localhost:9000')
annotators = "ssplit,ner,depparse"
ner_keys = ["PERSON", "LOCATION", "ORGANIZATION", "NUMBER", "DATE", "EMAIL", 
            "URL", "CITY", "STATE_OR_PROVINCE", "COUNTRY", "NATIONALITY", 
            "RELIGION", "TITLE", "IDEOLOGY"]

reference_keys = ["basicDependencies","enhancedDependencies","enhancedPlusPlusDependencies"]

dataset_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/"

for account in os.listdir(dataset_path):
    if account == "log.txt":
        continue

    #if "nlp.json" in os.listdir(dataset_path + account):
    #    continue

    print(account)
    js = open(dataset_path + account+ "/bio.json")
    sentence = json.load(js)
    print(sentence)

    res = nlp.annotate(sentence,
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
                            
    with open(dataset_path+account+"/nlp.json", "w") as js:
        json.dump(nlp_res, js)