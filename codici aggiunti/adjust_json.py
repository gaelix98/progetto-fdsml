import json, os

dataset_path = "C:\\Users\\Mark\\Marco\\Magistrale\\Anno I\\Secondo semestre\\DS & ML\\Progetto\\Social-Mapper-Extended\\social_mapper2\\dataset\\"

for account in os.listdir(dataset_path):
    if account == "log.txt":
        continue
    songs = {"songs" : []}
    print(account)
    with open(dataset_path + account + "\\music_info.json") as f:
        try:
            data = json.load(f)
            if len(data) > 0:
                for d in data[0]:
                    for song in d["songs"]:
                        songs["songs"].append(song)
            else:
                continue
        except:
            continue
    f.close()
    os.remove(dataset_path + account + "\\music_info.json")
    with open(dataset_path + account + "\\music_info.json", "w") as js:
        json.dump(songs, js)