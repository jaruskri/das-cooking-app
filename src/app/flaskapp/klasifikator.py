from keras.preprocessing.image import load_img,img_to_array
from keras.models import model_from_json
from keras.applications.vgg16 import preprocess_input
import numpy as np

filename = "ingredients.txt"
with open(filename)  as f:
    classes = sorted(line.strip() for line in f)
    
with open("clf.json") as f:
    loaded_model_json = f.read()
    
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("model.h5")
loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

def klasifikace(path, threshold=0):        
    im = load_img(path, target_size=(224, 224))
    im = img_to_array(im)
    im = im.reshape((1, im.shape[0], im.shape[1], im.shape[2]))
    im = preprocess_input(im)

    weights = loaded_model.predict(im).flatten()
    sorted_index = np.argsort(-weights)
    weights = weights[sorted_index]
    sorted_classes = np.array(classes)[sorted_index]
    i = weights > threshold
    weights = weights[i].astype('float64')
    sorted_classes = sorted_classes[i]
    return (list(sorted_classes), list(weights), 'cnn1')