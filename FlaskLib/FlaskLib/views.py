"""
Routes and views for the flask application.
"""

from datetime import datetime
import encodings
from flask import render_template, flash, request, abort, redirect, url_for, jsonify
from FlaskLib import app, dbx, lm, oid
from forms import *
from models import *
from flask.ext.login import login_user, logout_user, current_user, login_required

@lm.user_loader
def load_user(id):
    try:
        return User.query.get(int(id))
    except ValueError:
        return None


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    bookz = Book.query.all()
    return render_template(
        'index.html',
        title='Home Page', user = current_user,
        books = bookz
    )

@app.route('/')
@app.route('/writers')
def writers():
    """Renders the home page."""
    wrs = Writer.query.all()
    return render_template(
        'writers.html',
        title='Writers', user = current_user,
        writers = wrs
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        passwd = get_passwd_hash(form.password.data)
        print 'user', form.username.data, 'is trying to log in with pass: ', passwd
        user = User.query.filter_by(name = form.username.data, password = passwd).first()
        if user is not None:
            login_user(user)
            print 'user', user.name, 'succesfully logged in'
            flash('Logged in successfully.')
            next = request.args.get('next')
                # next_is_valid should check if the user has valid
                # permission to access the `next` url

            return redirect(url_for(next or 'home'))
        else:
            flash('wrong user/password')
    return render_template('login.html', form=form, user = current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        userWithUrLogin = User.query.filter_by(name = form.username.data).first()
        if userWithUrLogin is not None:
            flash('user with this name is already registered')
            return render_template('register.html', form=form, user = current_user)
        user = User(name = form.username.data, password= form.password.data)
        dbx.session.add(user)
        dbx.session.commit()
        return redirect(url_for('home'))
        
    return render_template('register.html', form=form, user = current_user)


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.',
        user = current_user
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.', user = current_user
    )

@app.route('/get_authors')
def get_authors_json():
    id = request.args['id']
    book = Book.query.filter_by(id = id).first()
    if book is None:
        return jsonify({'authors': []})
    authors = book.writers.all()
    author_names = [author.name for author in authors]
    return jsonify({'authors': author_names})

@app.route('/remove_book')
@login_required
def remove_book():
    id = request.args['id']
    book = Book.query.filter_by(id = id).first()
    if book is None:
        return redirect(url_for('home'))
    dbx.session.delete(book)
    dbx.session.commit()
    return redirect(url_for('home'))

@app.route('/remove_writer')
@login_required
def remove_writer():
    id = request.args['id']
    wr = Writer.query.filter_by(id = id).first()
    if wr is None:
        return redirect(url_for('writers'))
    dbx.session.delete(wr)
    dbx.session.commit()
    return redirect(url_for('writers'))

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(title = form.title.data)
        writers = form.writers.data.split(",")
        for wr in writers:
            him = Writer.query.filter_by(name = wr.strip()).first()
            if him is None:
                him = Writer(wr.strip())
                dbx.session.add(him)
            if him not in book.writers:
                book.writers.append(him)

        dbx.session.add(book)
        dbx.session.commit()
        id = book.id
        return redirect(url_for('home'))
    return render_template('add_book.html', form=form, user = current_user)

@app.route('/edit_book', methods=['GET', 'POST'])
@login_required
def edit_book():
    form = BookForm()
    id = request.args['id']
    if request.method == 'GET':
        #return form with data
        book = Book.query.filter_by(id = id).first()
        form.title.data = book.title
        form.writers.data = ', '.join([str(writer.name) for writer in book.writers])
        form.id.data = book.id
    elif request.method == 'POST':
        #write data into book
        book = Book.query.filter_by(id = id).first()
        if form.validate_on_submit():
            book.title = form.title.data
            writers_raw = form.writers.data.split(",")
            writers = [w.strip() for w in writers_raw]
            oldwriters = book.writers
            for oldwr in oldwriters: #remove writers
                if oldwr.name.strip() not in writers:
                    book.writers.remove(oldwr)
            for wr in writers: #add writers
                him = Writer.query.filter_by(name = wr.strip()).first()
                if him is None:
                    him = Writer(wr.strip())
                    dbx.session.add(him)
                if him not in book.writers:
                    book.writers.append(him)
            print book
            dbx.session.commit()
            print book
            return redirect(url_for('home'))
    return render_template('edit_book.html', form=form, user = current_user)

@app.route('/edit_writer', methods=['GET', 'POST'])
@login_required
def edit_writer():
    form = WriterForm()
    id = request.args['id']
    if request.method == 'GET':
        #return form with data
        w = Writer.query.filter_by(id = id).first()
        form.name.data = w.name
        form.id.data = w.id
    elif request.method == 'POST':
        #write data into writer
        wr = Writer.query.filter_by(id = id).first()
        if form.validate_on_submit():
            w = Writer.query.filter_by(name = form.name.data.strip()).first()
            if w is not None:
                if w.name == wr.name:
                    flash('Nothing changed')
                    return redirect(url_for('writers'))
                flash('Writer with name "%s" already exists' % form.name.data)
                return render_template('edit_writer.html', form=form, user = current_user)
            wr.name = form.name.data.strip()
            dbx.session.commit()
            return redirect(url_for('writers'))
    return render_template('edit_writer.html', form=form, user = current_user)

@app.route('/all_authors')
def get_all_authors_json():
    writers = Writer.query.all()
    author_names = [author.name for author in writers]
    return jsonify({'authors': author_names})

