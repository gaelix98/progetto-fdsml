import pandas as pd
from instalooter.looters import PostLooter
import base64
import json
import os 
import tqdm

os.chdir("C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/")
cavia=open("log.txt","a+")
for user in os.listdir(): 
    if user == "log.txt":
        continue
    print(user)
    listone=[]
    if "info.json" in os.listdir(user):
        continue
    for media in os.listdir(user):
            if media in ["2616109190035207246.jpg","2631999076914088920.mp4"]:
                continue
            print(media)
            instagram_id=media.split(".")
            id_to_shortcode = lambda instagram_id: base64.b64encode(instagram_id.to_bytes(9, 'big'), b'-_').decode().replace('A', ' ').lstrip().replace(' ', 'A')
            codice=id_to_shortcode(int(instagram_id[0]))
            try:
                x=PostLooter(codice)
                if not x.logged_in():
                    x.login("allocca.gennaro", "Ilcanesimba2")
                post= x.get_post_info(codice)
            except:
                try:
                    x=PostLooter(codice)
                    if not x.logged_in():
                        x.login("allocca.gennaro", "Ilcanesimba2")
                    post= x.get_post_info(codice)
                except Exception as e:
                    print(e)
                    cavia.write("{} + {} \n".format(user,media))
                    cavia.flush()
                    continue
#post=json.dumps(post)
            utente=post["owner"]
            testo=post["edge_media_to_caption"]["edges"]
            
            try:
                utile={"descrizione":post["accessibility_caption"],"taggati":post["edge_media_to_tagged_user"]["edges"],"testo":testo,"location":post["location"],"musica":post["clips_music_attribution_info"],"nome":utente["full_name"]}
                listone.append(utile)
            except:
                try:
                    utile={"descrizione":post["accessibility_caption"],"taggati":post["edge_media_to_tagged_user"]["edges"],"testo":testo,"location":post["location"],"nome":utente["full_name"]}
                    listone.append(utile)
                except:
                    utile={"taggati":post["edge_media_to_tagged_user"]["edges"],"testo":testo,"location":post["location"],"nome":utente["full_name"]}
                    listone.append(utile)
    with open("{}/info.json".format(user),"w") as info:
        json.dump(listone,info)