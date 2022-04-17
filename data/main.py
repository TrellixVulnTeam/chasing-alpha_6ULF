from data.database.connection import connect, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from data.database.crud import copy_dataframe_to_database
from data.datasources.alpacamarketapi import AlpacaMarketDataApi, ONE_WEEK_AGO, HOURLY
from data.models.market_data_model import TickerPrice


"""
Entry point for getting data from API's such as Alpaca.

Objective:
 1. Cleaning the data and inserting into the database.
 2. Reading from the database.
 3. Keeps data in database up to date.

Establishing a connecting to database in done in [connection.py]
"""

class ChasingAlphaData:

    def __init__(self):
        self.alpaca = AlpacaMarketDataApi()

    def get_and_save_df_to_db(self):
        df = self.alpaca.get_data_by_ticker("AAPL", HOURLY, "2021-01-01", ONE_WEEK_AGO)
        connection = connect(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

        copy_dataframe_to_database(connection, df, TickerPrice.__tablename__)

        connection.close()



if __name__ == "__main__":
    chasing_alpha_data = ChasingAlphaData()

    chasing_alpha_data.get_and_save_df_to_db()