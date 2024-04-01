from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from Login_details import email, password
import re
import urllib.request
import numpy as np
from main import isWhite
import cv2
from bs4 import BeautifulSoup


class tinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome()
    def open(self):
        self.driver.get("https://www.tinder.com")
        sleep(15)

        login = self.driver.find_element(By.XPATH,'//*[@id="o-1868991261"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a/div[2]/div[2]')
        login.click()
        sleep(5)

        self.LoginFacebook()
        try:
            self.locationAccess()
        except:
            print("No Location Pop-up")

        self.autoLike()

    def LoginFacebook(self):
        facebook = self.driver.find_element(By.XPATH,'//*[@id="o697594959"]/main/div/div/div[1]/div/div/div[3]/span/div[2]/button/div[2]/div[2]/div/div')
        facebook.click()
        sleep(2)

        base_window = self.driver.window_handles[0]
        facebook_window = self.driver.window_handles[1]
        self.driver.switch_to.window(facebook_window)

        emailInput = self.driver.find_element(By.XPATH,'//*[@id="email"]')
        passwordInput = self.driver.find_element(By.XPATH,'//*[@id="pass"]')
        loginButton = self.driver.find_element(By.XPATH,'//*[@id="loginbutton"]')

        emailInput.send_keys(email)
        passwordInput.send_keys(password)
        loginButton.click()

        self.driver.switch_to.window(base_window)
        sleep(10)

    def Find(self, string):
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex, string)
        return [x[0] for x in url]

    def locationAccess(self):
        location = self.driver.find_element(By.XPATH,'//*[@id="q779046258"]/main/div/div/div/div[3]/button[1]/div[2]/div[2]')
        location.click()
        sleep(5)

        notifications = self.driver.find_element(By.XPATH,'//*[@id="q779046258"]/main/div/div/div/div[3]/button[2]')
        notifications.click()
        sleep(10)

    def updatedSpans(self):
        # Make a request to the webpage and get the HTML content
        html_content = self.driver.page_source

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        bb = soup.find_all("div",{"class": "Expand Pos(a) D(f) Ov(h) Us(n) keen-slider"})

        # Find all the spans with class 'keen-slider__slide'
        return bb[1].find_all("span", {"class": "keen-slider__slide"})

    def autoLike(self):
        while(True):
            like = self.driver.find_element(By.XPATH, '//*[@id="Tinder"]/body')
            try:
                verified = self.driver.find_element(By.XPATH, '//*[@id="c964396036"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div/div[2]/div[3]/div/div/div/div/div[1]/div/div[2]')

                slides = self.updatedSpans()

                # Loop through each span and extract the image url
                for i in range(len(slides)):
                    image_div = slides[i].find("div", {"class": "StretchedBox"})
                    if image_div:
                        image_url = image_div['style'].split('background-image: url("')[1].split('");')[0]
                        req = urllib.request.urlopen(image_url)
                        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
                        img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
                        sleep(3)
                        slides = self.updatedSpans()

            except:
                like.send_keys(Keys.ARROW_LEFT)
                sleep(3)





bot = tinderBot()
bot.open()
