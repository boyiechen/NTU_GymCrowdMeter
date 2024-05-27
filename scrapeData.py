# packages
import json
import requests
import pandas as pd
import time
import datetime
import os
import sys
from config import weather_url 
from bs4 import BeautifulSoup

class Scraper:

    def __init__(self, weather_url = weather_url):
        self.url = 'https://rent.pe.ntu.edu.tw/'
        self.weather_url = weather_url
        self.count_dict = {}

    def getCrowdMeterDF(self):
        self.fetchCrowdMeterNow()
        self.fetchWeatherNow()

        # build dataframe
        tmp = pd.DataFrame.from_dict([self.count_dict])
        tmp = tmp.set_index("Timestamp")
        if tmp.shape[0] == 0:
            print("NO DATA, EXIT PROGRAM")
            sys.exit()

        return tmp

    def fetchCrowdMeterNow(self):
        res = requests.get(self.url)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        fitness_center = soup.find_all("div", class_="CMCItem")[0]
        swimming_pool = soup.find_all("div", class_="CMCItem")[1]

        current_count_fc = int(fitness_center.find_all("span")[0].text)
        optimal_count_fc = int(fitness_center.find_all("span")[1].text)
        max_count_fc = int(fitness_center.find_all("span")[2].text)

        current_count_sp = int(swimming_pool.find_all("span")[0].text)
        optimal_count_sp = int(swimming_pool.find_all("span")[1].text)
        max_count_sp = int(swimming_pool.find_all("span")[2].text)

        # build dictionary
        self.count_dict["current_count"] = current_count_fc
        # self.count_dict["optimal_count_fc"] = optimal_count_fc
        self.count_dict["capacity_fulll"] = max_count_fc
        self.count_dict["capacity_ratio"] = round(current_count_fc / max_count_fc, 4)
        self.count_dict["current_count_swim"] = current_count_sp
        # self.count_dict["optimal_count_sp"] = optimal_count_sp
        self.count_dict["capacity_full_swim"] = max_count_sp
        self.count_dict["Timestamp"] = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")

    def fetchWeatherNow(self):
        # attach weather info
        res = requests.get(self.weather_url)
        weather_res = res.json()
        self.count_dict["temp"] = weather_res["main"]["temp"]
        self.count_dict["temp_feel"] = weather_res["main"]["feels_like"]
        self.count_dict["temp_min"] = weather_res["main"]["temp_min"]
        self.count_dict["temp_max"] = weather_res["main"]["temp_max"]
        self.count_dict["pressure"] = weather_res["main"]["pressure"]
        self.count_dict["humidity"] = weather_res["main"]["humidity"]

