# -*- coding: utf-8 -*-
"""Covid-19 Chest X_rays CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gP9uVWBGtZeWnt_o8F7Zn70oyaXrLOGL
"""

import os
os.environ['KAGGLE_USERNAME']="KAGGLE_USERNAME"
os.environ['KAGGLE_KEY']="KAGGLE_KEY"
!kaggle datasets download  tawsifurrahman/covid19-radiography-database

!unzip covid19-radiography-database.zip

print(len(os.listdir('COVID-19_Radiography_Dataset/COVID/images')))
len(os.listdir('COVID-19_Radiography_Dataset/Normal/images'))

import cv2

img=cv2.imread('COVID-19_Radiography_Dataset/COVID/images/COVID-10.png')

import matplotlib.pyplot as plt
plt.imshow(img)

img.shape

import numpy as np

import pandas as pd
urls=os.listdir('COVID-19_Radiography_Dataset/COVID/images')
path="COVID-19_Radiography_Dataset/COVID/images" + urls[0]
path

def load_images(path, urls, target):
    images = []
    labels = []

    for i in range(min(3616, len(urls))):
        img_path = os.path.join(path, urls[i])
        img = cv2.imread(img_path)
        img = img / 255.0
        img = cv2.resize(img, (80, 80))
        images.append(img)
        labels.append(target)

    images = np.asarray(images)
    return images, labels

from tensorflow.keras.preprocessing.image import ImageDataGenerator
datagen = ImageDataGenerator(
   # rescale=1.0 / 255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

covid_path="COVID-19_Radiography_Dataset/COVID/images"
covid_url=os.listdir(covid_path)
covidimages , covidtargets = load_images(covid_path, covid_url, 1)
print(len(covid_url))
len(covidimages)

normal_path="COVID-19_Radiography_Dataset/Normal/images"
normal_url=os.listdir(normal_path)
normal_images , normal_targets = load_images(normal_path, normal_url, 0)

print(covidimages.shape)
normal_images.shape

#now merging the normal and covid images
data=np.r_[covidimages , normal_images]
targets=np.r_[covidtargets, normal_targets]
print(data.shape)
targets.shape

from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense,Dropout
from tensorflow.keras.losses import BinaryCrossentropy

x_train , x_test , y_train, y_test =train_test_split (data, targets, test_size=0.2)

model= Sequential(
    [
        Conv2D(64,(3,3),input_shape=(80,80,3),activation='relu'),
        MaxPooling2D(),
        Conv2D(64 , (3,3), activation='relu'),
        MaxPooling2D(),
        Conv2D(128 , (3,3), activation='relu'),
        MaxPooling2D(),
        Flatten(),
        Dense(512,activation='relu'),
        Dense(256,activation='relu'),
        Dropout(0.5),
        Dense(1,activation='sigmoid')
    ]
)

model.summary()

model.compile(optimizer='adam', loss='BinaryCrossentropy', metrics=['accuracy'])

model.fit(x_train, y_train, batch_size=32, epochs=15, validation_data=(x_test, y_test))

plt.plot(model.history.history['accuracy'], label='train_Accuracy')
plt.plot(model.history.history['val_accuracy'], label='test_Accuracy')
plt.legend()
plt.show()

plt.plot(model.history.history['loss'], label='train_loss')
plt.plot(model.history.history['val_loss'], label='test_loss')
plt.legend()
plt.show()

#model.save('covid19_xray_cnn_model.h5')

#oaded_model = tf.keras.models.load_model('covid19_xray_cnn_model.h5')
#loaded_model