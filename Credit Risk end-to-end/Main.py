# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import kagglehub
import pandas as pd
import os

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