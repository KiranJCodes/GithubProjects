# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 17:25:19 2025

@author: DAYDREAMER
"""

import kagglehub
import pandas as pd

import tensorflow as tf 
# Download latest version
path = kagglehub.dataset_download("gpiosenka/cards-image-datasetclassification")

print("Path to dataset files:", path)

data = pd.read_csv(path+r"/cards.csv")


# Create TensorFlow dataset from DataFrame  
def load_and_preprocess(fpath, label): 
    fpath = path+"\\"+fpath
    print(fpath)
    
    img = tf.io.read_file(fpath)  
    img = tf.image.decode_jpeg(img, channels=3)  
    img = tf.image.resize(img, [224, 224])  # Resize for CNNs  
    return img, label  

# Filter train data
traindata = data[data['data set'] == 'train']

# Convert to TensorFlow Dataset
trainds = tf.data.Dataset.from_tensor_slices(
    (traindata['filepaths'].values, traindata['labels'].values)  # Adjust column names
).map(load_and_preprocess).batch(32).prefetch(tf.data.AUTOTUNE)

for images, labels in trainds.take(1):
    print(images.shape, labels.shape)  # Should print (batch_size, 224, 224, 3) and (batch_size,)