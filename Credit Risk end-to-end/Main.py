# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import kagglehub
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
try:
    # Download and get the path
    download_path = kagglehub.dataset_download("kabure/german-credit-data-with-risk")
    
    # Find the actual CSV file in the downloaded directory
    for file in os.listdir(download_path):
        if file.endswith('.csv'):
            file_path = os.path.join(download_path, file)
            df = pd.read_csv(file_path)
            break
    print(f"Dataset loaded from: {file_path}")
    
except Exception as e:
    print(f"Download failed: {e}")
    print("Please ensure you have Kaggle API credentials setup")
    
    
## Handle missing and duplicate values by deleting them
df.isna().sum()
df.duplicated().sum()

df = df.dropna().reset_index(drop=True)


## EDA now

df[['Age','Credit amount','Duration']].hist(bins=20,edgecolor='black')
plt.suptitle("Distrubution of Numerical values",fontsize=16)
plt.show

plt.figure(figsize=(15,5))
for i, col in enumerate(['Age','Credit amount','Duration']):
    plt.subplot(1, 3, i+1)
    sns.boxplot(y = df[col],color='gold')
    plt.title(col)
plt.tight_layout()
plt.show()


cols = ['Job','Housing','Saving accounts','Checking account','Purpose']
plt.figure(figsize=(15,10))
for i, col in enumerate(cols):
    plt.subplot(3,3,i+1)
    sns.countplot(data=df,x=col,palette='Set1',
                  order=df[col].value_counts().index)
    plt.title(f"Distrubution of {col}" )
    plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

## heatmap
corr = df[["Age","Job","Credit amount","Duration"]].corr()
sns.heatmap(corr, annot=True,cmap='coolwarm',fmt=".2f")
plt.show()


df.groupby('Job')['Credit amount'].mean()

df.groupby('Sex')['Credit amount'].mean()



## Make sure all are number format for ML models. 
df.dtypes
df['Sex'].value_counts()

## for sex 1 for male 0 for female
df['Sex'] = df['Sex'].map({'female': 0, 'male':1})
df['Sex'].value_counts()


## Housing 1 own 2 rent 0 free
df['Housing'].value_counts()
df['Housing'] = df['Housing'].map({'own':1,
                                   'rent':2,
                                   'free':0})

## Saving accounts rich 0 qtr - 1 - mod - 2 - little - 3
df['Saving accounts'].value_counts()
df['Saving accounts'] = df['Saving accounts'].map({'rich':0,
                                                   'quite rich':1,
                                                   'moderate':2,
                                                   'little':3})

## Checking account 
df['Checking account'].value_counts()
df['Checking account'] = df['Checking account'].map({'rich':0,
                                                   'moderate':1,
                                                   'little':2})


## Purpose
df['Purpose'].value_counts()
