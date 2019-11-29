from flask import render_template, make_response, request, session, flash
from flaskapp import app
from flaskapp.forms import LoginForm
from flaskapp.func import allowed_file, convert_image, recognize
import json
import os
import time

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
            estimation = recognize(newfilename)
            names.append({'filename': newfilename, 'estimation': dict(estimation)})
    uploaded = session.get('uploaded') or []
    uploaded.extend(names)
    session['uploaded'] = uploaded
    return json.dumps(names)