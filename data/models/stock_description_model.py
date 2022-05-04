### alpaca market data api model ###

from sre_constants import IN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Identity, Integer, String, BigInteger, Float, DateTime


Base = declarative_base()

class Description(Base):
    __tablename__ = 'stock_description'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    symbol = Column(String)
    fifty_two_week_high = Column(Float)
    fifty_two_week_low = Column(Float)
    market_cap = Column(Integer)
    average_volume = Column(Integer)
    current_volume = Column(Integer)
    shares_outstanding = Column(Integer)
    float = Column(Integer)


    def __repr__(self):
        return "<Stock Description(symbol='{}', ticker='{}', open='{}', high='{}', low='{}', close='{}', volume='{}')>" \
            .format(self.timestamp, self.ticker, self.open, self.high, self.low, self.close, self.volume)
