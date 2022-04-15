### crud operations against postgres db ###
from sqlalchemy.orm import sessionmaker

from datasources.database.connection import engine
from datasources.models.market_data_model import TickerPrice, Base

# Reminder: always close the session to free up resources and connection.
# Not closing a session will prevent you from recreating a database

Session_maker = sessionmaker(bind=engine)

def insert_row(ticker_row_data: TickerPrice):
    with Session_maker() as session:
        session.add(ticker_row_data)
        session.commit()

def read_first_row():
    with Session_maker() as session:
        row_data = session.query(TickerPrice).first()
        return row_data

def recreate_database():
    """Drops all db create from 'Base' in models folder, then recreates them"""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
