# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 17:25:19 2025

@author: DAYDREAMER
"""

import kagglehub

# Download latest version
path = kagglehub.dataset_download("gpiosenka/cards-image-datasetclassification")

print("Path to dataset files:", path)