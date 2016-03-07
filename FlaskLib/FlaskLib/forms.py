from flask_wtf import Form
from wtforms import BooleanField, TextField, PasswordField, IntegerField, validators

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=3, max=10)])
    password = PasswordField('New Password', [
        validators.Required(), validators.Length(min=3),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    username = TextField('username', [validators.Required()])
    password = PasswordField('password', [validators.Required()])

class BookForm(Form):
    id = IntegerField('id')
    title = TextField('Book title', [validators.Required(), validators.Length(min=3)])
    writers = TextField('Writers (comma separated)')

class WriterForm(Form):
    id = IntegerField('id')
    name = TextField('Full name', [validators.Required(), validators.Length(min=3)])