### alpaca market data api model ###

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, BigInteger, TIMESTAMP, Float
from sqlalchemy.dialects.postgresql import MONEY

Base = declarative_base()

class TickerPrice(Base):
    __tablename__ = 'ticker_prices'
    timestamp = Column(TIMESTAMP, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)
    ticker = Column(String)

    def __repr__(self):
        return "<TickerPrice(time='{}', ticker='{}', open='{}', high='{}', low='{}', close='{}', volume='{}')>" \
            .format(self.timestamp, self.ticker, self.open, self.high, self.low, self.close, self.volume)
