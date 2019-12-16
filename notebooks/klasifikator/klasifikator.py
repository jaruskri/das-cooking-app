
import keras
from keras.layers.core import Dense, Flatten
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.vgg16 import VGG16
from keras.models import Model
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing.image import load_img,img_to_array
from keras.models import model_from_json
import numpy as np
import os
import pandas as pd




def klasifikace(path):
    filename = "ingredients.txt"
    classes=[]
    with open(filename)  as f:
        classes = sorted(word.strip(",") for line in f for word in line.split())
    classes[classes.index('soy')]='soy sauce'
    classes[classes.index('bell')]='bell pepper'
    classes.remove(classes[classes.index('pepper')])
    classes.remove(classes[classes.index('sauce')])
    classes = classes
    im=load_img(path, target_size=(224, 224))
    im=img_to_array(im)
    im = im.reshape((1, im.shape[0], im.shape[1], im.shape[2]))
    prepared_images = preprocess_input(im)
    json_file = open('clf.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("model.h5")
    loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    predikce = loaded_model.predict(im).tolist()[0]
    threshold=1/52
    sorted_index = sorted(range(len(predikce)), key=lambda i: predikce[i])
    j=1
    output=[]
    while predikce[sorted_index[-j]]>threshold:
        output.append([classes[sorted_index[-j]], predikce[sorted_index[-j]]])
        j=j+1
    return output







