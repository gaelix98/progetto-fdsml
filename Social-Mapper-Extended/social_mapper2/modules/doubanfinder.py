# -*- coding: utf-8 -*-
from __future__ import print_function

import os
from time import sleep

from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver

# Classe concreta che istanzia il crawler per il social Douban
class Doubanfinder(object):
    timeout = 10 #timeout per rallentare l'esecuzione e similuare l'operatore delll'utente reale, per limitare blocchi anti-crawler

    #
    # Metodo init per settare proprietà del browser
    #
    # @param showbrowser Stringa legata al comando da console, se presente si richiede la visine in real-time della ricerca
    #
    def __init__(self, showbrowser):
        display = Display(visible=0, size=(1600, 1024))
        display.start()
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
        self.driver.get("https://www.douban.com")
        self.driver.execute_script('localStorage.clear();')

        if (self.driver.title.encode('utf8', 'replace').startswith(bytes("登录", 'utf-8'))):
            print("\n[+] Douban Login Page loaded successfully [+]")
            wbUsername = self.driver.find_element_by_id("email")
            wbUsername.send_keys(username)
            wbPassword = self.driver.find_element_by_id("password")
            wbPassword.send_keys(password)
            # self.driver.find_element_by_id("login_button").click()
            # self.driver.find_element_by_css_selector('a.submitBtn').click()
            self.driver.find_element_by_css_selector('input[type=\'submit\']').click()
            sleep(5)
            if (self.driver.title.encode('utf8', 'replace').startswith(bytes("豆", 'utf-8')) == False):
                print("[+] Douban Login Success [+]\n")
            else:
                print("[-] Douban Login Failed [-]\n")

    #
    # Metodo che effettua la ricerca di una persona sul social
    #
    # @param first_name Stringa che rappresenta il nome della persona da cercare
    # @param last_name Stringa che rappresenta il cognome della persona da cercare
    #
    # @return picturelist Array di persone trovare rispetto al nome in input
    #
    def getDoubanProfiles(self, first_name, last_name):
        # effettua ricerca della parsona richiesta
        url = "https://www.douban.com/search?cat=1005&q=" + first_name + "+" + last_name
        self.driver.get(url)
        sleep(3)
        searchresponse = self.driver.page_source.encode('utf-8')
        soupParser = BeautifulSoup(searchresponse, 'html.parser')
        picturelist = []
        # per ogni persona risultante dalla ricerca, ne estrapola la foto
        for element in soupParser.find_all('div', {'class': 'pic'}):
            try:
                badlink = element.find('a')['href']
                link = badlink.split('?url=', 1)[1].split('&query', 1)[0].replace("%3A", ":").replace("%2F", "/")
                badprofilepiclinksmall = element.find('img')['src']
                profilepic = badprofilepiclinksmall.replace("/icon/u", "/icon/ul")
                picturelist.append([link, profilepic, 1.0])
            except Exception as e:
                continue
        return picturelist

    #
    # Metodo che termnina la sessione
    #
    def kill(self):
        self.driver.quit()
