# -*- coding: utf-8 -*-
from __future__ import print_function

import os
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver

# Classe concreta che istanzia il crawler per il social Vkontakte
class Vkontaktefinder(object):
    timeout = 100 #timeout per rallentare l'esecuzione e similuare l'operatore delll'utente reale, per limitare blocchi anti-crawler

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
        self.driver.implicitly_wait(15)
        self.driver.delete_all_cookies()

    #
    # Metodo che effettua il login al social
    #
    # @param username Stringa che rappresenta l'username dell'account da usare per il login
    # @param password Stringa che rappresenta l'password dell'account da usare per il login
    #
    def doLogin(self, username, password):
        self.driver.get("https://www.vk.com/login")
        self.driver.execute_script('localStorage.clear();')

        if (self.driver.title.encode('ascii', 'replace').startswith(bytes("Log in", 'utf-8'))):
            print("\n[+] VKontakte Login Page loaded successfully [+]")
            vkUsername = self.driver.find_element_by_id("email")
            vkUsername.send_keys(username)
            vkPassword = self.driver.find_element_by_id("pass")
            vkPassword.send_keys(password)
            self.driver.find_element_by_id("login_button").click()
            sleep(10)
            if (self.driver.title.encode('ascii', 'replace').startswith(bytes("Log in", 'utf-8')) == False):
                print("[+] Vkontakte Login Success [+]\n")
            else:
                print("[-] Vkontakte Login Failed [-]\n")

    #
    # Metodo che effettua la ricerca di una persona sul social
    #
    # @param first_name Stringa che rappresenta il nome della persona da cercare
    # @param last_name Stringa che rappresenta il cognome della persona da cercare
    #
    # @return picturelist Array di persone trovare rispetto al nome in input
    #
    def getVkontakteProfiles(self, first_name, last_name):
        # effettua la ricerca compilando il campo apposito
        url = "https://vk.com/search?c%5Bq%5D=" + first_name + "%20" + last_name + "&c%5Bsection%5D=auto"
        self.driver.get(url)
        sleep(3)
        searchresponse = self.driver.page_source.encode('utf-8')
        soupParser = BeautifulSoup(searchresponse, 'html.parser')
        picturelist = []

        # per ogni persona risultante dalla ricerca, ne estrapola la foto
        for element in soupParser.find_all('div', {'class': 'people_row'}):  # "people_row search_row clear_fix"
            try:
                link = element.find('a')['href']
                profilepic = element.find('img')['src']
                picturelist.append(["https://vk.com" + link, profilepic, 1.0])
            except:
                continue
        return picturelist

    def normalizeDictionary(self, vkontackte):
        standard = {"Data di Nascita": "", "Città": "", "Studiato a": "", "Luogo di Nascita": "", "Lingue": "",
                    "Cellulare": "", "Telefono": "", "Skype": "", "College o università": "", "Stato": "", "Scuola": "",
                    "Gruppi": "", "Azienda": "", "Interesse": ""}

        for label in vkontackte.keys():
            if label in standard.keys():
                standard[label] = vkontackte[label]
        return standard

    #
    # Metodo che effettua la ricerca di una persona sul social
    #
    # @param username Stringa che rappresenta l'username dell'account da usare per il login
    # @param password Stringa che rappresenta l'password dell'account da usare per il login
    # @param url Stringa legata al profilo della persona ricercata, identificata tramite face-recognition
    #
    # @return vkontackte Array di informazioni estrapolate circa la persona trovata
    #
    def crawlerDataVkontackte(self, username, password, url):
        self.driver.get(url)
        sleep(1)
        # verifico se il login è ancora valido, altrimenti lo rieseguo
        if "login" in self.driver.current_url:
            self.doLogin(username, password)
            sleep(3)
            if "login" in self.driver.current_url:
                print("Vkontackte Timeout Error, session has expired and attempts to reestablish have failed")
        # accedo alla sezione completa dei dettagli della persona
        self.driver.find_element_by_class_name("profile_more_info_link").click()
        searchresponse = self.driver.page_source.encode('utf-8')
        soupParser = BeautifulSoup(searchresponse, 'html.parser')
        sleep(1)
        i = 0
        # estrapola le label delle informazioni trovate
        labellist = []
        for element in soupParser.findAll('div', {'class': 'label fl_l'}):
            labellist.append((element.text).replace(":", ""))

        # estrapola le informazioni trovate collegandole alle label precedentemente acquisite
        vkontackte = {}
        for element in soupParser.findAll('div', {'class': 'labeled'}):
            if i > 1:
                info = ""
                for el in element.findAll('a'):
                    l = str(el)
                    l = l.split('">')[1]
                    l = l.split('</a>')[0]
                    if info == "":
                        info = l
                    else:
                        info = info + " " + l

                    d = {labellist[i - 2]: info}
                vkontackte.update(d)
            i = i + 1
        vkontackte = self.normalizeDictionary(vkontackte)
        return vkontackte

    #
    # Metodo che termnina la sessione
    #
    def kill(self):
        self.driver.quit()
