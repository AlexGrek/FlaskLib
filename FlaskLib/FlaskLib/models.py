import hashlib, binascii
from FlaskLib import dbx
from flask.ext.login import UserMixin

def get_passwd_hash(passwd):
    """hash function for security, returns salty hash of user password"""
    dk = hashlib.pbkdf2_hmac('sha256', passwd, b'salt', 10)
    return binascii.hexlify(dk)


association_table = dbx.Table('association', dbx.metadata,
    dbx.Column('left_id', dbx.Integer, dbx.ForeignKey('writers.id')),
    dbx.Column('right_id', dbx.Integer, dbx.ForeignKey('books.id'))
)


class Writer(dbx.Model):
    __tablename__ = 'writers'
    id = dbx.Column(dbx.Integer, primary_key=True)
    name = dbx.Column(dbx.String)
    children = dbx.relationship("Book",
                    secondary=association_table,
                    backref=dbx.backref('writers', lazy='dynamic'), 
                    lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
         return "<Writer('%s')>" % (self.name)


class Book(dbx.Model):
    __tablename__ = 'books'
    id = dbx.Column(dbx.Integer, primary_key=True)
    title = dbx.Column(dbx.String)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
         return "<Book('%s', '%s')>" % (self.title, self.id)


class User(dbx.Model, UserMixin):
    __tablename__ = 'users'
    id = dbx.Column(dbx.Integer, primary_key=True)
    name = dbx.Column(dbx.String)
    password = dbx.Column(dbx.String)
    is_authenticated = True
    is_anonymous = False
    is_active = True

    def __init__(self, name, password):
        self.name = name
        self.password = get_passwd_hash(password)

    def __repr__(self):
       return "<User('%s', '%s')>" % (self.name, self.password)
    
    def get_id(self):
        return unicode(self.id)