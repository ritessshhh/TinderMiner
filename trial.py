from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import re
import urllib.request
import numpy as np
import cv2
from bs4 import BeautifulSoup
import tensorflow as tf
import requests
import json

class CNNModel:
    def __init__(self):
        self.weights = np.random.rand(224, 224, 3)

    def predict(self, image):
        processed_image = cv2.resize(image, (224, 224)) / 255.0
        score = np.dot(processed_image.flatten(), self.weights.flatten())
        return score > 0.5

class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.cnn_model = CNNModel()
    
    def open(self):
        self.driver.get("https://www.tinder.com")
        sleep(10)

        login = self.driver.find_element(By.XPATH, '//*[@id="o-1868991261"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a/div[2]/div[2]')
        login.click()
        sleep(5)
        
        self.autoLike()

    def updatedSpans(self):
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        bb = soup.find_all("div", {"class": "Expand Pos(a) D(f) Ov(h) Us(n) keen-slider"})
        return bb[1].find_all("span", {"class": "keen-slider__slide"})

    def autoLike(self):
        while True:
            like = self.driver.find_element(By.XPATH, '//*[@id="Tinder"]/body')
            try:
                slides = self.updatedSpans()
                for i in range(len(slides)):
                    image_div = slides[i].find("div", {"class": "StretchedBox"})
                    if image_div:
                        image_url = image_div['style'].split('background-image: url("')[1].split('");')[0]
                        req = urllib.request.urlopen(image_url)
                        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
                        img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
                        
                        if self.cnn_model.predict(img):
                            like.send_keys(Keys.ARROW_RIGHT)
                            sleep(3)
                            if self.checkMatch():
                                self.sendRizzMessage()
                                self.scheduleDate()
                        else:
                            like.send_keys(Keys.ARROW_LEFT)
                        sleep(3)
            except:
                like.send_keys(Keys.ARROW_LEFT)
                sleep(3)
    
    def checkMatch(self):
        try:
            match_popup = self.driver.find_element(By.XPATH, '//*[@id="match-popup"]')
            return True if match_popup else False
        except:
            return False

    def sendRizzMessage(self):
        prompt = "Generate a fun, flirty, and engaging opening line for a Tinder match."
        headers = {"Authorization": "Bearer YOUR_OPENAI_API_KEY", "Content-Type": "application/json"}
        data = {"model": "gpt-4", "messages": [{"role": "user", "content": prompt}]}
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        rizz_message = response.json()["choices"][0]["message"]["content"]

        chat_box = self.driver.find_element(By.XPATH, '//*[@id="chat-box"]')
        chat_box.send_keys(rizz_message)
        chat_box.send_keys(Keys.RETURN)

    def scheduleDate(self):
        headers = {"Authorization": "Bearer YOUR_CAL_COM_API_KEY", "Content-Type": "application/json"}
        check_conflicts = requests.get("https://api.cal.com/v1/availability", headers=headers).json()
        available_slot = None
        for slot in check_conflicts["available_times"]:
            if slot["start"] and slot["end"]:
                available_slot = slot
                break
        if available_slot:
            data = {
                "eventType": "tinder-date",
                "email": "match@example.com",
                "startTime": available_slot["start"],
                "endTime": available_slot["end"]
            }
            response = requests.post("https://api.cal.com/v1/schedule", headers=headers, json=data)
            print("Scheduled date:", response.json())

bot = TinderBot()
bot.open()
