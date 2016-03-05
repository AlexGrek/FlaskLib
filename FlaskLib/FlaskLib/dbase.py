from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
import hashlib

def create_database():
    engine = create_engine('sqlite:///:memory:', echo=True)

    metadata = MetaData()

    users_table = Table('users', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('password', String))

    metadata.create_all(engine)

if __name__ == '__main__':
    create_database()