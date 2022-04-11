### alpaca market data api model ###

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, BigInteger, TIMESTAMP
from sqlalchemy.dialects.postgresql import MONEY

Base = declarative_base()

# TODO: create data model https://www.learndatasci.com/tutorials/using-databases-python-postgres-sqlalchemy-and-alembic/

class TickerPrice(Base):
    __tablename__ = 'ticker_prices'
    timestamp = Column(TIMESTAMP, primary_key=True)
    open = Column(MONEY)
    high = Column(MONEY)
    low = Column(MONEY)
    close = Column(MONEY)
    volume = Column(BigInteger)
    ticker = Column(String)

    def __repr__(self):
        return "<Book(title='{}', author='{}', pages={}, published={})>" \
            .format(self.title, self.author, self.pages, self.published)
