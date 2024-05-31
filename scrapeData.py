# packages
import json
import requests
import pandas as pd
import time
import datetime
import os
import sys
from config import weather_url 

class scraper(object):

    def __init__(self, weather_url = weather_url):
        self.url = 'https://ntusportscenter.ntu.edu.tw/counter.txt'
        self.weather_url = weather_url
        self.count_dict = {}
        
    def getCrowdMeterDF(self):
        self.fetchCrowdMeterNow()
        self.fetchWeatherNow()

        # build dataframe
        tmp = pd.DataFrame.from_dict([self.count_dict])
        tmp = tmp.set_index("Timestamp")
        # tmp.to_csv(f"{base_path}/RSF_tmp.csv")
        if tmp.shape[0] == 0:
            print("NO DATA, EXIT PROGRAM")
            sys.exit()

        return tmp

    def fetchCrowdMeterNow(self):
        res = requests.get(self.url)
        print(res)
        count_dict = json.loads(res.text)
        count_dict = count_dict["CounterData"][0]
        current_count = int(count_dict['innerCount'].split(";")[0])
        current_count_swim = int(count_dict['innerCount'].split(";")[1])
        capacity_full = int(count_dict['permitNum'].split(";")[0])
        capacity_full_swim = int(count_dict['permitNum'].split(";")[1])

        # build dictionary
        self.count_dict["current_count"] = current_count
        self.count_dict["capacity_fulll"] = capacity_full
        self.count_dict["capacity_ratio"] = round(current_count / capacity_full, 4)
        self.count_dict["current_count_swim"] = current_count_swim
        self.count_dict["capacity_full_swim"] = capacity_full_swim
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
