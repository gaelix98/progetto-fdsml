# -*- coding: utf-8 -*-
from __future__ import print_function

import json
import os
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver

# Classe concreta che istanzia il crawler per il social Facebook
class Facebookfinder(object):
    timeout = 5 #timeout per rallentare l'esecuzione e similuare l'operatore delll'utente reale, per limitare blocchi anti-crawler

    #
    # Metodo init per settare proprietà del browser
    #
    # @param showbrowser Stringa legata al comando da console, se presente si richiede la visine in real-time della ricerca
    #
    def __init__(self, showbrowser):
        # display = Display(visible=0, size=(1600, 1024))
        # display.start()
        if not showbrowser:
            os.environ['MOZ_HEADLESS'] = '1'
        firefoxprofile = webdriver.FirefoxProfile()
        firefoxprofile.set_preference("permissions.default.desktop-notification", 1)
        firefoxprofile.set_preference("dom.webnotifications.enabled", 1)
        firefoxprofile.set_preference("dom.push.enabled", 1)
        self.driver = webdriver.Firefox(firefox_profile=firefoxprofile)
        self.driver.implicitly_wait(3)
        self.driver.delete_all_cookies()

    #
    # Metodo che effettua il login al social
    #
    # @param username Stringa che rappresenta l'username dell'account da usare per il login
    # @param password Stringa che rappresenta l'password dell'account da usare per il login
    #
    def doLogin(self, username, password):
        self.driver.get("https://www.facebook.com/login")
        self.driver.execute_script('localStorage.clear();')

        if (self.driver.title.encode('ascii', 'replace').endswith(bytes("Facebook", 'utf-8'))):
            print("\n[+] Facebook Login Page loaded successfully [+]")
            fbUsername = self.driver.find_element_by_id("email")
            fbUsername.send_keys(username)
            fbPassword = self.driver.find_element_by_id("pass")
            fbPassword.send_keys(password)
            self.driver.find_element_by_id("loginbutton").click()
            sleep(5)
            # checks if a notification is in place, which changes the title
            if (self.driver.title.encode('utf8', 'replace')[0] == "("):
                if (str(self.driver.title.encode('utf8', 'replace').split()[1]) == bytes("Facebook", 'utf-8')):
                    print("[+] Facebook Login Success [+]\n")
                else:
                    print("[-] Facebook Login Failed [-]\n")
            else:
                if (self.driver.title.encode('utf8', 'replace').startswith(bytes("Facebook", 'utf-8')) == True):
                    print("[+] Facebook Login Success [+]\n")
                else:
                    print("[-] Facebook Login Failed [-]\n")

    #
    # Metodo che effettua la ricerca di una persona sul social
    #
    # @param first_name Stringa che rappresenta il nome della persona da cercare
    # @param last_name Stringa che rappresenta il cognome della persona da cercare
    # @param username Stringa che rappresenta l'username dell'account da usare per il login
    # @param password Stringa che rappresenta l'password dell'account da usare per il login
    #
    # @return picturelist Array di persone trovare rispetto al nome in input
    #
    def getFacebookProfiles(self, first_name, last_name, username, password):
        # effettuo la ricerca, compilando il campo apposito
        url = "https://www.facebook.com/search/people/?q=" + first_name + "%20" + last_name
        self.driver.get(url)
        sleep(3)
        picturelist = []

        # verifica se il sessione è ancora valida, in caso negativo la ricrea rieseguendo i login e rieffettua la ricerca
        if (self.driver.title.encode('utf8', 'replace').split()[1].startswith(
                bytes(first_name, 'utf-8')) == False and self.driver.title.encode('utf8', 'replace').startswith(
            bytes(first_name, 'utf-8')) == False):
            print("\nFacebook session has expired, attempting to reestablish...")
            self.doLogin(username, password)
            self.driver.get(url)
            sleep(3)
            if (self.driver.title.encode('utf8', 'replace').split()[1].startswith(
                    bytes(first_name, 'utf-8')) == False and self.driver.title.encode('utf8', 'replace').startswith(
                bytes(first_name, 'utf-8')) == False):
                print("Facebook Timeout Error, session has expired and attempts to reestablish have failed")
                return picturelist
            else:
                print("New Facebook Session created, resuming mapping process")

        searchresponse = self.driver.page_source.encode('utf-8')
        soupParser = BeautifulSoup(searchresponse, 'html.parser')
        # per ogni persona risultante dalla ricerca, ne estrapola la foto
        for element in soupParser.find_all('div', {'class': '_401d'}):
            try:
                datagt = element['data-gt']
                stripped = datagt.replace("\\", "")
                stripped2 = stripped.replace("{\"type\":\"xtracking\",\"xt\":\"21.", "")
                stripped3 = stripped2.replace("}\"}", "}")
                jsondata = json.loads(stripped3)
                profilepic = "https://www.facebook.com/search/async/profile_picture/?fbid=" + str(
                    jsondata['raw_id']) + "&width=8000&height=8000"
                link = element.find('a')['href']
                cdnpicture = element.find('img')['src']
                picturelist.append([link, profilepic, 1.0, cdnpicture])
            except:
                continue
        return picturelist

    #
    # Metodo che effettua la ricerca di una persona sul social
    #
    # @param username Stringa che rappresenta l'username dell'account da usare per il login
    # @param password Stringa che rappresenta l'password dell'account da usare per il login
    # @param url Stringa legata al profilo della persona ricercata, identificata tramite face-recognition
    #
    # @return facebook Array di informazioni estrapolate circa la persona trovata
    #
    def crawlerDataFacebook(self, username, password, url):
        info = ""
        facebook = {"Work_and_Education": "", "Placed_Lives": "", "Contact": "", "Basic_Info": "", "Detail_about": ""}
        url = url.split("?")[0]
        self.driver.get(url)
        # verifico se il login è ancora valido, altrimenti lo rieseguo (max 2 volte)
        if "login" in self.driver.current_url:
            self.doLogin(username, password)

            if "login" in self.driver.current_url:
                print("Facebook Timeout Error, session has expired and attempts to reestablish have failed")
        searchresponse = self.driver.page_source.encode('utf-8')
        sleep(1)

        # carico la sezione Work_and_Education
        self.driver.get(url + "?sk=about&section=education&lst=100052072695021%3A1084323423%3A1592853368")
        searchresponse = self.driver.page_source.encode('utf-8')
        soupParser = BeautifulSoup(searchresponse, 'html.parser')
        # estrapolo le informazioni nella sezione Work_and_Education della persona trovata
        for element in soupParser.findAll('div', {'class': "_42ef"}):
            try:
                info = info + element.text + "\\"
            except Exception as e:
                print(e)
        if "No workplaces to show\\No schools to show\\" == info or "Add a workplace\\Add a professional skill\\Add a college\\Add a high school\\" == info:
            facebook["Work_and_Education"] = ""
        else:
            app = str(info[:-1])
            facebook["Work_and_Education"] = app

        # carico la sezione Placed_Lives
        info = ""
        self.driver.get(url + "?sk=about&section=living&lst=100052072695021%3A1084323423%3A1592853368")
        searchresponse = self.driver.page_source.encode('utf-8')
        soupParser = BeautifulSoup(searchresponse, 'html.parser')
        # estrapolo le informazioni nella sezione Placed_Lives della persona trovata
        for element in soupParser.findAll('div', {'class': "_42ef"}):
            try:
                info = info + element.text + "\\"
            except Exception as e:
                print(e)
        if "No current city to show\\No hometown to show\\no place to show\\" == info or "Add your current city\\Add your hometown\\Add a place\\" == info:
            facebook["Placed_Lives"] = ""
        else:
            info = info.replace("Current city", "(Current city)")
            info = info.replace("Hometown", "(Hometown)")
            app = str(info[:-1])
            facebook["Placed_Lives"] = app
        # carico la sezione Contact e Basic_Info
        info = ""
        self.driver.get(url + "?sk=about&section=contact-info&lst=100052072695021%3A1084323423%3A1592853368")
        searchresponse = self.driver.page_source.encode('utf-8')
        soupParser = BeautifulSoup(searchresponse, 'html.parser')
        # estrapolo le informazioni nelle sezioni Contact e Basic_Info della persona trovata
        for element in soupParser.findAll('li', {'class': "_3pw9 _2pi4"}):
            try:
                info = info + element.text + "\\"
            except Exception as e:
                print(e)
        if "No contact info to show\\" == info:
            facebook["Contact"] = ""
        else:
            app = str(info[:-1])
            facebook["Contact"] = app

        info = ""
        for element in soupParser.findAll('li', {'class': "_3pw9 _2pi4 _2ge8 _3ms8"}):
            try:
                info = info + element.text + "\\"
            except Exception as e:
                print(e)
        info = info.replace("Gender", "(Gender)")
        app = str(info[:-1])
        facebook["Basic_Info"] = app

        # Families and Relationship
        # self.driver.get(url + "?sk=about&section=relationship&lst=100052072695021%3A1084323423%3A1592853368")
        # searchresponse = self.driver.page_source.encode('utf-8')
        # soupParser = BeautifulSoup(searchresponse, 'html.parser')
        # relazioni
        # for element in soupParser.findAll('div', {'class': "_vb- _50f5"}):
        #     try:
        #
        #     except:
        #         continue
        #
        # persone di famiglia
        # for element in soupParser.findAll('a', {'id': "js_1xk"}):
        #     try:
        #
        #     except:
        #         continue

        # carico la sezione Detail_about
        info = ""
        self.driver.get(url + "?sk=about&section=bio&lst=100052072695021%3A1084323423%3A1592853368")
        searchresponse = self.driver.page_source.encode('utf-8')
        soupParser = BeautifulSoup(searchresponse, 'html.parser')
        # estrapolo le informazioni nella sezione Detail_about della persona trovata
        for element in soupParser.findAll('li', {'class': "_3pw9 _2pi4"}):
            try:
                info = info + element.text + "\\"
            except Exception as e:
                continue
        if "No additional details to show" in info or "No favorite quotes to show" in info or "\"\"" == info:
            facebook["Detail_about"] = ""
        else:
            app = str(info[:-1])
            facebook["Detail_about"] = app

        return facebook

    #
    # Metodo che restituisce tutti i cookies presenti
    #
    def getCookies(self):
        all_cookies = self.driver.get_cookies()
        cookies = {}
        for s_cookie in all_cookies:
            cookies[s_cookie["name"]] = s_cookie["value"]
        return cookies

    #
    # Metodo che elimina tutti i cookies presenti
    #
    def testdeletecookies(self):
        self.driver.delete_all_cookies()

    #
    # Metodo che termnina la sessione
    #
    def kill(self):
        self.driver.quit()
