# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys
import traceback
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver

# Classe concreta che istanzia il crawler per il social Pinterest
class Pinterestfinder(object):
    timeout = 10 #timeout per rallentare l'esecuzione e similuare l'operatore delll'utente reale, per limitare blocchi anti-crawler

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
        self.driver.get("https://www.pinterest.com/login/")
        self.driver.execute_script('localStorage.clear();')

        # verifica se il sessione è ancora valida, in caso negativo la ricrea rieseguendo i login e rieffettua la ricerca
        if (self.driver.title.encode('ascii', 'replace').startswith(bytes("Pinterest", 'utf-8'))):
            print("\n[+] Pinterest Login Page loaded successfully [+]")
            try:
                pinUsername = self.driver.find_element_by_id("email")
            except:
                print(
                    "Pinterest Login Page username field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")
                sys.exit()
            pinUsername.send_keys(username)
            sleep(2)

            try:
                # pinPassword = self.driver.find_element_by_xpath("//input[@class='js-password-field']")
                pinPassword = self.driver.find_element_by_id("password")
            except:
                print(
                    "Pinterest Login Page password field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")
                sys.exit()
            pinPassword.send_keys(password)
            sleep(2)

            try:
                pinLoginButton = self.driver.find_element_by_xpath("//button[@class='red SignupButton active']")
            except:
                print(
                    "Pinterest Login Page login button name seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")
                traceback.print_exc()
                sys.exit()
            pinLoginButton.click()
            sleep(5)

            if (self.driver.title.encode('ascii', 'replace').startswith(bytes("Pinterest", 'utf-8'))):
                print("[-] Pinterest Login Failed [-]\n")
            else:
                print("[+] Pinterest Login Success [+]\n")
        else:
            print(
                "Pinterest Login Page title field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")

    #
    # Metodo che effettua la ricerca di una persona sul social
    #
    # @param first_name Stringa che rappresenta il nome della persona da cercare
    # @param last_name Stringa che rappresenta il cognome della persona da cercare
    #
    # @return picturelist Array di persone trovare rispetto al nome in input
    #
    def getPinterestProfiles(self, first_name, last_name):
        # effettua la ricerca compilando il campo apposito
        url = "https://www.pinterest.de/search/users/?q=" + first_name + "%20" + last_name
        self.driver.get(url)
        sleep(3)
        searchresponse = self.driver.page_source.encode('utf-8')
        soupParser = BeautifulSoup(searchresponse, 'html.parser')
        picturelist = []

        # per ogni persona risultante dalla ricerca, ne estrapola la foto
        for element in soupParser.find_all('div', {'class': 'Yl-'}):
            try:
                link = element.find('a')['href']
                smallpic = element.find('img')['src']
                # replaced1 = smallpic.replace()
                # profilepic = replaced1.replace("_bigger.jpeg","_400x400.jpg")
                picturelist.append(["https://pinterest.com" + link, smallpic, 1.0])
            # print(smallpic)
            except:
                continue
        return picturelist

    #
    # Metodo che termnina la sessione
    #
    def kill(self):
        self.driver.quit()
