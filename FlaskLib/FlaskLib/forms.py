from flask_wtf import Form
from wtforms import BooleanField, TextField, PasswordField, validators

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=3, max=10)])
    email = TextField('Email Address', [validators.Length(min=2, max=50)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])

class LoginForm(Form):
    username = TextField('username', [validators.Required()])
    password = TextField('password', [validators.Required()])