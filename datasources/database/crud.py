### crud operations against postgres db ###
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datasources.database.connection import DATABASE_URI
from datasources.models.market_data_model import Base, Book

engine = create_engine(DATABASE_URI)

# Reminder: always close the session to free up resources and connection.
# Not closing a session will prevent you from recreating a database
Session = sessionmaker(bind=engine)

def insert_row_books():
    book = Book(
        title='Deep Learning',
        author='Ian Goodfellow',
        pages=775,
        published=datetime(2016, 11, 18)
    )
    s = Session()
    s.add(book)
    s.commit()
    s.close()

def read_row_books():
    s = Session()
    row_data =  s.query(Book).first()
    s.close()
    return row_data
# Drops all db create from 'Base' in models folder, then recreates them
def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
