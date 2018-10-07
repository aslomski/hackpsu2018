# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 13:01:08 2018

@author: arslo
"""

import boto3
import json
import quandl
import requests
from datetime import timedelta, date
import time
import pickle

ticker = "AMZN"

with open(ticker + '_modified', 'rb') as input:
    df = pickle.load(input)

print df.iloc[0]

end_dt = date(2018, 3, 23)
enddate = end_dt.strftime("%Y-%m-%d")
print(df.loc[enddate])