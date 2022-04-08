### alpaca market data api model ###

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()

# TODO: create data model https://www.learndatasci.com/tutorials/using-databases-python-postgres-sqlalchemy-and-alembic/

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    pages = Column(Integer)
    published = Column(Date)

    def __repr__(self):
        return "<Book(title='{}', author='{}', pages={}, published={})>" \
            .format(self.title, self.author, self.pages, self.published)

