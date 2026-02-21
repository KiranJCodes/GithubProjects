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
Imports = pd.read_csv("Coffee_import.csv")



    

# TASK 1 Find top proucers of coffee 
def ShowTopten(df,colname):
    if "production" in colname:
        titlename = "Producers"
        colname = "Total_production"
    else:
        titlename = "Importers"
        colname = "Total_import"
    Sorttotal = df.sort_values(colname,ascending=False).head(10)
    for i in range(10):
        print(f"Country: {Sorttotal['Country'].iloc[i:i+1]} | {Sorttotal[colname].iloc[i:i+1] / 1_000_000_000} ")
    ## Additionally convert the huge number in billions for easier viewving 
    plt.figure(figsize=(12,6))
    sns.barplot(data=Sorttotal,
                x=Sorttotal[colname] / 1_000_000_000,
                y='Country', palette='viridis')
    
    plt.title(f'Top 10 Coffee {titlename} (All-Time)')
    plt.xlabel('Total Production (units in Billions)')
    plt.ylabel('Country')
    plt.show()
    
    
# 1a
ShowTopten(production, "Total_production")


## Cut to top 10 and sort
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
        ax=axes[1])
axes[1].set_title('Top 5 Countries with Increased Avg Production')
axes[1].set_xlabel('Change in Avg Production (Millions of Units)')
axes[1].set_ylabel('Country')


    # Plot for Decreased Production
plt.figure(figsize=(12, 6))
sns.barplot(
        data=decreased_production.head(5),
        x=decreased_production['Avg_Production_Change']/ 1_000_000,
        y='Country',
        palette='Reds_d',
        ax=axes[0]
    )
axes[0].set_title('Top 5 Countries with Decreased Avg Production')
axes[0].set_xlabel('Change in Avg Production (Millions of Units)')
axes[0].set_ylabel('Country')

plt.tight_layout()
plt.show()


# TASK 2 Find top Importers of coffee 

ShowTopten(Imports, "Total_import")


## Cut to top 10
Imports.columns
relevant_year_cols = Imports.iloc[:, 1:-2].columns.tolist()

# Get the last 5 years
last_5_years_cols = relevant_year_cols[-5:]
    
    # Get the 5 years immediately preceding the last 5
previous_5_years_cols = relevant_year_cols[-10:-5]

print(f"\nLast 5 years columns: {last_5_years_cols}")
print(f"Previous 5 years columns: {previous_5_years_cols}")

    # --- Calculate the change in average production ---
Imports['Avg_Last_5_Years'] = Imports[last_5_years_cols].mean(axis=1)


Imports['Avg_Previous_5_Years'] = Imports[previous_5_years_cols].mean(axis=1)


Imports['Avg_import_Change'] = Imports['Avg_Last_5_Years'] - Imports['Avg_Previous_5_Years']

    # --- Identify countries with increased and decreased production ---
increased_imports = Imports[Imports['Avg_import_Change'] > 0].sort_values('Avg_import_Change', ascending=False)

print("\n--- Top 5 Countries with Increased Average Imports in Last 5 Years ---")
print(increased_imports[['Country', 'Avg_import_Change']].head(5))

print("\n--- Top 5 Countries with Decreased Average Imports in Last 5 Years ---")
print(increased_imports[['Country', 'Avg_import_Change']].tail(5))


# --- Plotting the top 5 for each category ---

    # Plot for Increased Production
fig, axes = plt.subplots(1, 2, figsize=(18, 7), sharey=False)
sns.barplot(
        data=increased_imports.head(5),
        x=increased_imports['Avg_import_Change'] / 1_000_000,
        y='Country',
        palette='Greens_d',
        ax=axes[1])
axes[1].set_title('Top 5 Countries with Increased Avg Imports')
axes[1].set_xlabel('Change in Avg Production (Millions of Units)')
axes[1].set_ylabel('Country')


    # Plot for Decreased Production
plt.figure(figsize=(12, 6))
sns.barplot(
        data=increased_imports.tail(5),
        x=increased_imports['Avg_import_Change']/ 1_000_000,
        y='Country',
        palette='Reds_d',
        ax=axes[0]
    )
axes[0].set_title('Top 5 Countries with Decreased Avg Imports')
axes[0].set_xlabel('Change in Avg Production (Millions of Units)')
axes[0].set_ylabel('Country')

plt.tight_layout()
plt.show()