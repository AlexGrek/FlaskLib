"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, flash, request, abort, redirect, url_for
from FlaskLib import app, db, lm, oid
from forms import *
from flask.ext.login import *


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        
        

        login_user(user)
        print 'so here we fucking go'

        flash('Logged in successfully.')

        

        next = request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url

        return redirect(url_for(next or 'home'))
    return render_template('login.html', form=form)



@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
