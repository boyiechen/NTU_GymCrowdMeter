#!/usr/bin/env python
# coding: utf-8
# 新體健身房人數即時推送及統計
# https://ntusportscenter.ntu.edu.tw/#/

# packages
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time
import datetime
import os
import calendar
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pyimgur

# import credentials
from config import CLIENT_ID, token, weather_url


# Set up working directory
cwd = os.getcwd()
base_path = cwd + "/"

# Set up timezone
os.environ['TZ'] = 'Asia/Taipei'
time.tzset()

# Web scraping
url = "https://ntusportscenter.ntu.edu.tw"

# Open Browser and open udn library #打開瀏覽器，但不要載入圖片
options = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values': {
        'images': 2,
        #'javascript': 2
    }
}
options.add_experimental_option('prefs', prefs)

## 偽裝header
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
options.add_argument('--user-agent=%s' % user_agent)
## 防止 javascript detect selenium
options.add_experimental_option('excludeSwitches', ['enable-automation'])
## headless
options.add_argument('-headless')

global driver
driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', chrome_options=options)


# 健身中心人數
# a dataframe with raw data
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'lxml')
count = soup.select("#home_index > div.allinbg > div.allin > div.condis > div > div > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)")[0].text

count_dict = {}
for c in count.split("\n"):
    c = c.strip()
    if len(c)==0:
        continue
    key = c.split("：")[0]
    value = int(c.split("：")[-1])
    count_dict[key] = value

current_count = count_dict["健身中心現在人數"]
capacity_full = count_dict["健身中心最大乘載人數"]

current_count_swim = count_dict["室內游泳池現在人數"]
capacity_full_swim = count_dict["室內游泳池最大乘載人數"]

# build dictionary
count_dict = {}
count_dict["current_count"] = current_count
count_dict["capacity_fulll"] = capacity_full
count_dict["capacity_ratio"] = current_count / capacity_full
count_dict["current_count_swim"] = current_count_swim
count_dict["capacity_full_swim"] = capacity_full_swim
count_dict["Timestamp"] = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")

# attach weather info
res = requests.get(weather_url)
weather_res = res.json()
count_dict["temp"] = weather_res["main"]["temp"]
count_dict["temp_feel"] = weather_res["main"]["feels_like"]
count_dict["temp_min"] = weather_res["main"]["temp_min"]
count_dict["temp_max"] = weather_res["main"]["temp_max"]
count_dict["pressure"] = weather_res["main"]["pressure"]
count_dict["humidity"] = weather_res["main"]["humidity"]
colnam = list(count_dict.keys())

# build dataframe
tmp = pd.DataFrame.from_dict([count_dict])
tmp = tmp.set_index("Timestamp")
tmp.to_csv(f"{base_path}NTU_GYM_Counter_tmp.csv")


## Loading Database and Updating
df = pd.read_csv(f"{base_path}NTU_GYM_Counter.csv", index_col="Timestamp")
df = df.append(tmp)
df = df.sort_values(by = "Timestamp", ascending = False)
# Saving
df.to_csv(f"{base_path}NTU_GYM_Counter.csv")

# Data Cleaning for better plot
df = pd.read_csv(f"{base_path}NTU_GYM_Counter.csv")

# Get the 15-minute time interval
# build a dictionary that indicates which time interval a row is in
time_interval_dict = {x : f"{x*15//60}:{x*15%60}" for x in range(0,97)}
def findTimeInterval(date): 
    t_hour = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M').hour
    t_minute = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M').minute
    t_HM = t_hour*60+t_minute
    return (t_HM//15)
# equivalent to column 1: date
df["TimeInterval"] = df.iloc[0:len(df),0].map(lambda x:findTimeInterval(x))

# Get week day from a given date
def findDay(date): 
    born = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M').weekday() 
    return (calendar.day_name[born])

date_text = df.iloc[0:len(df),0][0]
# equivalent to column 1: date
df["WeekDay"] = df.iloc[0:len(df),0].map(lambda x:findDay(x))

# 0-6: Mon.-Sun.
WeekDayToday = datetime.datetime.today().weekday()
WeekDayDict = {
    0 : "Monday",
    1 : "Tuesday",
    2 : "Wednesday",
    3 : "Thursday",
    4 : "Friday",
    5 : "Saturday",
    6 : "Sunday",
}
WeekDayDict[WeekDayToday]

# Filter the samples that match today's weekday
df_wk2day = df[df["WeekDay"] == WeekDayDict[WeekDayToday]]
df_wk2day = df_wk2day.groupby("TimeInterval").mean()

# preparing for plots
x = [time_interval_dict[key] for key in list(df_wk2day.index)]
y = df_wk2day['current_count']

tick_spacing = 8
fig, ax = plt.subplots(1,1)
ax.plot(x,y)
fig_save = plt.gcf()
ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
fig.savefig(f'{base_path}plot/plot.png')

# Line notify
def sendNotification(text = "", img_url = "", token = ""):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {"message": text,
              "imageFullsize" : img_url,
              "imageThumbnail": img_url}
    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=params)
    print(r.status_code)  #200
    print("發送Line通知囉！")
    time.sleep(1)

# Set up Imgur credentials
PATH = f"{base_path}plot/plot.png" #A Filepath to an image on your computer"
title = "Uploaded with PyImgur"

im = pyimgur.Imgur(CLIENT_ID)
uploaded_image = im.upload_image(PATH, title=title)
print(uploaded_image.title)
print(uploaded_image.link)
print(uploaded_image.type)

key = 'current_count'
sendNotification(text = f"\n台大新體健身房\n資料抓取時刻：\n{count_dict['Timestamp']}\n{key} : {count_dict[key]}人\n人數上限：{count_dict['capacity_fulll']}人\n容留比例：{count_dict['capacity_ratio']}\n現在氣溫：攝氏{count_dict['temp']}\n體感溫度：攝氏{count_dict['temp_feel']}\n現在濕度：{count_dict['humidity']}%\n現在氣壓：{count_dict['pressure']}帕", 
                 img_url = uploaded_image.link,
                 token = token)

driver.close()
