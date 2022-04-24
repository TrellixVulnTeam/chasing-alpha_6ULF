import random

from dotenv import load_dotenv

from data.database.connection import Connect
from data.database.crud import Crud
from data.datacleaner.cleaner import add_ticker_column_and_populate, remove_columns
from data.datasources.alpacamarketapi import AlpacaMarketDataApi, ONE_WEEK_AGO, HOURLY_TIMEFRAME, FIVE_YEARS_AGO, \
    FIVE_MINUTE_TIMEFRAME
from data.datasources.yahoo_finance import get_all_tickers
from data.models.market_data_model import TickerPrice
from utils.timer import Timer

"""
Entry point for getting data from API's such as Alpaca.

Objective og 'data' folder:
 1. Retrieve market data from 3rd party APIs.
 2. Clean the data and insert into the database periodically.
 3. Be able to query from the database.
 4. Keep data in database up to date.

"""
config = load_dotenv("../.env")
class ChasingAlphaData:

    def __init__(self, connect: Connect, alpaca_api: AlpacaMarketDataApi, crud_ops: Crud):
        self.connect = connect
        self.alpaca = alpaca_api
        self.crud_ops = crud_ops

    # Can we optimize insertion speed with timescale db?
    # Can we stream everything, so that as we get the data we are simultaneously processing it?
    def save_all_ticker_data_to_db(self):
        self.crud_ops.recreate_database()
        # connect to postgres via psycopg2
        connection = self.connect.connect_to_db()

        # get list of tickers to query from Alpaca
        list_of_tickers = get_all_tickers()
        wanted_list = list_of_tickers[0]
        total_get_df_by_ticker_time = 0
        total_cleaning_time = 0
        total_insertion_time = 0
        for i, ticker in enumerate(random.sample(wanted_list, 10)):
            # print(ticker)
            # get df for each ticker
            Timer.start("get_data_by_ticker")
            df = self.alpaca.get_data_by_ticker(ticker, FIVE_MINUTE_TIMEFRAME, FIVE_YEARS_AGO, ONE_WEEK_AGO)
            total_get_df_by_ticker_time += Timer.stop("get_data_by_ticker")

            # clean the dataframe
            Timer.start("cleaning")
            df = add_ticker_column_and_populate(df, ticker)
            remove_columns(df, "trade_count")
            total_cleaning_time += Timer.stop("cleaning")

            # insert (append, hopefully) df to database
            Timer.start("copy_to_database")
            self.crud_ops.copy_dataframe_to_database(connection, df, TickerPrice.__tablename__)
            total_insertion_time += Timer.stop("copy_to_database")

        connection.close()

        print("Average df retrieve time: {}".format(total_get_df_by_ticker_time/10))
        print("Average cleaning time: {}".format(total_cleaning_time/10))
        print("Average insertion time: {}".format(total_insertion_time/10))


if __name__ == "__main__":
    alpaca_market_data_api = AlpacaMarketDataApi()
    connect_db = Connect()
    crud = Crud(connect_db)

    chasing_alpha_data = ChasingAlphaData(
        connect_db,
        alpaca_market_data_api,
        crud
    )

    chasing_alpha_data.save_all_ticker_data_to_db()