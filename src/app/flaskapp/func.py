from flaskapp import app
from PIL import Image
import os
import numpy as np
import json

with open(os.path.join(app.config['UPLOAD_FOLDER'], 'full_format_recipes_excerpt.json')) as f:
    recipes = json.load(f)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def convert_image(filename, dir):
    try:
        im = Image.open(os.path.join(app.config['APP_PATH'], dir, filename))
    except:
        os.remove(os.path.join(app.config['APP_PATH'], dir, filename))
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
    items = np.array(['apple', 'butter', 'oil', 'sugar', 'dog', 'pork', 'egg', 'tomato', 'beer', 'wine', 'onion', 'garlic', 'ammonium sulfate', 'water', 'human', 'vinegar'])
    weights = np.random.rand(len(items))
    threshold = 0.7
    i = weights > threshold
    weights = weights[i]
    weights = weights / np.sum(weights)
    items = items[i]
    i = np.argsort(-weights)
    weights = weights[i]
    items = items[i]
    return (list(items), list(weights))

def listingredients():
    return ['apple', 'butter', 'oil', 'sugar', 'dog', 'pork', 'egg', 'tomato', 'beer', 'wine', 'onion', 'garlic', 'ammonium sulfate', 'water', 'human', 'vinegar']

def getRecipes(ingredients):
    i = np.random.randint(len(recipes), size=5)
    selectedRecipes = []
    for x in np.nditer(i):
        selectedRecipes.append(recipes[x])
    return selectedRecipes