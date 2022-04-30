import concurrent.futures

from pandas import DataFrame
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

def fill_database():
    alpaca_market_data_api = AlpacaMarketDataApi()
    connect_db = Connect()
    crud = Crud(connect_db)

    chasing_alpha_data = ChasingAlphaData(
        connect_db,
        alpaca_market_data_api,
        crud
    )

    chasing_alpha_data.save_all_ticker_data_to_db()

class ChasingAlphaData:

    def __init__(self, connect: Connect, alpaca_api: AlpacaMarketDataApi, crud_ops: Crud):
        self.connect = connect
        self.alpaca = alpaca_api
        self.crud_ops = crud_ops

    def save_all_ticker_data_to_db(self):
        self.crud_ops.recreate_database()
        # connect to postgres via psycopg2
        connection = self.connect.connect_to_db()

        # get list of tickers to query from Alpaca
        list_of_tickers = get_all_tickers()
        wanted_list = list_of_tickers[0]
        Timer.start("market_data")

        self.process_dataframe_single_thread(wanted_list, connection)

        Timer.stop_and_print_elapsed_time("market_data")
        connection.close()


    def get_df_by_ticker(self, ticker: str) -> DataFrame:
        df = self.alpaca.get_data_by_ticker(ticker, FIVE_MINUTE_TIMEFRAME, FIVE_YEARS_AGO, ONE_WEEK_AGO)
        return df

    def get_df_by_ticker_return_df_ticker(self, ticker: str):
        df = self.alpaca.get_data_by_ticker(ticker, FIVE_MINUTE_TIMEFRAME, FIVE_YEARS_AGO, ONE_WEEK_AGO)
        return df, ticker

    # Not in use, Alpaca rate limit is a bottleneck. Paying for premium data access will fix this.
    def process_dataframe_multi_threaded(self, ten_wanted_list, connection):
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
            for df, ticker in executor.map(self.get_df_by_ticker_return_df_ticker, ten_wanted_list):

                df = add_ticker_column_and_populate(df, ticker)
                remove_columns(df, "trade_count")

                self.crud_ops.copy_dataframe_to_database(connection, df, TickerPrice.__tablename__)

    def process_dataframe_single_thread(self, ticker_list, connection):
        for ticker in ticker_list:
            # get df for each ticker
            df = self.get_df_by_ticker(ticker)

            # clean the dataframe
            df = add_ticker_column_and_populate(df, ticker)
            remove_columns(df, "trade_count")

            # insert (append, hopefully) df to database
            self.crud_ops.copy_dataframe_to_database(connection, df, TickerPrice.__tablename__)

if __name__ == "__main__":
    print("hi")
