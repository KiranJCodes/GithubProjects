# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 17:25:19 2025

@author: DAYDREAMER
"""

import kagglehub
import pandas as pd
import tensorflow as tf 
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_class_weight

# Download latest version
path = kagglehub.dataset_download("gpiosenka/cards-image-datasetclassification")

print("Path to dataset files:", path)

data = pd.read_csv(path+r"/cards.csv")
data['filepaths'] = data['filepaths'].str.replace(r'/', r'\\', regex=True)
data = data[data['filepaths'].str.contains('.jpg', case=False, regex=False)]

le = LabelEncoder()
le.fit(data['labels'])
# Create TensorFlow dataset from DataFrame  


def load_and_preprocess(fpath, label):
    
    fpath = tf.strings.regex_replace(fpath, '/', '\\')
    full_path = tf.strings.join([path, '\\', fpath])
    
    img = tf.io.read_file(full_path)  
    img = tf.image.decode_jpeg(img, channels=3)  
    img = tf.image.resize(img, [224, 224])
    img = img / 255.0  # Normalization
    return img, label

# Filter train data




def Filterdata(DS, subset):
    Filtered = DS[DS['data set'] == subset].copy()
    Filtered['label_encoded'] = le.transform(Filtered['labels'])  
    return Filtered

traindata = Filterdata(data, 'train')
validata = Filterdata(data, 'valid')



def create_ds(df, shuffle=True):
    ds = tf.data.Dataset.from_tensor_slices(
        (df['filepaths'].values, df['label_encoded'].values))
    ds = ds.map(load_and_preprocess, num_parallel_calls=tf.data.AUTOTUNE)
    if shuffle:
        ds = ds.shuffle(buffer_size=500)  # Reduced from 1000
    ds = ds.batch(32)
    ds = ds.prefetch(2)  # Smaller prefetch for CPU
    return ds

trainds = create_ds(traindata)
valds = create_ds(validata, shuffle=False)

for images, labels in trainds.take(1):
    print(images.shape, labels.shape)  # Should print (batch_size, 224, 224, 3) and (batch_size,)
    
    
num_classes = len(le.classes_)    


base_model = tf.keras.applications.MobileNetV2(
    input_shape=(128, 128, 3),
    include_top=False,
    weights='imagenet',
    alpha=0.35  # Extra-lightweight (35% of original size)
)
base_model.trainable = False  # Freeze pretrained layers

model = tf.keras.Sequential([
    tf.keras.layers.Rescaling(1./127.5, offset=-1),  # MobileNet expects [-1,1]
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])


model.compile(
    optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.001),  # Better for CPU
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=8),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_accuracy', 
        factor=0.5, 
        patience=3,
        min_lr=1e-6),
    tf.keras.callbacks.ModelCheckpoint(
        'best_model.h5',
        save_best_only=True,
        monitor='val_accuracy')
]


# Run before training
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

model.build((None, 224, 224, 3))
model.summary()


class_weights = compute_class_weight('balanced', 
                                   classes=np.unique(traindata['label_encoded']),
                                   y=traindata['label_encoded'])
class_weights = dict(enumerate(class_weights))

history = model.fit(
    trainds,
    epochs=50,  # Let early stopping handle this
    validation_data=valds,
    callbacks=callbacks,
    class_weight=class_weights
)

# Check your data loading
for images, labels in trainds.take(1):
    print("Image stats - Min:", tf.reduce_min(images).numpy(), 
          "Max:", tf.reduce_max(images).numpy(), 
          "Mean:", tf.reduce_mean(images).numpy())
    print("Unique labels:", np.unique(labels.numpy()))
    
    # Check ALL labels in training set
print("Label counts:\n", traindata['label_encoded'].value_counts())

print("Unique labels in CSV:", traindata['label_encoded'].unique())