# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 17:25:19 2025

@author: DAYDREAMER
"""

import kagglehub
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf 
# Download latest version
path = kagglehub.dataset_download("gpiosenka/cards-image-datasetclassification")

print("Path to dataset files:", path)

data = pd.read_csv(path+r"/cards.csv")

le = LabelEncoder()
# Create TensorFlow dataset from DataFrame  
def load_and_preprocess(fpath, label): 
    fpath = path+"\\"+fpath
    fpath.replace("/","\\",-1)
    print(fpath)
    
    img = tf.io.read_file(fpath)  
    img = tf.image.decode_jpeg(img, channels=3)  
    img = tf.image.resize(img, [224, 224])  # Resize for CNNs  
    return img, label

# Filter train data

check = load_and_preprocess(r"train/ace of clubs/001.jpg","ace of clubs")
x= check[-1]
x.replace("/","\\",-1)

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
    tf.keras.layers.Rescaling(1./255),  # Normalize pixel values
    tf.keras.layers.Conv2D(32, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(num_classes)  
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


sample_batch = next(iter(trainds))
print("Image batch shape:", sample_batch[0].shape)
print("Image dtype:", sample_batch[0].dtype)
print("Label batch shape:", sample_batch[1].shape)
print("Label dtype:", sample_batch[1].dtype)