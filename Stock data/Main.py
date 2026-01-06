#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  3 01:01:48 2025

@author: daydreamer
"""


import http.client
import json
from datetime import datetime
import time

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
    print("-_"*25)
    print(f"Fetching {Stock_name}")
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
    print(f"{Stock_name} fetch completed")
    print("-."*25)
    return name,price,sqldate,closing

## currently not used. keeping it here to test new stocks
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

'''
STEP1: 
    1. call this function to get the current data on all your watchlisted stocks
    2. data will be in trhe form of tupple inside a list
    ex:
        [(0,1,2,3),(0,1,2,3)]
'''

def updatePrices():
    SQ = []
    for w in WL:
        print(f"Stock {WL.index(w) + 1} / 10")
        n,p,d,c = getStockof(w[0],w[1])
        x = (n,p,d,c)
        SQ.append(x)
    return SQ





# establish connection
def connectDB():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        return conn
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None

'''
STEP2: 
    1. connect to DB using conn var
    2. Insert values and repeat
    3. commit and close when successful
'''

def InsertSQL():
    for stock in SQLpush:
        print("+-"*25)
            
        print(f"߷ Company name: {stock[0]}")
        print(f"߷ Price: {stock[1]}")
        print(f"߷ Date: {stock[2]}")
        print(f"߷ Closing price: {stock[3]}")
        
        conn = connectDB()
        if not conn:
            return False
        try:
            with conn.cursor() as cur:
                sql = """
                INSERT INTO stockprofile 
                (company, price, date, closingprice)
                VALUES (%s, %s, %s, %s)
                """
                cur.execute(sql, (stock[0], stock[1], stock[2], stock[3]))
                conn.commit()
                print("="*50)
                print(f"✅ Inserted {stock[0]} data")
                print("="*50)
        except Exception as e:
            print(f"❌ Insert failed: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()  


SQLpush = []

# running from DAG
def main():
    global SQLpush
    start_time = time.time()
    SQLpush = updatePrices()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"⏱️ Loop executed in {execution_time:.2f} seconds")
    
    start_time = time.time()
    InsertSQL()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"⏱️ Updated to SQL in {execution_time:.2f} seconds")
    
    