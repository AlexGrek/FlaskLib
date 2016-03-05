import hashlib
import binascii
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)

    def __init__(self, name, password):
        dk = hashlib.pbkdf2_hmac('sha256', password, b'salt', 100000)
        
        self.name = name
        self.password = binascii.hexlify(dk)

    def __repr__(self):
       return "<User('%s', '%s')>" % (self.name, self.password)
    
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)