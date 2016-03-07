"""
The flask application package.
"""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID


app = Flask(__name__)

app.config.from_object('config')


lm = LoginManager()
lm.login_view = 'login'
lm.init_app(app)


oid = OpenID(app, 'tmp')

dbx = SQLAlchemy(app)

print dbx

import FlaskLib.views