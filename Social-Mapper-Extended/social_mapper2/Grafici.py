import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Codice per la creazione dei grafici sulle statitiche dei dati raccolti sui singoli social network
# Estrazione delle informazioni dal dataset in formato csv
data = pd.read_csv("definitivo.csv", sep=";")
#stampa delle feature con il relativo tipo e numero di valori not-null per ognuna
print("Info features dataset")
data.info()
print("-------------------------------------------------------------------------------------------------------")

# estrazione info feature linkedin e creazione pieplot
# Nomi feature dataset originali
# linkedin = data[["Cellulare","Sito Web","Email","Compleanno","Città","Impiego"]]
linkedin = data.iloc[:, 2:8]
print("Info features Linkedin")
# linkedin.info()
statistiche_linkedin = linkedin.count()
stat_linkedin = np.array(
    [statistiche_linkedin[0], statistiche_linkedin[1], statistiche_linkedin[2], statistiche_linkedin[3],
     statistiche_linkedin[4], statistiche_linkedin[5]])
label_linkedin = ["Cellulare", "Sito Web", "Email", "Compleanno", "Città", "Impiego"]
plt.pie(stat_linkedin, labels=label_linkedin, counterclock=True, shadow=True, autopct='%1.1f%%')
plt.title("Analisi informazioni Linkedin")
plt.show()
print("-------------------------------------------------------------------------------------------------------")

# estrazione info feature facebook e creazione pieplot
# Nomi feature dataset originali
# facebook = data["Work_and_Education","Placed_Lives","Contact","Basic_Info","Detail_about"]
facebook = data.iloc[:, 9:15]
print("Info features Facebook")
# facebook.info()
statistiche_facebook = facebook.count()
stat_facebook = np.array(
    [statistiche_facebook[0], statistiche_facebook[1], statistiche_facebook[2],statistiche_facebook[3],
     statistiche_facebook[4], statistiche_facebook[5]])
label_facebook = ["Work_and_Education", "Placed_Lives", "Contact", "Basic_Info_Birthday", "Basic_Info_Gender", "Detail_about"]
plt.pie(stat_facebook, labels=label_facebook, counterclock=True, shadow=True, autopct='%1.1f%%')
plt.title("Analisi informazioni Facebook")
plt.show()
print("-------------------------------------------------------------------------------------------------------")

# estrazione info feature twitter e creazione pieplot
# Nomi feature dataset originali
# twitter = data["Sito_Twitter","Città_Twitter","Twitter_Biografia"]
twitter = data.iloc[:, 16:19]
print("Info features Twitter")
# twitter.info()
statistiche_twitter = twitter.count()
stat_twitter = np.array([statistiche_twitter[0], statistiche_twitter[1], statistiche_twitter[2]])
label_twitter = ["SitoWeb", "Città", "Biografia"]
plt.pie(stat_twitter, labels=label_twitter, counterclock=True, shadow=True, autopct='%1.1f%%')
plt.title("Analisi informazioni Twitter")
plt.show()
print("-------------------------------------------------------------------------------------------------------")

# instagram = data["Biografi_Instagram"] #instagram possiede solo una feature

# estrazione info feature vkontakte e creazione pieplot
# Nomi feature dataset originali
# vkontakte = data["Data_di_Nascita","Città_1","Studiato_a","Luogo_di_Nascita","Lingue","Cellulare_2","Telefono","Skype","College_o_università","Stato","Scuola","Gruppi","Azienda","Interesse"]
vkontakte = data.iloc[:, 23:37]
print("Info features VKontakte")
# vkontakte.info()
statistiche_vkontakte = vkontakte.count()
stat_vkontakte = np.array(
    [statistiche_vkontakte[0], statistiche_vkontakte[1], statistiche_vkontakte[9], statistiche_vkontakte[2],
     statistiche_vkontakte[3], statistiche_vkontakte[5], statistiche_vkontakte[4], statistiche_vkontakte[7],
     statistiche_vkontakte[8], statistiche_vkontakte[10], statistiche_vkontakte[6], statistiche_vkontakte[11],
     statistiche_vkontakte[12], statistiche_vkontakte[13]])
label_vkontakte = ["Compleanno", "Città", "Stato", "Studiato a", "Luogo di Nascita", "Cellulare", "Lingue", "Skype",
                   "Col/Uni", "Scuola", "Telefono", "Gruppi", "Azienda", "Interesse"]
plt.pie(stat_vkontakte, labels=label_vkontakte, counterclock=True, autopct='%1.1f%%', rotatelabels=True)
plt.title("Analisi informazioni VKontakte")
plt.show()

# STATISTICHE CROSS SOCIAL

# GRAFICO VALORI ATTRIBUTI DI TUTTO IL DATASET
statistiche_dati = data.count()
stat_data = np.array(
    [statistiche_dati[21], statistiche_dati[2], statistiche_dati[3], statistiche_dati[4], statistiche_dati[5],
     statistiche_dati[6], statistiche_dati[7], statistiche_dati[9], statistiche_dati[10], statistiche_dati[11],
     statistiche_dati[12], statistiche_dati[13], statistiche_dati[14], statistiche_dati[15], statistiche_dati[17],
     statistiche_dati[18], statistiche_dati[23], statistiche_dati[24], statistiche_dati[25], statistiche_dati[26],
     statistiche_dati[27], statistiche_dati[28], statistiche_dati[29], statistiche_dati[30], statistiche_dati[31],
     statistiche_dati[32], statistiche_dati[33], statistiche_dati[34], statistiche_dati[35], statistiche_dati[36]])
label_data = ["Biografia_ig", "Cellulare", "Sito_Web_li", "Email", "Compleanno_li", "Città_li", "Impiego",
              "WorkandEducation", "Placed_Lives", "Contact", "Basic_Info_Birthday", "Basic_Info_Gender", "Detail_about",
              "SitoWeb_tw", "Città_tw","Biografia_tw", "Compleanno_vk", "Città_vk", "Stato", "Studiato a",
              "Luogo di Nascita", "Cellulare_vk", "Lingue", "Skype", "Col/Uni", "Scuola_vk", "Telefono_vk", "Gruppi",
              "Azienda", "Interesse"]
x_pos = np.arange(len(label_data))
plt.barh(x_pos, stat_data, align='center',
         color=['red', 'cyan', 'cyan', 'cyan', 'cyan', 'cyan', 'cyan', 'blue', 'blue', 'blue', 'blue', 'blue', 'green',
                'green', 'green', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange',
                'orange', 'orange', 'orange', 'orange', 'orange', 'orange'])
plt.yticks(x_pos, label_data)
plt.ylabel('Attributi', fontsize=10)
colors = {'Linkedin': 'cyan', 'Facebook': 'blue', 'Instagram': 'red', "Twitter": "green", "VKontakte": "orange"}
labels = list(colors.keys())
handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
plt.legend(handles, labels)
plt.xlabel('Valori', fontsize=10)
plt.title('Analisi sugli attributi significativi di tutto il dataset')
plt.show()

# GRAFICO TOP FIVE ATTRIBUTI DATASET
statistiche_dati = data.count()
topfive_data = np.array(
    [statistiche_dati[7], statistiche_dati[6], statistiche_dati[21], statistiche_dati[13], statistiche_dati[3]])
label_topfive = ["Impiego", "Città", "Biografia", "Basic_Info", "Sito Web"]
x_pos = np.arange(len(label_topfive))
plt.rcParams['figure.figsize'] = (10, 6)
plt.bar(x_pos, topfive_data, color=['cyan', 'cyan', 'red', 'blue', 'cyan'])
plt.xticks(x_pos, label_topfive, rotation=90)
plt.ylabel('Valori', fontsize=10)
colors = {'Linkedin': 'cyan', 'Facebook': 'blue', 'Instagram': 'red'}
labels = list(colors.keys())
handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
plt.legend(handles, labels)
plt.xlabel('Attributi', fontsize=10)
plt.title('Top five attributi cross social')
plt.show()

# GRAFICO CROSS-SOCIAL EMAIL
fig = plt.figure()
ax2 = fig.add_subplot(121)
ax1 = fig.add_subplot(122)
statistiche_dati = data.count()
email_data = np.array([statistiche_dati[4], statistiche_dati[11], statistiche_dati[30]])
label_email = ["Email_Linkedin", "Email_Facebook", "Email_VKontakte"]
x_pos = np.arange(len(label_email))
plt.rcParams['figure.figsize'] = (10, 6)
ax1.bar(x_pos, email_data, color=['cyan', 'blue', 'orange'])
plt.xticks(x_pos, label_email, rotation=90)
plt.ylabel('Valori', fontsize=10)
colors = {'Linkedin': 'cyan', 'Facebook': 'blue', 'VKontakte': 'orange'}
labels = list(colors.keys())
handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
plt.legend(handles, labels)
plt.xlabel('Attributi', fontsize=10)
ax2.pie(email_data, labels=label_email, counterclock=True, autopct='%1.1f%%', colors=['cyan', 'blue', 'orange'])
plt.title("Analisi cross-social: email")
plt.show()

# GRAFICO CROSS-SOCIAL DATA DI NASCITA
fig = plt.figure()
ax2 = fig.add_subplot(121)
ax1 = fig.add_subplot(122)
statistiche_dati = data.count()
nascita_data = np.array([statistiche_dati[5], statistiche_dati[12], statistiche_dati[23]])
label_nascita = ["DataNascita_Linkedin", "DataNascita_Facebook", "DataNascita_VKontakte"]
x_pos = np.arange(len(label_nascita))
plt.rcParams['figure.figsize'] = (10, 6)
ax1.bar(x_pos, nascita_data, color=['cyan', 'blue', 'orange'])
plt.xticks(x_pos, label_nascita, rotation=90)
plt.ylabel('Valori', fontsize=10)
colors = {'Linkedin': 'cyan', 'Facebook': 'blue', 'VKontakte': 'orange'}
labels = list(colors.keys())
handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
plt.legend(handles, labels)
plt.xlabel('Attributi', fontsize=10)

ax2.pie(nascita_data, labels=label_nascita, counterclock=True, autopct='%1.1f%%', colors=['cyan', 'blue', 'orange'])
plt.title("Analisi cross social: data di nascita")
plt.show()

# GRAFICO CROSS-SOCIAL NUMERO TELEFONICO
fig = plt.figure()
ax2 = fig.add_subplot(121)
ax1 = fig.add_subplot(122)
statistiche_dati = data.count()
nascita_data = np.array([statistiche_dati[2], statistiche_dati[11], statistiche_dati[28], statistiche_dati[29]])
label_nascita = ["Tel_Linkedin", "Tel_Facebook", "Cell__VKontakte", "Tel_VKontakte"]
x_pos = np.arange(len(label_nascita))
plt.rcParams['figure.figsize'] = (10, 6)
ax1.bar(x_pos, nascita_data, color=['cyan', 'blue', 'orange', 'orange'])
plt.xticks(x_pos, label_nascita, rotation=90)
plt.ylabel('Valori', fontsize=10)
colors = {'Linkedin': 'cyan', 'Facebook': 'blue', 'VKontakte': 'orange'}
labels = list(colors.keys())
handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
plt.legend(handles, labels)
plt.xlabel('Attributi', fontsize=10)
ax2.pie(nascita_data, labels=label_nascita, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: numeri di telefono")
plt.show()

# GRAFICO CROSS-SOCIAL CITTA'
fig = plt.figure()
ax2 = fig.add_subplot(121)
ax1 = fig.add_subplot(122)
statistiche_dati = data.count()
nascita_data = np.array([statistiche_dati[6],statistiche_dati[10], statistiche_dati[17], statistiche_dati[24], statistiche_dati[26]])
label_nascita = ["Città_Ln", "Placed_Lives_Fb", "Città_Tw", "Città__VK", "Luogo_di_Nascita_VK"]
x_pos = np.arange(len(label_nascita))
plt.rcParams['figure.figsize'] = (10, 6)
ax1.bar(x_pos, nascita_data, color=['cyan', 'blue', 'green', 'orange','orange'])
plt.xticks(x_pos, label_nascita, rotation=90)
plt.ylabel('Valori', fontsize=10)
colors = {'Linkedin': 'cyan', 'Facebook': 'blue', 'Twitter': 'green','VKontakte': 'orange'}
labels = list(colors.keys())
handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
plt.legend(handles, labels)
plt.xlabel('Attributi', fontsize=10)
ax2.pie(nascita_data, labels=label_nascita, counterclock=True, autopct='%1.1f%%', colors=['cyan', 'blue', 'green', 'orange','tomato'])
plt.title("Analisi cross social: città")
plt.show()

# GRAFICO CROSS-SOCIAL FORMAZIONE O LAVORO
fig = plt.figure()
ax2 = fig.add_subplot(121)
ax1 = fig.add_subplot(122)
statistiche_dati = data.count()
nascita_data = np.array([statistiche_dati[7], statistiche_dati[9],statistiche_dati[25], statistiche_dati[31], statistiche_dati[33], statistiche_dati[35]])
label_nascita = ["Impiego_Ln", "Work/Edu_Fb", "Studiato_VK","Coll/Uni_VK","Scuola_VK", "Azienda_VK"]
x_pos = np.arange(len(label_nascita))
plt.rcParams['figure.figsize'] = (10, 6)
plt.xticks(x_pos, label_nascita, rotation=90)
plt.ylabel('Valori', fontsize=10)
plt.title("Analisi cross social: scuola e lavoro")
ax1.bar(x_pos, nascita_data, color=['cyan', 'blue', 'orange', 'orange','orange','orange'])

colors = {'Linkedin': 'cyan', 'Facebook': 'blue', 'VKontakte': 'orange'}
labels = list(colors.keys())
handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label]) for label in labels]
ax1.legend(handles, labels,loc='upper right')
plt.xlabel('Attributi', fontsize=10)
plt.title("Analisi cross social: scuola e lavoro")
ax2.pie(nascita_data, labels=label_nascita, counterclock=True, autopct='%1.1f%%',colors=['cyan', 'blue', 'orange', 'tomato','orangered','lightcoral'])
#ax2.title("Analisi informazioni nascita")
plt.show()

data = data.fillna(0)
# data di nascita per ricostruzione codice fiscale
list = pd.DataFrame(columns=['0', '1', '2', '3', '4', '5', '6', '7'])

statistiche_dati = np.array(data)
for item in statistiche_dati:
    i = 0
    if item[5] != 0:
        i = 1
    if item[12] != 0:
        if i != 0:
            i = i + 3
        else:
            i = i + 2
    if item[23] != 0:
        if i == 1 or i == 2:
            i = i + 4
        else:
            i = i + 3
    list = list.append({str(i): i}, ignore_index=True)

cross_data = list.count()
label_data = ["Nessuno", "Linkedin", "Facebook", "VKontakte", "F&L", "V&L", "V&F", "Tutti"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: data di nascita per ricostruzione codice fiscale")
plt.show()

# analisi dati sensibili: cellulare
list = pd.DataFrame(columns=['0', '1', '2', '3', '4', '5', '6', '7'])
statistiche_dati = np.array(data)
for item in statistiche_dati:
    i = 0
    if item[2] != 0:
        i = 1
    if item[11] != 0:
        if i != 0:
            i = i + 3
        else:
            i = i + 2
    if item[28] != 0 or item[29] != 0:
        if i == 1 or i == 2:
            i = i + 4
        else:
            i = i + 3
    list = list.append({str(i): i}, ignore_index=True)

cross_data = list.count()
label_data = ["Nessuno", "Linkedin", "Facebook", "VKontakte", "F&L", "V&L", "V&F", "Tutti"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi dati sensibili cross-social: cellulare")
plt.show()

# città natale per ricostruzione codice fiscale
list = pd.DataFrame(columns=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'])
bool = False
statistiche_dati = np.array(data)
for item in statistiche_dati:
    i = 0
    if item[6] != 0:
        i = 1
    if item[10] != 0:
        if i != 0:
            i = i + 3
        else:
            i = i + 2
    if item[17] != 0:
        if i == 1 or i == 2:
            i = i + 4
        else:
            bool = True
            i = i + 3
    if item[24] != 0 or item[26] != 0:
        if i == 3 and bool:
            bool = False
            i = i + 9
        else:
            i = i + 8
    list = list.append({str(i): i}, ignore_index=True)

cross_data = list.count()
app= np.array([cross_data[0],cross_data[6], cross_data[5],cross_data[1],cross_data[10],cross_data[14],cross_data[3],cross_data[13],cross_data[4], cross_data[2],cross_data[7],cross_data[8],cross_data[9],cross_data[11],cross_data[12],cross_data[15]])
label_data = ["Nessuno", "V&F", "V&L", "Linkedin", "T&F",  "T&V&F", "VKontakte", "T&V&L", "F&L", "Facebook", "V&F&L", "Twitter", "T&L", " T&V", "T&F&L", "Tutti"]
plt.pie(app, labels=label_data, counterclock=True)
plt.title("Analisi cross social: città natale per ricostruzione codice fiscale")
plt.show()

list = pd.DataFrame(columns=['no', 'si'])

statistiche_dati = np.array(data)
for item in statistiche_dati:
    i = 0
    if item[5] != 0 or item[12] != 0 or item[23] != 0:
        i = i + 1
    if item[6] != 0 or item[10] != 0 or item[17] != 0 or item[24] != 0 or item[26] != 0:
        i = i + 1
    if i == 2:
        list = list.append({'si': 1}, ignore_index=True)
    else:
        list = list.append({'no': 1}, ignore_index=True)

cross_data = list.count()
label_data = ["Non ricostruibile", "Ricostruibile"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: ricostruzione codice fiscale")
plt.show()

##########################################################################################

# formazione o lavoro, bloccando linkedin
statistiche_dati = np.array(data.query('Impiego == 0'))
list = pd.DataFrame(columns=['Facebook', 'Nessuno', 'VKontakte'])

for item in statistiche_dati:
    i = 0
    if item[9] != 0:
        i = 1
        list = list.append({'Facebook': 1}, ignore_index=True)
    if item[32] != 0 or item[35] != 0:
        i = 1
        list = list.append({'VKontakte': 1}, ignore_index=True)
    if i == 0:
        list = list.append({'Nessuno': 1}, ignore_index=True)

cross_data = list.count()
label_data = ["Facebook", "Nessuno", "VKontakte"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: ricostruzione impiego\nrispetto ai dati non presenti su Linkedin")
plt.show()

# lavoro, bloccando facebook
statistiche_dati = np.array(data.query('Work_and_Education == 0'))
list = pd.DataFrame(columns=['Linkedin', 'Nessuno', 'VKontakte'])

for item in statistiche_dati:
    i = 0
    if item[7] != 0:
        i = 1
        list = list.append({'Linkedin': 1}, ignore_index=True)
    if item[25] != 0 or item[31] != 0 or item[32] != 0 or item[33] != 0 or item[35] != 0:
        i = 1
        list = list.append({'VKontakte': 1}, ignore_index=True)
    if i == 0:
        list = list.append({'Nessuno': 1}, ignore_index=True)

cross_data = list.count()
label_data = ["Linkedin", "Nessuno", "VKontakte"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: ricostruzione formazione/lavoro\nrispetto ai dati non presenti su Facebook")
plt.show()

# formazione, bloccando vkontakte
statistiche_dati = np.array(data.query('Studiato_a == 0 or College_o_università == 0 or Scuola == 0'))
list = pd.DataFrame(columns=['Facebook', 'Nessuno'])

for item in statistiche_dati:
    i = 0
    if item[9] != 0:
        i = 1
        list = list.append({'Facebook': 1}, ignore_index=True)
    if i == 0:
        list = list.append({'Nessuno': 1}, ignore_index=True)

cross_data = list.count()
label_data = ["Facebook", "Nessuno"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: ricostruzione formazione\nrispetto ai dati non presenti su VKontakte")
plt.show()

# lavoro, bloccando vkontakte
statistiche_dati = np.array(data.query('Azienda == 0 or Stato == 0'))
list = pd.DataFrame(columns=['Facebook', 'Nessuno', 'Linkedin'])

for item in statistiche_dati:
    i = 0
    if item[9] != 0:
        i = 1
        list = list.append({'Facebook': 1}, ignore_index=True)
    if item[7] != 0:
        i = 1
        list = list.append({'Linkedin': 1}, ignore_index=True)
    if i == 0:
        list = list.append({'Nessuno': 1}, ignore_index=True)

cross_data = list.count()
label_data = ["Facebook", "Nessuno", "Linkedin"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: ricostruzione dati sul lavoro\nrispetto ai dati non presenti su VKontakte")
plt.show()

#########################################################################################

statistiche_dati = np.array(data.query('Email == 0'))
list = pd.DataFrame(columns=['Facebook', 'Nessuno', 'VKontakte'])

for item in statistiche_dati:
    i = 0
    if item[11] != 0:
        i = 1
        list = list.append({'Facebook': 1}, ignore_index=True)
    if item[30] != 0:
        i = 1
        list = list.append({'VKontakte': 1}, ignore_index=True)
    if i == 0:
        list = list.append({'Nessuno': 1}, ignore_index=True)

cross_data = list.count()
label_data = ["Facebook", "Nessuno", "VKontakte"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: ricostruzione email\nrispetto ai dati non presenti su Linkedin")
plt.show()

# email, bloccando facebook
statistiche_dati = np.array(data.query('Contact == 0'))
list = pd.DataFrame(columns=['Linkedin', 'Nessuno', 'VKontakte'])

for item in statistiche_dati:
    i = 0
    if item[4] != 0:
        i = 1
        list = list.append({'Linkedin': 1}, ignore_index=True)
    if item[30] != 0:
        i = 1
        list = list.append({'VKontakte': 1}, ignore_index=True)
    if i == 0:
        list = list.append({'Nessuno': 1}, ignore_index=True)

cross_data = list.count()
label_data = ["Linkedin", "Nessuno", "VKontakte"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: ricostruzione email\nrispetto ai dati non presenti su Facebook")
plt.show()

# email, bloccando vkontakte
statistiche_dati = np.array(data.query('Skype == 0'))
list = pd.DataFrame(columns=['Facebook', 'Nessuno', 'Linkedin'])

for item in statistiche_dati:
    i = 0
    if item[11] != 0:
        i = 1
        list = list.append({'Facebook': 1}, ignore_index=True)
    if item[4] != 0:
        i = 1
        list = list.append({'Linkedin': 1}, ignore_index=True)
    if i == 0:
        list = list.append({'Nessuno': 1}, ignore_index=True)

cross_data = list.count()
label_data = ["Facebook", "Nessuno", "Linkedin"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: ricostruzione email\nrispetto ai dati non presenti su VKontakte")
plt.show()

#########################################################################################

statistiche_dati = np.array(data.query('Compleanno == 0'))
list = pd.DataFrame(columns=['Facebook', 'Nessuno', 'VKontakte'])

for item in statistiche_dati:
    i = 0
    if item[12] != 0:
        i = 1
        list = list.append({'Facebook': 1}, ignore_index=True)
    if item[23] != 0:
        i = 1
        list = list.append({'VKontakte': 1}, ignore_index=True)
    if i == 0:
        list = list.append({'Nessuno': 1}, ignore_index=True)

cross_data = list.count()
label_data = ["Facebook", "Nessuno", "VKontakte"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: ricostruzione data di nascita\nrispetto ai dati non presenti su Linkedin")
plt.show()

# data, bloccando facebook
statistiche_dati = np.array(data.query('Basic_Info_Birthday == 0'))
list = pd.DataFrame(columns=['Linkedin', 'Nessuno', 'VKontakte'])

for item in statistiche_dati:
    i = 0
    if item[5] != 0:
        i = 1
        list = list.append({'Linkedin': 1}, ignore_index=True)
    if item[23] != 0:
        i = 1
        list = list.append({'VKontakte': 1}, ignore_index=True)
    if i == 0:
        list = list.append({'Nessuno': 1}, ignore_index=True)

cross_data = list.count()
label_data = ["Linkedin", "Nessuno", "VKontakte"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: ricostruzione data di nascita\nrispetto ai dati non presenti su Facebook")
plt.show()

# data, bloccando vkontakte
statistiche_dati = np.array(data.query('Data_di_Nascita == 0'))
list = pd.DataFrame(columns=['Facebook', 'Nessuno', 'Linkedin'])

for item in statistiche_dati:
    i = 0
    if item[12] != 0:
        i = 1
        list = list.append({'Facebook': 1}, ignore_index=True)
    if item[5] != 0:
        i = 1
        list = list.append({'Linkedin': 1}, ignore_index=True)
    if i == 0:
        list = list.append({'Nessuno': 1}, ignore_index=True)

cross_data = list.count()
label_data = ["Facebook", "Nessuno", "Linkedin"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: ricostruzione data di nascita\nrispetto ai dati non presenti su VKontakte")
plt.show()

#########################################################################################

statistiche_dati = np.array(data.query('Cellulare == 0'))
list = pd.DataFrame(columns=['Facebook', 'Nessuno', 'VKontakte'])

for item in statistiche_dati:
    i = 0
    if item[11] != 0:
        i = 1
        list = list.append({'Facebook': 1}, ignore_index=True)
    if item[28] != 0 or item[29] != 0:
        i = 1
        list = list.append({'VKontakte': 1}, ignore_index=True)
    if i == 0:
        list = list.append({'Nessuno': 1}, ignore_index=True)

cross_data = list.count()
label_data = ["Facebook", "Nessuno", "VKontakte"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: ricostruzione cellulare\nrispetto ai dati non presenti su Linkedin")
plt.show()

# tel, bloccando facebook
statistiche_dati = np.array(data.query('Contact == 0'))
list = pd.DataFrame(columns=['Linkedin', 'Nessuno', 'VKontakte'])

for item in statistiche_dati:
    i = 0
    if item[2] != 0:
        i = 1
        list = list.append({'Linkedin': 1}, ignore_index=True)
    if item[28] != 0 or item[29] != 0:
        i = 1
        list = list.append({'VKontakte': 1}, ignore_index=True)
    if i == 0:
        list = list.append({'Nessuno': 1}, ignore_index=True)

cross_data = list.count()
label_data = ["Linkedin", "Nessuno", "VKontakte"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: ricostruzione cellulare\nrispetto ai dati non presenti su Facebook")
plt.show()

# tel, bloccando vkontakte
statistiche_dati = np.array(data.query('Cellulare_2 == 0 or Telefono == 0'))
list = pd.DataFrame(columns=['Facebook', 'Nessuno', 'Linkedin'])

for item in statistiche_dati:
    i = 0
    if item[11] != 0:
        i = 1
        list = list.append({'Facebook': 1}, ignore_index=True)
    if item[2] != 0:
        i = 1
        list = list.append({'Linkedin': 1}, ignore_index=True)
    if i == 0:
        list = list.append({'Nessuno': 1}, ignore_index=True)

cross_data = list.count()
label_data = ["Facebook", "Nessuno", "Linkedin"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: ricostruzione cellulare\nrispetto ai dati non presenti su VKontakte")
plt.show()

#########################################################################################

statistiche_dati = np.array(data.query('Città == 0'))
list = pd.DataFrame(columns=['Facebook', 'Nessuno', 'VKontakte', 'Twitter'])

for item in statistiche_dati:
    i = 0
    if item[10] != 0:
        i = 1
        list = list.append({'Facebook': 1}, ignore_index=True)
    if item[17] != 0:
        i = 1
        list = list.append({'Twitter': 1}, ignore_index=True)
    if item[24] != 0 or item[26] != 0:
        i = 1
        list = list.append({'VKontakte': 1}, ignore_index=True)
    if i == 0:
        list = list.append({'Nessuno': 1}, ignore_index=True)

cross_data = list.count()
label_data = ["Facebook", "Nessuno", "VKontakte", "Twitter"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: ricostruzione Città\nrispetto ai dati non presenti su Linkedin")
plt.show()

# città, bloccando twitter
statistiche_dati = np.array(data.query('Città_Twitter == 0'))
list = pd.DataFrame(columns=['Linkedin', 'Nessuno', 'VKontakte', 'Facebook'])

for item in statistiche_dati:
    i = 0
    if item[6] != 0:
        i = 1
        list = list.append({'Linkedin': 1}, ignore_index=True)
    if item[10] != 0:
        i = 1
        list = list.append({'Facebook': 1}, ignore_index=True)
    if item[24] != 0 or item[26] != 0:
        i = 1
        list = list.append({'VKontakte': 1}, ignore_index=True)
    if i == 0:
        list = list.append({'Nessuno': 1}, ignore_index=True)

cross_data = list.count()
label_data = ["Linkedin", "Nessuno", "VKontakte", "Facebook"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: ricostruzione Città\nrispetto ai dati non presenti su Twitter")
plt.show()

# città, bloccando facebook
statistiche_dati = np.array(data.query('Placed_Lives == 0'))
list = pd.DataFrame(columns=['Linkedin', 'Nessuno', 'VKontakte', 'Twitter'])

for item in statistiche_dati:
    i = 0
    if item[6] != 0:
        i = 1
        list = list.append({'Linkedin': 1}, ignore_index=True)
    if item[17] != 0:
        i = 1
        list = list.append({'Twitter': 1}, ignore_index=True)
    if item[24] != 0 or item[26] != 0:
        i = 1
        list = list.append({'VKontakte': 1}, ignore_index=True)
    if i == 0:
        list = list.append({'Nessuno': 1}, ignore_index=True)

cross_data = list.count()
label_data = ["Linkedin", "Nessuno", "VKontakte", "Twitter"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: ricostruzione Città\nrispetto ai dati non presenti su Facebook")
plt.show()

# città, bloccando vkontakte
statistiche_dati = np.array(data.query('Città_1 == 0 or Luogo_di_Nascita == 0'))
list = pd.DataFrame(columns=['Facebook', 'Nessuno', 'Linkedin', 'Twitter'])

for item in statistiche_dati:
    i = 0
    if item[10] != 0:
        i = 1
        list = list.append({'Facebook': 1}, ignore_index=True)
    if item[17] != 0:
        i = 1
        list = list.append({'Twitter': 1}, ignore_index=True)
    if item[6] != 0:
        i = 1
        list = list.append({'Linkedin': 1}, ignore_index=True)
    if i == 0:
        list = list.append({'Nessuno': 1}, ignore_index=True)

cross_data = list.count()
label_data = ["Facebook", "Nessuno", "Linkedin", "Twitter"]
plt.pie(cross_data, labels=label_data, counterclock=True, autopct='%1.1f%%')
plt.title("Analisi cross social: ricostruzione Città\nrispetto ai dati non presenti su VKontakte")
plt.show()