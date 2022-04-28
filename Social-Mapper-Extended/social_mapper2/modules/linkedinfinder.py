# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import re
import os
from itertools import repeat
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver

# Classe concreta che istanzia il crawler per il social Linkedin
class Linkedinfinder(object):
    timeout = 1 #timeout per rallentare l'esecuzione e similuare l'operatore delll'utente reale, per limitare blocchi anti-crawler

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
        self.driver.implicitly_wait(2)
        self.driver.delete_all_cookies()

    #
    # Metodo che effettua il login al social
    #
    # @param username Stringa che rappresenta l'username dell'account da usare per il login
    # @param password Stringa che rappresenta l'password dell'account da usare per il login
    #
    def doLogin(self, username, password):
        self.driver.get("https://www.linkedin.com/uas/login")
        self.driver.execute_script('localStorage.clear();')

        # agent = self.driver.execute_script("return navigator.userAgent")
        # print("User Agent: " + agent)

        if (self.driver.title.encode('ascii', 'replace').startswith(bytes("Accesso a LinkedIn ", 'utf-8'))):
            print("\n[+] LinkedIn Login Page loaded successfully [+]")
            try:
                lnkUsername = self.driver.find_element_by_id("session_key-login")
            except:
                try:
                    lnkUsername = self.driver.find_element_by_id("username")
                except:
                    print(
                        "LinkedIn Login Page username field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")
            lnkUsername.send_keys(username)
            try:
                lnkPassword = self.driver.find_element_by_id("session_password-login")
            except:
                try:
                    lnkPassword = self.driver.find_element_by_id("password")
                except:
                    print(
                        "LinkedIn Login Page password field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")
            lnkPassword.send_keys(password)
            try:
                self.driver.find_element_by_id("btn-primary").click()
            except:
                try:
                    self.driver.find_element_by_class_name("btn__primary--large").click()
                except:
                    print(
                        "LinkedIn Login Page login button seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")
            # sleep(5)
            if (self.driver.title.encode('utf8', 'replace') == bytes("Sign In to LinkedIn", 'utf-8')):
                print("[-] LinkedIn Login Failed [-]\n")
            else:
                print("[+] LinkedIn Login Success [+]\n")
        else:
            print(
                "LinkedIn Login Page title field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")

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
    def getLinkedinProfiles(self, first_name, last_name, username, password):
        picturelist = []
        url = "https://www.linkedin.com/search/results/people/?keywords=" + first_name + "%20" + last_name + "&origin=SWITCH_SEARCH_VERTICAL"
        self.driver.get(url)

        # verifico se il login è ancora valido, altrimenti lo rieseguo
        if "login" in self.driver.current_url:
            self.doLogin(username, password)
            self.driver.get(url)
            # sleep(3)
            if "login" in self.driver.current_url:
                print("LinkedIn Timeout Error, session has expired and attempts to reestablish have failed")
                return picturelist
        searchresponse = self.driver.page_source.encode('utf-8')
        soupParser = BeautifulSoup(searchresponse, 'html.parser')

        # LinkedIn has implemented some code to say no results seemly at random, need code to research if this result pops.
        ## Anti Scraping Bypass (Try 3 times before skipping):
        # If there are no results do check
        if (len(soupParser.find_all('div', {'class': 'search-result__image-wrapper'})) == 0):
            # If there is the no results page do an additional try
            if (len(soupParser.find_all('div', {'class': 'search-no-results__image-container'})) != 0):
                self.driver.get(url)
                if "login" in self.driver.current_url:
                    self.doLogin(username, password)
                    self.driver.get(url)
                    # sleep(3)
                    if "login" in self.driver.current_url:
                        print("LinkedIn Timeout Error, session has expired and attempts to reestablish have failed")
                        return picturelist
                searchresponse = self.driver.page_source.encode('utf-8')
                soupParser = BeautifulSoup(searchresponse, 'html.parser')
                if (len(soupParser.find_all('div', {'class': 'search-result__image-wrapper'})) == 0):
                    if (len(soupParser.find_all('div', {'class': 'search-no-results__image-container'})) != 0):
                        # print("Second Check")
                        self.driver.get(url)
                        if "login" in self.driver.current_url:
                            self.doLogin(username, password)
                            self.driver.get(url)
                            if "login" in self.driver.current_url:
                                print(
                                    "LinkedIn Timeout Error, session has expired and attempts to reestablish have failed")
                                return picturelist
                        searchresponse = self.driver.page_source.encode('utf-8')
                        soupParser = BeautifulSoup(searchresponse, 'html.parser')

        # per ogni persona risultante dalla ricerca, ne estrapola la foto
        for element in soupParser.find_all('div', {'class': 'search-result__image-wrapper'}):
            try:
                link = element.find('a')['href']
                profilepic = element.find('img')['src']
                picturelist.append(["https://linkedin.com" + link, profilepic, 1.0])
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
    # @return info Array di informazioni estrapolate circa la persona trovata
    #
    def crawlerDataLinketin(self, username, password, url):
        info = {"Cellulare": "", "Sito Web": "", "Email": "", "Compleanno": "", "Città": "",
                "Impiego": ""}

        self.driver.get(url)
        sleep(1)
        # verifico se il login è ancora valido, altrimenti lo rieseguo
        if "login" in self.driver.current_url:
            self.doLogin(username, password)
            sleep(3)
            if "login" in self.driver.current_url:
                print("LinkedIn Timeout Error, session has expired and attempts to reestablish have failed")
        searchresponse = self.driver.page_source.encode('utf-8')
        soupParser = BeautifulSoup(searchresponse, 'html.parser')
        sleep(1)
        # estrapolo le informazioni circa l'impiego
        for element in soupParser.findAll('h2', {'class': 'mt1 t-18 t-black t-normal break-words'}):
            try:
                l = element.text
                l = l.strip()
                impiego = str(l)
                info["Impiego"] = l

            except Exception as e:
                print(e)
        # estrapolo le informazioni circa la città di residenza
        for element in soupParser.findAll('li', {'class': 't-16 t-black t-normal inline-block'}):
            try:
                l = element.text
                l = l.strip()
                luogo = str(l)
                info["Città"] = luogo
            except Exception as e:
                print(e)

        # carico la sezione delle Contact-info
        self.driver.get(url + "detail/contact-info/")
        searchresponse = self.driver.page_source.encode('utf-8')
        soupParser = BeautifulSoup(searchresponse, 'html.parser')
        # estrapolo le informazioni circa il cellulare
        for element in soupParser.findAll('section', {'class': 'pv-contact-info__contact-type ci-phone'}):
            try:
                for element2 in element.findAll('span', {'class': 't-14 t-black t-normal'}):
                    l = element2.text
                    l = l.strip()
                    cellulare = str(l)
                    info["Cellulare"] = cellulare
            except Exception as e:
                print(e)
        # estrapolo le informazioni circa il compleanno
        for element in soupParser.findAll('section', {'class': 'pv-contact-info__contact-type ci-birthday'}):
            try:
                for element2 in element.findAll('span',
                                                {'class': 'pv-contact-info__contact-item t-14 t-black t-normal'}):
                    l = element2.text
                    l = l.strip()
                    compleanno = str(l)
                    info["Compleanno"] = compleanno
            except Exception as e:
                print(e)
        # estrapolo le informazioni circa il sito web personale o dell'azienda di lavoro
        for element in soupParser.findAll('section', {'class': 'pv-contact-info__contact-type ci-websites'}):
            try:
                for element2 in element.findAll('a', {'class': 'pv-contact-info__contact-link t-14 t-black t-normal'}):
                    l = element2.text
                    l = l.strip()
                    sito = str(l)
                    info["Sito Web"] = sito
            except Exception as e:
                print(e)
        # estrapolo le informazioni circa l'e-mail
        for element in soupParser.findAll('section', {'class': 'pv-contact-info__contact-type ci-email'}):
            try:
                for element2 in element.findAll('a', {'class': 'pv-contact-info__contact-link t-14 t-black t-normal'}):
                    l = element2.text
                    l = l.strip()
                    email = str(l)
                    info["Email"] = email
            except Exception as e:
                print(e)
        return info

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
