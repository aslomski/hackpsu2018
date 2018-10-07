# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 17:22:39 2018

@author: arslo
"""

import boto3
import quandl
import requests
from datetime import timedelta, date
import time
import pickle

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

#config
comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
quandl.ApiConfig.api_key = '7nvCPUhM6GxdVSHQn3Bg'
ticker = "AMZN"
start_dt = date(2017, 11, 22)
end_dt = date(2018, 3, 23)


#pull stock data
df = quandl.get("WIKI/" + ticker) 


startdate = start_dt.strftime("%Y-%m-%d")
firstloc = df.index.get_loc(startdate)
df.drop(df.index[:(firstloc)], inplace=True)
df.drop(columns=['Volume', 'Ex-Dividend', 'Split Ratio', 'Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume'])

print(df.iloc[0])

#loop through each date
counter = 0
for dt in daterange(start_dt, end_dt):
    date = dt.strftime("%Y-%m-%d")
    if date in df.index:
        #this is to avoid api limits(255 requests every 15 mins)
        if counter > 250:
            #sleep for 15 mins dt.strftime("%Y-%m-%d")
            time.sleep(960)
            counter = 0
        response = requests.get("https://api.newsriver.io/v2/search?query=text%3A(%22" + ticker + "%22)%20AND%20discoverDate%3A%5B" + date + "%20TO%20" + date + "%5D&sortBy=_score&sortOrder=DESC&limit=15", headers={"Authorization":"sBBqsGXiYgF0Db5OV5tAw4c7JaSN3tI12pcxXQAfaOE_cpRKlyKxz2801D099mVpn2pHZrSf1gT2PUujH1YaQA"})
        jsonFile = response.json()
        text = jsonFile[0].get('text')
        text = text[:4700]
        #comprehendResponse = comprehend.detect_sentiment(Text=text, LanguageCode='en')
        #respJSON = comprehendResponse.json()
        respJSON = comprehend.detect_sentiment(Text=text, LanguageCode='en')
        neutral = respJSON["SentimentScore"]["Neutral"]
        positive = respJSON["SentimentScore"]["Positive"]
        negative = respJSON["SentimentScore"]["Negative"]
        mixed = respJSON["SentimentScore"]["Mixed"]
        df.loc[date, "Neutral"] = neutral
        df.loc[date, "Positive"] = positive
        df.loc[date, "Negative"] = negative
        df.loc[date, "Mixed"] = mixed
        print(df.loc[date])
        print("\n")
                

with open(ticker + "_modified", 'wb') as output:  # Overwrites any existing file.
        pickle.dump(df, output, pickle.HIGHEST_PROTOCOL)

print("Output File to " + ticker + "_modified")

 
  

  

  

  
