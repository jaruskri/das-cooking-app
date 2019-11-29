from flask import Flask
import os
from flaskapp import config

app = Flask(__name__, template_folder='html')
app.config.from_object(config.Config())

from flaskapp import routes