"""
The flask application package.
"""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.login import LoginManager


app = Flask(__name__)

app.config.from_object('config')


lm = LoginManager()
lm.login_view = 'login'
lm.init_app(app)


dbx = SQLAlchemy(app)

print dbx #to know where our database is

import FlaskLib.views