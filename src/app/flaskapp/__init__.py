from flask import Flask
import os
from flaskapp import config
from flaskapp import dbconfig
import psycopg2
from psycopg2 import pool

app = Flask(__name__, template_folder='html')
app.config.from_object(config.Config())
app.config.from_object(dbconfig.DbConfig())
app.config['postgreSQL_pool'] = psycopg2.pool.SimpleConnectionPool(1, 20,
    user = app.config['DB_USER'],
    password = app.config['DB_PASSWORD'],
    host = app.config['DB_HOST'],
    port = app.config['DB_PORT'],
    database = app.config['DB_NAME'])

from flaskapp import routes