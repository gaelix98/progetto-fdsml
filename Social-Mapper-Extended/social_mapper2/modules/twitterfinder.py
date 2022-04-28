# -*- coding: utf-8 -*-
from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from time import sleep
import traceback
import sys
import os
from bs4 import BeautifulSoup

# Classe concreta che istanzia il crawler per il social Twitter
class Twitterfinder(object):
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
        self.driver.get("https://twitter.com/login?lang=en-gb")
        self.driver.execute_script('localStorage.clear();')
        sleep(4)
        if (self.driver.title.encode('ascii', 'replace').startswith(bytes("Login on", 'utf-8'))):
            print("\n[+] Twitter Login Page loaded successfully [+]")
            try:
                twUsername = self.driver.find_element_by_name("session[username_or_email]")
            except:
                print(
                    "Twitter Login Page username field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")
                sys.exit()
            twUsername.send_keys(username)
            sleep(2)

            try:
                # twPassword = self.driver.find_element_by_xpath("//input[@class='js-password-field']")
                twPassword = self.driver.find_element_by_name("session[password]")
            except:
                print(
                    "Twitter Login Page password field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")
                sys.exit()
            twPassword.send_keys(password)
            sleep(2)

            try:
                twLoginButton = self.driver.find_element_by_xpath(
                    "/html/body/div/div/div/div/main/div/div/form/div/div[3]/div")
            except:
                print(
                    "Twitter Login Page login button name seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")
                traceback.print_exc()
                sys.exit()
            twLoginButton.click()
            sleep(5)

            if (self.driver.title.encode('ascii', 'replace').startswith(bytes("Login on", 'utf-8'))):
                print("[-] Twitter Login Failed [-]\n")
            else:
                print("[+] Twitter Login Success [+]\n")
        else:
            print(
                "Twitter Login Page title field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")

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
    def getTwitterProfiles(self, first_name, last_name):
        # effettua la ricerca compilando il campo apposito
        url = "https://twitter.com/search?q=" + first_name + "%20" + last_name + "&src=typed_query"
        self.driver.get(url)
        sleep(3)
        searchresponse = self.driver.page_source.encode('utf-8')
        soupParser = BeautifulSoup(searchresponse, 'html.parser')
        picturelist = []

        # per ogni persona risultante dalla ricerca, ne estrapola la foto
        for element in soupParser.find_all('div', {
            'class': 'css-18t94o4 css-1dbjc4n r-1ny4l3l r-1j3t67a r-1w50u8q r-o7ynqc r-6416eg'}):
            try:
                link = element.find('a')['href']
                smallpic = element.find('img')['src']
                # replaced1 = smallpic.replace("_bigger.jpg","_400x400.jpg")
                # profilepic = replaced1.replace("_bigger.jpeg","_400x400.jpg")
                profilepic = smallpic.replace("_reasonably_small.", "_400x400.")
                picturelist.append(["https://twitter.com" + link, profilepic, 1.0])

            except:
                print("Error")
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
    def crawlerDataTwitter(self, username, password, url):
        info = {"Città_twitter": "", "Sito_twitter": "", "Twitter_Biografia": ""}
        self.driver.get(url)
        sleep(1)
        # verifico se il login è ancora valido, altrimenti lo rieseguo
        if "login" in self.driver.current_url:
            self.doLogin(username, password)
            sleep(3)
            if "login" in self.driver.current_url:
                print("Twitter Timeout Error, session has expired and attempts to reestablish have failed")
        searchresponse = self.driver.page_source.encode('utf-8')
        soupParser = BeautifulSoup(searchresponse, 'html.parser')
        sleep(1)
        # estrapolo la Biografia della persona trovata
        for element in soupParser.findAll('div', {'data-testid': 'UserDescription'}):
            try:
                for element2 in element.findAll('span', {
                    'class': 'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0'}):
                    biografia = element2.text
                    info["Twitter_Biografia"] = biografia
            # info["Cellulare"] = cellulare
            except Exception as e:
                print(e)
        # estrapolo, per ogni persona trovata, la città e il sito web
        for element in soupParser.findAll('div', {'data-testid': 'UserProfileHeader_Items'}):
            try:
                for element2 in element.findAll('span', {
                    'class': 'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0'}):
                    città = element2.text
                    info["Città_twitter"] = città
                    break
                for element2 in element.findAll('a', {
                    'class': 'css-4rbku5 css-18t94o4 css-901oao css-16my406 r-13gxpu9 r-1loqt21 r-4qtqp9 r-1qd0xha r-ad9z0x r-zso239 r-bcqeeo r-qvutc0'}):
                    sito = element2.text
                    info["Sito_twitter"] = sito
            except Exception as e:
                print(e)

        return info

    #
    # Metodo che termnina la sessione
    #
    def kill(self):
        self.driver.quit()
