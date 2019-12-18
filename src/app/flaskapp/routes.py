from flask import render_template, make_response, request, session, flash, send_from_directory, redirect, url_for
from flaskapp import app
from flaskapp.forms import LoginForm
from flaskapp.func import allowed_file, convert_image, recognize, listingredients, chooseRecipes, get_db, getRecipe, kategoriecetnosti
import json
import os
import time
from flaskapp.klasifikator import klasifikace

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        if request.form.get('password') == app.config['PASSWORD']:
            session['logged'] = True
            flash("User logged in.")
        else:
            flash("Wrong password.")
    if session.get('logged'):
        return render_template('upload.html')
    return render_template('login.html', form=form)

@app.route('/upload', methods=['POST'])
def upload():
    if not session.get('logged'):
        return redirect(url_for('index'))
    if 'photos' not in request.files:
        return '[]'
    files = request.files.getlist('photos')
    names = []
    for file in files:
        if file.filename == '':
            continue
        if file and allowed_file(file.filename):
            newfilename = (str(round(time.time()*1000)) + '_' + file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], newfilename))
            newfilename = convert_image(newfilename, app.config['UPLOAD_FOLDER'])
            if newfilename == False: continue
            estimation, estimationWeights, method = klasifikace(app.config['UPLOAD_FOLDER']+'/'+newfilename, threshold=app.config['CLASSIFICATION_THRESHOLD'])
            names.append({'filename': newfilename, 'estimation': estimation, 'estimationWeights': estimationWeights, 'estimationMethod': method, 'selection': estimation[0], 'selectionMethod': 'auto'})
    uploaded = session.get('uploaded') or []
    uploaded.extend(names)
    session['uploaded'] = uploaded
    return json.dumps(names)

@app.route('/ingredientslist')
def ingredientslist():
    if not session.get('logged'):
        return redirect(url_for('index'))
    return json.dumps(listingredients())

@app.route('/uploaded/<path:filename>')
def uploaded_static(filename):
    if not session.get('logged'):
        return redirect(url_for('index'))
    return send_from_directory(app.root_path + '/uploaded/', filename)

@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    if not session.get('logged'):
        return redirect(url_for('index'))
    if request.form.get('ingredients') is not None:
        ingredients = json.loads(request.form.get('ingredients'))
        with open(os.path.join(app.config['UPLOAD_FOLDER'], str(round(time.time()*1000)) + '.json'), 'w') as outfile:
            json.dump(ingredients, outfile)
        selectedIngredients = []
        for i in ingredients:
            selectedIngredients.append(i['selection'])
        session['ingredients'] = selectedIngredients
        return redirect(url_for('recipes'))
    elif session.get('ingredients'):
        selectedIngredients = session.get('ingredients')
    else:
        selectedIngredients = []
    return render_template('recipes.html', ingredients=selectedIngredients, noscript=True, num_cat=app.config['NUM_AVAILABLE_CATEGORIES'])

@app.route('/listrecipes', methods=['GET', 'POST'])
def listrecipes():
    if not session.get('logged'):
        return redirect(url_for('index'))
    if session.get('ingredients'):
        selectedIngredients = session.get('ingredients')
    else: return ''
    if request.form.get('cats') is not None: categories = json.loads(request.form.get('cats'))
    else: categories = []
    recipes = chooseRecipes(selectedIngredients, categories)
    return render_template('listrecipes.html', recipes=recipes)



@app.route('/log')
def log():
    if not session.get('logged'):
        return redirect(url_for('index'))
    files = []
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        if file.endswith(".json"): files.append(os.path.join(app.config['UPLOAD_FOLDER'], file))
    files.sort(key=os.path.getctime, reverse=True)
    data = []
    for i in range(min(len(files), 20)):
        with open(files[i]) as f:
            data.append(json.load(f))
    return render_template('log.html', data=data, uf=app.config['UPLOAD_FOLDER'])

@app.route('/recipe<id>')
def recipe(id):
    if not session.get('logged'):
        return redirect(url_for('index'))
    recipe = getRecipe(id)
    return render_template('recipe.html', recipe=recipe, noscript=True)

@app.route('/kategoriecetnosti<num>')
def kategoriecetnostir(num):    
    if not session.get('logged'):
        return redirect(url_for('index'))
    return json.dumps(kategoriecetnosti(num))