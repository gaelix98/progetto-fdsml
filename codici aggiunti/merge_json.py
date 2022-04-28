import os, json, pandas

def open_file_and_check(path, name):
    f_json = open(path)
    try:
        js = json.load(f_json)
        return js
    except:
        print("problemi con: "+name)

    return None
    

nlp_keys = ["PERSON", "LOCATION", "ORGANIZATION", "NUMBER", "DATE", "EMAIL", 
            "URL", "CITY", "STATE_OR_PROVINCE", "COUNTRY", "NATIONALITY", 
            "RELIGION", "TITLE", "IDEOLOGY"]

dataset_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/"

i= 0
for account in os.listdir(dataset_path):
    if account == "dylanchristopher" or account == "dataset_completo.json":
        continue
    print("#"+str(i)+" "+account)
    info_json = open_file_and_check(dataset_path+account+"/info.json", "info")
    didascalia_nlp_json = open_file_and_check(dataset_path+account+"/didascalia_nlp.json", "didascalia_nlp")
    music_info_json = open_file_and_check(dataset_path+account+"/music_info.json", "music_info")
    nlp_json = open_file_and_check(dataset_path+account+"/nlp.json", "nlp")
    
    df = pandas.read_csv("interessi_cat.csv")

    general_json = dict()
    general_json["index"] = i
    i+=1
    general_json["username"] = account
    
    info_locations = []
    info_music = []

    if info_json != None and len(info_json) != 0:
        general_json["info_name"] = info_json[0]["nome"]
        for info in info_json:
            if info["location"] != None:
                found_info_location = False
                for location in info_locations:
                    if location["location"] == info["location"]["name"]:
                        location["occurrences"] += 1
                        found_info_location =True
                        break
                if not found_info_location:
                    info_locations.append({"location": info["location"]["name"], "occurrences": 1})
            if "music" in info.keys():
                if info["music"] != None:
                    artist = info["music"]["artist_name"]
                    song = info["music"]["song_name"]
                    fonud_info_music = False
                    for s in info_music:
                        if s["artist_name"] == artist and s["song_name"] == song:
                            s["occurrences"] += 1
                            fonud_info_music = True
                            break
                    if not fonud_info_music:
                        info_music.append({"artist_name": artist, "song_name": song, "occurrences": 1})
                        
    
    else:
        general_json["info_name"] = ""
    
    general_json["info_locations"] = info_locations
    general_json["music"] = info_music

    if music_info_json != None and music_info_json:
        if not isinstance(music_info_json, list):
            for song in music_info_json["songs"]:
                artist = song["artist"]
                song = song["title"]
                fonud_info_music = False
                for s in general_json["music"]:
                    if s["artist_name"] == artist and s["song_name"] == song:
                        s["occurrences"] += 1
                        fonud_info_music = True
                        break
                if not fonud_info_music:
                    general_json["music"].append({"artist_name": artist, "song_name": song, "occurrences": 1})
                    
    general_json["didascalia_location"] = []
    general_json["didascalia_hashtags"] = []
    
    for k in nlp_keys:
        if k == "PERSON":
            general_json["nlp_name"] = []
            general_json["didascalia_nlp_name"] = []
        if k == "TITLE":
            general_json["nlp_titles"] = []
            general_json["didascalia_nlp_titles"] = []
        else:
            general_json["nlp_"+k.lower()] = []
            general_json["didascalia_nlp_"+k.lower()] = []
        if nlp_json != None and nlp_json:
            if not isinstance(nlp_json,str): 
                for entity in nlp_json["entities"]:
                    if k in entity.keys():
                        if k == "PERSON":
                            nlp_name_count = dict()
                            for nlp_name in entity[k]:
                                if nlp_name in nlp_name_count.keys():
                                    nlp_name_count[nlp_name] += 1
                                else:
                                    nlp_name_count[nlp_name] = 1
                            for nlp_n in nlp_name_count.keys():
                                general_json["nlp_name"].append({"PERSON": nlp_n, "occurrences": nlp_name_count[nlp_n]})
                        elif k == "TITLE":
                            titles = entity[k]
                            official_titles = []
                            for title_entity in titles:
                                official_titles.append({"title": title_entity, "occurrences":1})
                            for title in titles:
                                for reference in nlp_json["references"]:
                                    if title in reference.keys():
                                        for t in reference[title]:
                                            found_t = False
                                            for off_t in official_titles:
                                                if t == off_t["title"]:
                                                    off_t["occurrences"] += 1
                                                    found_t = True
                                                    break
                                            if not found_t:
                                                official_titles.append({"title":t, "occurrences":1})
                            general_json["nlp_titles"] = official_titles

                        else:
                            supp_dict = dict()
                            for nlp_entity in entity[k]:
                                if nlp_entity in supp_dict.keys():
                                    supp_dict[nlp_entity] += 1
                                else:
                                    supp_dict[nlp_entity] = 1
                                    
                            for nlp_k in supp_dict.keys():
                                general_json["nlp_"+k.lower()].append({k.lower():nlp_k, "occurrences": supp_dict[nlp_k]})
       
        if didascalia_nlp_json != None and didascalia_nlp_json:
            for pic in didascalia_nlp_json["pictures"]:
                if "didascalia" in pic["metadata"].keys():
                    for didascalia_entity in pic["metadata"]["didascalia"]["nlp"]["entities"]:
                        if k in didascalia_entity.keys():
                            if k == "PERSON":
                                didascalia_name_count = dict()
                                for nlp_name in didascalia_entity[k]:
                                    if nlp_name in didascalia_name_count.keys():
                                        didascalia_name_count[nlp_name] += 1
                                    else:
                                        didascalia_name_count[nlp_name] = 1
                                for nlp_n in didascalia_name_count.keys():
                                    general_json["didascalia_nlp_name"].append({"PERSON": nlp_n, "occurrences": didascalia_name_count[nlp_n]})
                            elif k == "TITLE":
                                titles = didascalia_entity[k]
                                official_titles = []
                                for title in titles:
                                    official_titles.append({"title": title, "occurrences":1})
                                for title in titles:
                                    for reference in pic["metadata"]["didascalia"]["nlp"]["references"]:
                                        if title in reference.keys():
                                            for t in reference[title]:
                                                found_t = False
                                                for off_t in official_titles:
                                                    if t == off_t["title"]:
                                                        off_t["occurrences"] = off_t["occurrences"] + 1
                                                        found_t = True
                                                        break
                                                if not found_t:
                                                    official_titles.append({"title":t, "occurrences": 1})
                                    general_json["didascalia_nlp_titles"] = official_titles

                            else:
                                supp_dict = dict()
                                for didascalia_entity in didascalia_entity[k]:
                                    if didascalia_entity in supp_dict.keys():
                                        supp_dict[didascalia_entity] += 1
                                    else:
                                        supp_dict[didascalia_entity] = 1
                                        
                                for didascalia_k in supp_dict.keys():
                                    general_json["didascalia_nlp_"+k.lower()].append({k.lower():didascalia_k, "occurrences": supp_dict[didascalia_k]})

    if didascalia_nlp_json != None and didascalia_nlp_json:
        for pic in didascalia_nlp_json["pictures"]:
            if "didascalia_hashtags" in general_json.keys():
                 if "didascalia" in pic["metadata"].keys():
                    if "hastags" in pic["metadata"]["didascalia"].keys():
                        for hashtag in pic["metadata"]["didascalia"]["hashtags"]:
                            found_hastag = False
                            for hg in general_json["didascalia_hashtags"]:
                                if hg["hashtag"] == hashtag:
                                    found_hastag = True
                                    hg["occurrences"] += 1
                                    break
                            if not found_hastag:
                                general_json["didascalia_hashtags"].append({"hashtag": hashtag, "occurrences": 1})

            else:
                if "didascalia" in pic["metadata"].keys():
                    if "hastags" in pic["metadata"]["didascalia"].keys():
                        supp_dict = dict()
                        for hg_metadata in pic["metadata"]["didascalia"]["hashtags"]:
                            if hg_metadata in supp_dict.keys():
                                supp_dict[hg_metadata] += 1
                            else:
                                supp_dict[hg_metadata] = 1
                        for hashtag_k in supp_dict.keys():
                            general_json["didascalia_hashtags"].append({"hashtag": hashtag_k, "occurrences": supp_dict[hashtag_k]})

        if "location" in pic["metadata"].keys():
            found_didascalia_location = False
            for didascalia_location in general_json["didascalia_location"]:
                    if didascalia_location["location"] == pic["metadata"]["location"]:
                        didascalia_location["occurrences"] += 1
                        found_didascalia_location =True
                        break
            if not found_didascalia_location:
                general_json["didascalia_location"].append({"location": pic["metadata"]["location"], "occurrences": 1})
        
    general_json["interessi"] = df.loc[df["nome"] == account].drop(columns = ["nome"]).to_dict(orient = "records")[0]
    with open(dataset_path+account+"/general.json", "w") as general_js:
        json.dump(general_json, general_js)
