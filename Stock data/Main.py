#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  3 01:01:48 2025

@author: daydreamer
"""


import http.client
import json
from datetime import datetime


import os
from dotenv import load_dotenv

import psycopg2

load_dotenv() 
apikey = os.getenv('API_KEY')

'''

https://indianapi.in/indian-stock-market
'''

def getStockof(Stock_name,market):
    conn = http.client.HTTPSConnection("stock.indianapi.in")
    headers = { 'X-Api-Key': apikey }
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

    
    #closing price
    closing= filterdata['stockDetailsReusableData']['close']
    
    return name,price,sqldate,closing

def test():
    
    n,p,d,c = getStockof("RBLBANK","NSE")
    print(f"Company name: {n}")
    print(f"price: {p}")
    print(f"Date: {d}")
    print(f"Closing price: {c}")


## create 10 watchlists

WL = [ ("APEX", "NSE"), ("SUZLON", "NSE"),
            ("CANBK","NSE"), ("TATASTEEL",'NSE'),
            ("BHEL","NSE"), ("ENGINERSIN","NSE"),
            ("RBLBANK","NSE"),("WIPRO","NSE"),
            ("ETERNAL","NSE"),("WELSPUNLIV","NSE")
            ]


## Get listed details for every watchlist stock 
def updatePrices():
    SQ = []
    for w in WL:
    
        n,p,d,c = getStockof(w[0],w[1])
        x = (n,p,d,c)
        SQLpush.append(x)
    return SQ

SQLpush = updatePrices()  


for stock in SQLpush:
    print("+-"*25)
        
    print(f"Company name: {stock[0]}")
    print(f"price: {stock[1]}")
    print(f"Date: {stock[2]}")
    print(f"Closing price: {stock[3]}")


# establish connection

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)