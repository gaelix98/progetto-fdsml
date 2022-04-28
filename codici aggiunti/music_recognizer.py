import requests, os, base64, json
from moviepy.editor import *

log_file = open("log.txt","a+")


dataset_path = "C:\\Users\\Mark\\Marco\\Magistrale\\Anno I\\Secondo semestre\\DS & ML\\Progetto\\Social-Mapper-Extended\\social_mapper2\\dataset"
accounts = os.listdir(dataset_path)
mp3_files = []
i = 1
for account in accounts:
    if account == "log.txt":
        continue
    music_info = []
    account_path = dataset_path+"\\"+account
    files = os.listdir(account_path)
    if "music_info.json" in files:
        i+=1
        continue
    print("#",i," Analizzo: "+account)
    log_file.write("\n#"+str(i)+" Analizzo: "+account)
    json_file = open(account_path+"\\music_info.json", "w")
    for f in files:
        file_name, extension = f.split(".")
        if extension == "mp4":
            print("\tConverto l'mp4 in mp3 "+f)
            log_file.write("\n\tConverto l'mp4 in mp3 "+f)
           
            try:
                video = VideoFileClip(os.path.join(account_path, f))
                video.audio.write_audiofile(os.path.join(account_path, file_name+".mp3"))
            except AttributeError as e:
                print("\tQuesto video non contiene audio "+f)
                log_file.write("\n\tQuesto video non contiene audio "+f)
                continue
            except OSError as osErr:
                print("\tIl file è corrotto "+f)
                log_file.write("\n\tIl file è corrotto "+f)
                continue


           

            mp3_files.append(account_path+"\\"+file_name+".mp3")
            video = open(account_path+"\\"+file_name+".mp3", 'rb')

            data = {
                'accurate_offsets': 'true',
                'skip': '3',
                'every': '1',
                'api_token': '802d021d9d951a12237c73f8ba3aeb43'
            }
            
            print("\tRiconosco la musica...")
            log_file.write("\n\tRiconosco la musica...")
            result = requests.post('https://enterprise.audd.io/', data=data, files={"file":video}).json()
            if result["status"] == "success":
                if len(result["result"]) > 0:
                    print("\tCorrispondenze trovate!")
                    log_file.write("\n\tCorrispondenze trovate!")
                    music_info.append(result["result"])
                else:
                    print("\tNon sono riuscito a trovare nessuna corrispondenza per questo file")
                    log_file.write("\n\tNon sono riuscito a trovare nessuna corrispondenza per questo file")
    
    print("\tCorrispondenze trovate per per "+account+": "+str(len(music_info)))
    log_file.write("\n\tCorrispondenze trovate per "+account+": "+str(len(music_info)))
    log_file.flush()
    json.dump(music_info, json_file)
    i+=1
print("Tutti gli account sono stati analizzati!")
log_file.write("\nTutti gli account sono stati analizzati!")
log_file.flush()
log_file.close()