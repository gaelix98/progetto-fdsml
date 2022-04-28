from instalooter.looters import PostLooter
import os, json, base64, string

s = "TαmαrαAguadulce\ud83d\udccd"
print(output)
test = bytes(s,"unicode-escape").decode("unicode-escape")
print("\U0001f600")
complete_str = ""
for char in test:
    try:
        utf_char = char.encode("utf-8").decode("utf-8")
        complete_str += utf_char
    except:
        continue

'''
chosen_keys = ["edge_media_to_tagged_user", "edge_media_to_caption", "location", "clips_music_attribution_info"]

json_file = open("CR1iig3osTL.json")
data = json.load(json_file)
values = [data[k] for k in chosen_keys]
print(values)
'''
'''
path = ""

for account in os.listdir(path):
    for media in os.listdir(account):
        el = media.split(".")[0]

id_to_shortcode = lambda instagram_id: base64.b64encode(instagram_id.to_bytes(9, 'big'), b'-_').decode().replace('A', ' ').lstrip().replace(' ', 'A')
shortcode = id_to_shortcode(2176505611263720358)
print(shortcode)


looter = PostLooter(shortcode)
#looter.login("allocca.gennaro", "Ilcanesimba2")
diction = looter.get_post_info(shortcode)
with open(path+'/'+account+'info.json', 'w') as fp:
    json.dump(diction, fp)

f = open("account.txt", "a+")
dirs = os.listdir("C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset")
os.chdir("C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset")
for d in dirs:
    if d == "log.txt":
        continue
    if "info.json" in os.listdir(d):
        f.write(d+"\n")

dirs = os.listdir("C:/Users/MARCUS/Desktop/Social-Mapper-Extended/social_mapper2/dataset")
for account_name in dirs:
    print("Download di "+account_name)
    try:
        looter = ProfileLooter(account_name)
        looter.login("allocca.gennaro", "Ilcanesimba2")
        diction = looter.get_post_info("CSFFyh6MNie")
        print(diction)
        #looter.download_pictures("./dataset/"+account_name, media_count=10)
        #looter.download_videos("./dataset/"+account_name, media_count=5)
        print("Done..")
    except:
        continue
'''