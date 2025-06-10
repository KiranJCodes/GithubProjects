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


# New 1b

relevant_year_cols = production.iloc[:, 2:-2].columns.tolist()

# Get the last 5 years
last_5_years_cols = relevant_year_cols[-5:]
    
    # Get the 5 years immediately preceding the last 5
previous_5_years_cols = relevant_year_cols[-10:-5]

print(f"\nLast 5 years columns: {last_5_years_cols}")
print(f"Previous 5 years columns: {previous_5_years_cols}")

    # --- Calculate the change in average production ---
production['Avg_Last_5_Years'] = production[last_5_years_cols].mean(axis=1)


production['Avg_Previous_5_Years'] = production[previous_5_years_cols].mean(axis=1)


production['Avg_Production_Change'] = production['Avg_Last_5_Years'] - production['Avg_Previous_5_Years']

    # --- Identify countries with increased and decreased production ---
increased_production = production[production['Avg_Production_Change'] > 0].sort_values('Avg_Production_Change', ascending=False)
decreased_production = production[production['Avg_Production_Change'] < 0].sort_values('Avg_Production_Change', ascending=True)

print("\n--- Top 5 Countries with Increased Average Production in Last 5 Years ---")
print(increased_production[['Country', 'Avg_Production_Change']].head(5))

print("\n--- Top 5 Countries with Decreased Average Production in Last 5 Years ---")
print(decreased_production[['Country', 'Avg_Production_Change']].head(5))


# --- Plotting the top 5 for each category ---

    # Plot for Increased Production
fig, axes = plt.subplots(1, 2, figsize=(18, 7), sharey=False)
sns.barplot(
        data=increased_production.head(5),
        x=increased_production['Avg_Production_Change'] / 1_000_000,
        y='Country',
        palette='Greens_d',
        ax=axes[0])
axes[0].set_title('Top 5 Countries with Increased Avg Production')
axes[0].set_xlabel('Change in Avg Production (Millions of Units)')
axes[0].set_ylabel('Country')


    # Plot for Decreased Production
plt.figure(figsize=(12, 6))
sns.barplot(
        data=decreased_production.head(5),
        x=decreased_production['Avg_Production_Change']/ 1_000_000,
        y='Country',
        palette='Reds_d',
        ax=axes[1]
    )
axes[1].set_title('Top 5 Countries with Decreased Avg Production')
axes[1].set_xlabel('Change in Avg Production (Millions of Units)')
axes[1].set_ylabel('Country')

plt.tight_layout()
plt.show()