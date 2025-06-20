# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 17:25:19 2025

@author: DAYDREAMER
"""

import kagglehub
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf 
import numpy as np

# Download latest version
path = kagglehub.dataset_download("gpiosenka/cards-image-datasetclassification")

print("Path to dataset files:", path)

data = pd.read_csv(path+r"/cards.csv")
data['filepaths'] = data['filepaths'].str.replace(r'/', r'\\', regex=True)
data = data[data['filepaths'].str.contains('.jpg', case=False, regex=False)]

le = LabelEncoder()
# Create TensorFlow dataset from DataFrame  
def load_and_preprocess(fpath, label): 
    fpath = path + "\\" + fpath
    img = tf.io.read_file(fpath)  
    img = tf.image.decode_jpeg(img, channels=3)  
    img = tf.image.resize(img, [224, 224])  # Resize for CNNs  
    img = img / 255.0
    return img, label

# Filter train data


# Debug location!
check = load_and_preprocess("train/ace of clubs/001.jpg","ace of clubs")
x= check
# end of degub

def Filterdata(DS,subset):
    Filtered = DS[DS['data set']== subset]
    Filtered['label_encoded'] = le.fit_transform(Filtered['labels'])
    
    return Filtered

traindata = Filterdata(data, 'train')
validata = Filterdata(data, 'valid')



def ConvertTensor(Dataset):
    ConvertedDS = tf.data.Dataset.from_tensor_slices(
        (Dataset['filepaths'].values, Dataset['label_encoded'].values)  
    ).map(load_and_preprocess).batch(32).prefetch(tf.data.AUTOTUNE)
    
    return ConvertedDS

trainds = ConvertTensor(traindata)
valds = ConvertTensor(validata)

for images, labels in trainds.take(1):
    print(images.shape, labels.shape)  # Should print (batch_size, 224, 224, 3) and (batch_size,)
    
    
num_classes = len(le.classes_)    


model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(224, 224, 3)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
    )

history = model.fit(
    trainds,
    epochs=10,  # Start with 10 epochs, adjust later
    validation_data=valds  # Use your validation dataset
)


# Check your data loading
for images, labels in trainds.take(1):
    print("Image stats - Min:", tf.reduce_min(images).numpy(), 
          "Max:", tf.reduce_max(images).numpy(), 
          "Mean:", tf.reduce_mean(images).numpy())
    print("Unique labels:", np.unique(labels.numpy()))
    
    # Check ALL labels in training set
print("Label counts:\n", traindata['label_encoded'].value_counts())