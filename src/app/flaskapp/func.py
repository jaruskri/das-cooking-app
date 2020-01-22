from flaskapp import app
from PIL import Image
import os
import numpy as np
import json
from flask import g
import psycopg2
import psycopg2.extras

def get_db():
    if 'db' not in g:
        g.db = app.config['postgreSQL_pool'].getconn()
    return g.db

@app.teardown_appcontext
def close_conn(e):
    db = g.pop('db', None)
    if db is not None:
        app.config['postgreSQL_pool'].putconn(db)

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

# for testing purposes
def recognize(filename, threshold=0):
    #items = np.array(['apple', 'butter', 'oil', 'sugar', 'dog', 'pork', 'egg', 'tomato', 'beer', 'wine', 'onion', 'garlic', 'ammonium sulfate', 'water', 'human', 'vinegar'])
    items = listingredients()
    items = np.random.choice(items, 10)
    weights = np.random.exponential(1, len(items))
    i = np.argsort(-weights)
    weights = weights[i]
    items = items[i]
    weights = weights / np.sum(weights)
    i = weights > threshold
    weights = weights[i]
    items = items[i]
    return (list(items), list(weights), 'random')

def listingredients():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT nazev FROM ingredience_pref;")
    result = cursor.fetchall()
    cursor.close()
    return [x[0] for x in result]

def chooseRecipes(ingredients, categories=None, conditions=None, num=app.config['NUM_RECOMMENDED_RECIPES']):
    # dodatečné podmínky? řazení? vrátit jen id a title
    db = get_db()
    cursor = db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    sql1 = "INSERT INTO zvolene_kategorie(idk) VALUES ((SELECT kid FROM kategorie WHERE nazev = %s)) ON CONFLICT DO NOTHING"
    sql2 = "INSERT INTO zvolene_ingredience(idi) VALUES ((SELECT iid FROM ingredience_pref WHERE nazev = %s)) ON CONFLICT DO NOTHING"
    if 'polutry' in ingredients:
        ingredients.remove('polutry')
        ingredients.append('chicken')
        ingredients.append('turkey')
    if 'red meat' in ingredients:
        ingredients.remove('red meat')
        ingredients.append('pork')
        ingredients.append('beef')
    try:
        cursor.execute("DELETE FROM zvolene_kategorie")
        cursor.execute("DELETE FROM zvolene_ingredience")
        if categories is not None and len(categories) > 0: cursor.executemany(sql1, [[x] for x in categories])
        cursor.executemany(sql2, [[x] for x in ingredients])
        db.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        db.rollback()
        return None
    cursor.execute("SELECT * FROM navrzene_recepty ORDER BY "+app.config['RECIPES_ORDER_CRITERION']+" DESC LIMIT " + str(num))
    selectedRecipes = cursor.fetchall()
    selectedRecipes = [dict(x) for x in selectedRecipes]
    cursor.close()
    return selectedRecipes

def getRecipe(id):
    db = get_db()
    cursor = db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM recept WHERE rid="+str(id))
    result = cursor.fetchall()
    recipe = dict(result[0])
    recipe['date'] = recipe['date'].strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("SELECT text FROM ingredience WHERE idr="+str(id))
    result = cursor.fetchall()
    recipe['ingredients'] = [row['text'] for row in result]
    cursor.execute("SELECT text FROM postup WHERE idr="+str(id))
    result = cursor.fetchall()
    recipe['directions'] = [row['text'] for row in result]
    cursor.execute("SELECT nazev FROM kategorie_receptu WHERE idr="+str(id))
    result = cursor.fetchall()
    recipe['categories'] = [row['nazev'] for row in result]
    cursor.close()
    return recipe

def kategoriecetnosti(n=15):
    db = get_db()
    cursor = db.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT nazev as x, cetnost as value FROM cetnosti_kategorii ORDER BY cetnost DESC LIMIT "+str(n))
    result = cursor.fetchall()
    result = [dict(x) for x in result]
    return result