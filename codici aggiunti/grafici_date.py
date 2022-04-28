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

date_bio_esatte = 0
date_bio_inesatte = 0
date_bio_inutilizzabili = 0

date_did_esatte = 0
date_did_inesatte = 0
date_did_inutilizzabili = 0

for account in dataset:
    if account == "dylanchristopher":
        continue
    if len(dataset[account]["nlp_date"]) > 0:
        for date in dataset[account]["nlp_date"]:
            if re.search(regex_complete_date, date["date"]):
                print(date["date"])
                date_bio_esatte += 1
            elif re.search(regex_year, date["date"]):
                date_bio_inesatte += 1
            elif re.search(regex_dd_month_yyyy, date["date"]):
                date_bio_esatte += 1
            elif re.search(regex_month_yyyy, date["date"]):
                date_bio_inesatte += 1
            else:
                date_bio_inutilizzabili += 1
    if len(dataset[account]["didascalia_nlp_date"]) > 0:
        for date in dataset[account]["didascalia_nlp_date"]:
            if re.search(regex_complete_date, date["date"]):
                date_did_esatte += 1
            elif re.search(regex_year, date["date"]):
                date_did_inesatte += 1
            elif re.search(regex_dd_month_yyyy, date["date"]):
                date_did_esatte += 1
            elif re.search(regex_month_yyyy, date["date"]):
                date_did_inesatte += 1
            else:
                date_did_inutilizzabili += 1

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_autopct


labels = ["Esatte", "Generiche", "Non utilizzabili"]
data = [date_bio_esatte, date_bio_inesatte, date_bio_inutilizzabili]
myexplode = [0.4, 0.4, 0.4]
mycolors = ["#82C272", "#0087AC", "#00A88F"]
fig, ax = plt.subplots()
ax.set_xticklabels(labels,fontsize=8)
plt.pie(data, labels = labels, autopct=make_autopct(data), explode=myexplode, shadow=True, colors=mycolors)

plt.show()