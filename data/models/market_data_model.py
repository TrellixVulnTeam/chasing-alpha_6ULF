### alpaca market data api model ###

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, BigInteger, Float, DateTime


Base = declarative_base()

class TickerPrice(Base):
    __tablename__ = 'ticker_prices'
    timestamp = Column(DateTime, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)
    vwap = Column(Float)
    ticker = Column(String, primary_key=True)

    def __repr__(self):
        return "<TickerPrice(time='{}', ticker='{}', open='{}', high='{}', low='{}', close='{}', volume='{}')>" \
            .format(self.timestamp, self.ticker, self.open, self.high, self.low, self.close, self.volume)
