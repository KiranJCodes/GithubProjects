#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  3 01:01:48 2025

@author: daydreamer
"""
'''
import requests
import pandas as pd


baseurl = 'https://stock.indianapi.in'

apikey = 'St0cksAp!'

headers = {
    "accept": "application/json",
    "X-API-Key": apikey
}

symbol = "TCS"
quote_url = f"{baseurl}/stock/quote/{symbol}"
quote_response = requests.get(quote_url, headers=headers)
quote_data = quote_response.json()
        
'''

import http.client
import json
from datetime import datetime


import os
from dotenv import load_dotenv

load_dotenv() 
apikey = os.getenv('API_KEY')




def getStockof(Stock_name,market):
    conn = http.client.HTTPSConnection("stock.indianapi.in")
    headers = { 'X-Api-Key': "sk-live-6ZxoAaoKaXIXhLxOUyajwFsOylISnlTgZkaiKFhO" }
    conn.request("GET", "/stock?name="+Stock_name, headers=headers)

    res = conn.getresponse()
    data = res.read()

    filterdata = json.loads(data.decode('utf-8'))

    #name of the company 
    name = filterdata['companyName']
    
    # Current price
    price = filterdata['currentPrice'][market]

    # date
    date = filterdata['stockDetailsReusableData']['date']
    sqldate = datetime.strptime(date, '%d %b %Y').strftime('%Y-%m-%d')
    print(f"DATE: {sqldate}")
    
    #closing price
    closing= filterdata['stockDetailsReusableData']['close']
    
    return name,price,sqldate,closing

n,p,d,c = getStockof("APEX", "NSE")