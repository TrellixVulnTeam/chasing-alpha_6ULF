from sre_constants import IN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Identity, Integer, String, BigInteger, Float 

Base = declarative_base()

'''
Filters:
    Top Losers
    Under $50
    USA
    0.5 relative volume
    Over 1m average volume

Scrape 3 days worth of data per stock.
'''

'''
For data points that can change significantly daily
'''
class StratOneDailyModel(Base):
    __tablename__ = 'strat_one_daily'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    symbol = Column(String)
    perc_change = Column(Float)
    current_volume = Column(Integer)
    float = Column(Integer)
    short_float_perc = Column(Float)
    previous_close = Column(Float)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)


'''
For data points which don't change drastically daily
'''
class StratOneFixedModel(Base):
    __tablename__ = 'strat_one_fixed'
    symbol = Column(String)
    market_cap = Column(Integer)
    fiftytwo_week_high = Column(Float)
    fiftytwo_week_low = Column(Float)
    average_volume = Column(Integer)