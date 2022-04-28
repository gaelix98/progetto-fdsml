import json as js
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import re, datetime

dataset_completo_path = "C:/Users/Mark/Marco/Magistrale/Anno I/Secondo semestre/DS & ML/Progetto/Social-Mapper-Extended/social_mapper2/dataset/dataset_completo.json"

f = open(dataset_completo_path, "r")
dataset = js.load(f)

regex_complete_date = r"(\b(0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](0?[1-9]|1[0-2])[^\w\d\r\n:](\d{4}|\d{2})\b)|(\b(0?[1-9]|1[0-2])[^\w\d\r\n:](0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](\d{4}|\d{2})\b)"
regex_year = r"^[0-9]{4}$"
regex_dd_month_yyyy = r'(\b\d{1,2}\D{0,3})\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\D?(\d{1,2}\D?)?\D?((19[7-9]\d|20\d{2})|\d{2})'
regex_month_yyyy = r"^(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\D?(\d{1,2}\D?)?\D?((19[7-9]\d|20\d{2})|\d{2})"

account_bio_did = 0
account_bio = 0
account_did = 0
account_no = 0

for account in dataset:
    if account == "dylanchristopher":
        continue

    found_in_bio = False
    for date in dataset[account]["nlp_date"]:
        if (
        re.search(regex_complete_date, date["date"]) or 
        re.search(regex_year, date["date"]) or 
        re.search(regex_dd_month_yyyy, date["date"]) or 
        re.search(regex_month_yyyy, date["date"])):
            found_in_bio = True
    
    found_in_did = False
    for date in dataset[account]["didascalia_nlp_date"]:
        if (
        re.search(regex_complete_date, date["date"]) or 
        re.search(regex_year, date["date"]) or 
        re.search(regex_dd_month_yyyy, date["date"]) or 
        re.search(regex_month_yyyy, date["date"])):
            found_in_did = True
    
    if found_in_bio and found_in_did:
        account_bio_did += 1
    elif found_in_bio:
        account_bio += 1
    elif found_in_did:
        account_did += 1
    else:
        account_no += 1

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_autopct


labels = ["Bio & didascalia", "Solo bio", "Solo didascalia", "Nessuna delle due"]
data = [account_bio_did, account_bio, account_did, account_no]
myexplode = [0.4, 0.4, 0.4, 0.4]
mycolors = ["#82C272", "#0087AC", "#00A88F", "#005FAA", "#323B81"]
fig, ax = plt.subplots()
ax.set_yticklabels(labels,fontsize=1)
_, _, autotexts = plt.pie(data, labels = labels, autopct=make_autopct(data), shadow=True, explode=myexplode, colors=mycolors, textprops={"fontsize":15})
for autotext in autotexts:
    autotext.set_color('black')

plt.show()
    

