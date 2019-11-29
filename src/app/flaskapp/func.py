from flaskapp import app
from PIL import Image
import os
import numpy as np

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def convert_image(filename, dir):
    try:
        im = Image.open(os.path.join(app.config['APP_PATH'], dir, filename))
    except:
        return False
    newfilename = os.path.splitext(filename)[0] + '.' + app.config['IMAGE_EXTENSION']
    if im.format == app.config['IMAGE_FORMAT']:
        im.close()
        os.rename(os.path.join(app.config['APP_PATH'], dir, filename), os.path.join(dir, newfilename))
        return newfilename
    else:
        im2 = im.convert('RGB')
        im.close()
        im2.save(os.path.join(app.config['APP_PATH'], dir, newfilename))
        os.remove(os.path.join(app.config['APP_PATH'], dir, filename))
        return newfilename

def recognize(filename):
    items = np.array(['apple', 'butter', 'oil', 'sugar', 'dog', 'pork', 'egg', 'tomato', 'beer', 'wine', 'onion', 'garlic'])
    weights = np.random.rand(len(items))
    threshold = 0.7
    i = weights > threshold
    weights = weights[i]
    weights = weights / np.sum(weights)
    items = items[i]
    return zip(list(items), list(weights))