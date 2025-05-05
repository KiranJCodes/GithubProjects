# -*- coding: utf-8 -*-
"""
Created on Sun May  4 17:55:35 2025

@author: DAYDREAMER
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load datasets
production = pd.read_csv("Coffee_production.csv")
exports = pd.read_csv("Coffee_export.csv")
Inventories = pd.read_csv("Coffee_green_coffee_inventorie.csv")
Imports = pd.read_csv("Coffee_import.csv")
DomConsumption = pd.read_csv("Coffee_domestic_consumption.csv")
IntConsumption = pd.read_csv("Coffee_importers_consumption.csv")


# TASK 1 Find top proucers of coffee and the top ones in the last 10 years
# 1a

## Cut to top 10 and sort
Sorttotal = production.sort_values("Total_production",ascending=False).head(10)

## Additionally convert the huge number in billions for easier viewving 
## Plot
plt.figure(figsize=(12,6))
sns.barplot(data=Sorttotal,
            x=Sorttotal['Total_production'] / 1_000_000_000,
            y='Country', palette='viridis')
plt.title('Top 10 Coffee Producers (All-Time)')
plt.xlabel('Total Production (units in Billions)')
plt.ylabel('Country')
plt.show()

# 1b

last10years = production.iloc[0:,-12:-2]
last10years = production[['Country'] + list(last10years)] 

top10latest = last10years.groupby('Country').sum().sum(axis=1)
top10latest = top10latest.sort_values(ascending=False).head(10)
top10latest = top10latest.reset_index(name='total_production_recent')


plt.figure(figsize=(12,6))
sns.barplot(x=top10latest['total_production_recent'] / 1_000_000_000,
            y=top10latest["Country"], palette='viridis')
plt.title('Top 10 Coffee Producers (Last 10 years)')
plt.xlabel('Total Production (units in Billions)')
plt.ylabel('Country')
plt.show()

## see gainers and loosers 

combined = pd.merge(
    Sorttotal.reset_index(), 
    top10latest.reset_index(), 
    on='Country', 
    suffixes=('_alltime', '_recent')
)


combined['change'] = combined['total_production_recent'] - combined['Total_production']
combined['pct_change'] = (combined['change'] / combined['Total_production']) * 100

top_gainers = combined.sort_values('change', ascending=False).head(5)

top_losers = combined.sort_values('change').head(5)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Top Gainers
sns.barplot(data=top_gainers, x='change', y='Country', ax=ax1, palette='Greens')
ax1.set_title('Top 5 Gainers (Recent vs All-Time)')
ax1.set_xlabel('Production Increase (kg)')

# Top Losers
sns.barplot(data=top_losers, x='change', y='Country', ax=ax2, palette='Reds')
ax2.set_title('Top 5 Losers (Recent vs All-Time)')
ax2.set_xlabel('Production Decrease (kg)')

plt.tight_layout()
plt.show()


## end of task1 