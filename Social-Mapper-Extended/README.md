# Progetto-FDSML
Repository creata per il progetto di Fondamenti di Data Science e Machine Learning: Social mapper.

## Introduzione
![alt text](https://img.shields.io/badge/Python-3_only-blue.svg "Python 3 only")
![alt text](https://img.shields.io/travis/Greenwolf/social_mapper.svg "Travis build status")

Social Mapper è uno strumento di intelligenza open source che utilizza il riconoscimento facciale per correlare i profili dei social media su diversi siti su larga scala. Adotta un approccio automatizzato per cercare nei siti di social media popolari i nomi e le immagini dei target per rilevare e raggruppare con precisione la presenza di una persona, trascrivendo i risultati in un report in modo che un operatore umano possa visionarli rapidamente.

Social Mapper ha una varietà di usi nel settore della sicurezza, ad esempio la raccolta automatica di grandi quantità di profili di social media da utilizzare in campagne di phishing mirate. Il riconoscimento facciale aiuta questo processo rimuovendo i falsi positivi nei risultati della ricerca, in modo che la revisione di questi dati sia più rapida per un operatore umano.

Social Mapper supporta le seguenti piattaforme di social media:
* LinkedIn
* Facebook
* Pinterest
* Twitter
* Instagram
* VKontakte
* Weibo
* Douban

Social Mapper accetta una varietà di tipi di input come:
* Il nome di un'organizzazione, la ricerca tramite LinkedIn
* Una cartella piena di immagini con nome
* Un file CSV con nomi e URL per le immagini online

## Descrizione progetto                                                                                                                                                 
Il codice originale di SocialMapper ha subito le seguenti migliorie:                                                                                                                                
* aggiornamento delle componenti che effettuano la ricerca sui social network, inserendo i nuovi identificativi delle nuove versioni di questi;                                     
* lieve miglioramento della velocità d'esecuzione;                                                                                                                      
* correzione delle componenti errate e ripulitura del codice;                                                                                                                                  
* creazione di funzioni apposite di crawling per i social per estrarre le informazioni degli utenti, dove presenti;                                                                             
* creazione di dizionari dedicati per ogni social network strutturati per contenere tutte le informazioni che possono essere estratte;                                  
* modellazione di un csv restituito in output con tutte le estrazioni effettuate da ogni social, creando così un dataset.                                                                        

Non è stato creato un crawler per Pinterest, poichè tale social non presenta informazioni testuali dell'utente oltre al suo username.  
 
Per Weibo e Douban invece non è stato creato ne il crawler, ne è stata migliorata la componente di ricerca. 
Non è stato possibile lavorare su tali social asiatici poichè per la registrazione è richiesto obligatoriamente un numero di telefono, ma il prefisso italiano non è accettato.

## Istallazione

Le seguenti istruzioni mostrano i requisiti necessari e come usare Social Mapper.
Ulteriori informazioni sono contenute nel file README.md nella sottocartella `/ socialmapper2`.
 
### Prerequisiti

Trattandosi di uno strumento basato su Python3, dovrebbe teoricamente funzionare su Linux, ChromeOS ([Modalità sviluppatore] (https://www.chromium.org/chromium-os/developer-information-for-chrome-os-devices/generic) ) e macOS. I requisiti principali sono Firefox, Selenium e Geckodriver. Per installare lo strumento e configurarlo, seguire questi 4 passaggi:

1) Installare l'ultima versione di Mozilla Firefox per macOS qui:
```
https://www.mozilla.org/en-GB/firefox/new/
``` 
O per Debian/Kali (ma non richiesto per Ubuntu) ottenere la versione non ESR di Firefox con:
```
sudo add-apt-repository ppa:mozillateam/firefox-next && sudo apt update && sudo apt upgrade
```
Assicurarsi che la nuova versione di Firefox sia nel percorso. Se non presente, aggiungerla manualmente.

2) Installare Geckodriver per il sistema operativo e assicurati che sia nel giusto percorso, su Mac lo si puo posizionare in `/ usr / local / bin`, su ChromeOS lo si puo mettere in ` / usr / local / bin`, e su Linux in `/ usr / bin`.

Scaricare l'ultima versione di Geckodriver qui:
```
https://github.com/mozilla/geckodriver/releases
```   
3) Installare le librerie richieste:

Su Linux installare i seguenti prerequisiti:

```
sudo apt-get install build-essential cmake
sudo apt-get install libgtk-3-dev
sudo apt-get install libboost-all-dev
```

Su Linux e macOS, completare l'installazione con:

```
git clone https://github.com/Greenwolf/social_mapper
cd social_mapper/setup
python3 -m pip install --no-cache-dir -r requirements.txt
```           

## Utilizzo di Social Mapper

Social Mapper viene eseguito da riga di comando utilizzando una combinazione di parametri obbligatori e facoltativi. È possibile specificare opzioni come il tipo di input e quali siti controllare insieme a una serie di altri parametri che influiscono sulla velocità e l'accuratezza.

### Parametri obbligatori

Per avviare lo strumento devono essere forniti 4 parametri, un formato di input, il file o la cartella di input e la modalità di esecuzione di base:

```
-f, --format	: Specify if the -i, --input is a 'name', 'csv', 'imagefolder' or 'socialmapper' resume file
-i, --input	: The company name, a CSV file, imagefolder or Social Mapper HTML file to feed into Social Mapper
-m, --mode	: 'fast' or 'accurate' allows you to choose to skip potential targets after a first likely match is found, in some cases potentially speeding up the program x20
```

Inoltre, è necessario selezionare almeno un sito di social media da controllare includendo uno o più dei seguenti:

```
-a, --all		: Selects all of the options below and checks every site that Social Mapper has credentials for
-fb, --facebook		: Check Facebook
-tw, --twitter		: Check Twitter
-ig, --instagram	: Check Instagram
-li, --linkedin		: Check LinkedIn
-vk, --vkontakte	: Check VKontakte
-wb, --weibo		: Check Weibo
-db, --douban		: Check Douban
```         

### Parametri opzionali

È inoltre possibile impostare parametri opzionali aggiuntivi per aggiungere ulteriore personalizzazione al modo in cui viene eseguito Social Mapper:

```
-t, --threshold		: Customises the facial recognition threshold for matches, this can be seen as the match accuracy. Default is 'standard', but can be set to 'loose', 'standard', 'strict' or 'superstrict'. For example 'loose' will find more matches, but some may be incorrect. While 'strict' may find less matches but also contain less false positives in the final report.
-cid, --companyid	: Additional parameter to add in a LinkedIn Company ID for if name searches are not picking the correct company.
-s, --showbrowser	: Makes the Firefox browser visible so you can see the searches performed. Useful for debugging.
-v, --version		: Display current version.
-e, --email		: Provide a fuzzy email format like "<f><last>@domain.com" to generate additional CSV files for each site with firstname, lastname, fullname, email, profileURL, photoURL. These can be fed into phishing frameworks such as Gophish or Lucy.

```

### Esempi di esecuzioni 

Di seguito sono mostrati alcuni esempi di esecuzioni:

```
python3 social_mapper.py -f imagefolder -i ./mytargets -m fast -fb -tw

python3 social_mapper.py -f company -i "SpiderLabs" -m accurate -a -t strict     
``` 