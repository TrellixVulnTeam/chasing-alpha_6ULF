import datetime

from alpaca_trade_api.rest import TimeFrame, TimeFrameUnit, APIError, REST
from dotenv import load_dotenv, find_dotenv
from jupyternotebook.tickers import *
from utils.timer import Timer
from datetime import date
from ratelimit import limits, sleep_and_retry
from pandas import DataFrame
import numpy as np
import os
from typing import Final

'''
Requires .env file placed at root level.
'''

config = load_dotenv(find_dotenv())
ALPACA_API_VERSION = "v2"
ALPACA_API_KEY: Final = os.getenv("ALPACA_MARKET_DATA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_MARKET_DATA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"
HOURLY = TimeFrame(59, TimeFrameUnit.Minute)
ALPACA_API_CALL_LIMIT = 199
ONE_MIN_ONE_SEC = 61

UNWANTED_FIFTH_LETTER = ["W", "R", "Q"]
ONE_WEEK_AGO = (date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
FIVE_YEARS_AGO = (date.today() - datetime.timedelta(days=(365*5))).strftime("%Y-%m-%d")


def clean_historical_price_data(dataframe: DataFrame, ticker: str) -> DataFrame:
    if "ticker" not in dataframe:
        dataframe["ticker"] = ticker

    if "trade_count" in dataframe.columns:
        dataframe.drop("trade_count", axis=1, inplace=True)

    if "vwap" in dataframe.columns:
        dataframe.drop("vwap", axis=1, inplace=True)
    return dataframe


def get_all_tickers():
    nasdaq = get_nasdaq_tickers()
    other = get_other_tickers()
    union_nasdaq_other = eliminate_duplicates(nasdaq, other)

    return split_set_wanted_and_unwanted_tickers(union_nasdaq_other, UNWANTED_FIFTH_LETTER)


class AlpacaMarketDataApi:

    def __init__(self):
        self.api = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, BASE_URL, api_version=ALPACA_API_VERSION)
        self.timer = Timer()
        # Number of tickers whose data was successfully retrieved and stored
        self.actual_tickers_processed = 0

    @sleep_and_retry
    @limits(calls=ALPACA_API_CALL_LIMIT, period=ONE_MIN_ONE_SEC)
    def get_data_by_ticker(self, ticker: str, time_frame, start: str, end: str):
        """
        start and end date format: %Y-%m-%d (2020-01-01)
        API calls limited to 199 per 61 seconds to conform to Alpaca rate limit.
        :return: a pandas dataframe
        """
        try:
            self.timer.start("get_data_by_ticker")
            dataframe = self.api.get_bars(ticker, time_frame, start, end, adjustment='raw').df
            dataframe = clean_historical_price_data(dataframe, ticker)
            return dataframe
        except APIError:
            print(f"APIError: unable to retrieve {ticker}")
        finally:
            self.timer.stop_and_print_elapsed_time("get_data_by_ticker")


    def save_all_ticker_data(self):
        """
        Saves tickers (found in list) to a csv file.
        :return: void
        """
        list_of_all_tickers = get_all_tickers()

        self.timer.start("save_all_tickers")
        for ticker in list_of_all_tickers[0]:
            dataframe = self.get_data_by_ticker(ticker, HOURLY, FIVE_YEARS_AGO, ONE_WEEK_AGO)

            if dataframe is not None:
                self.actual_tickers_processed += 1
                dataframe.to_csv(r'D:\data\market_data.csv', mode="a", index=False, header=False)
                print(f"Tickers processed so far: {self.actual_tickers_processed}")
            if self.actual_tickers_processed == 1000:
                total_time_elapsed = self.timer.stop("save_all_tickers")
                print(f"Done. Tickers processed: {self.actual_tickers_processed}. Total time elapsed: {total_time_elapsed}")
                return


if __name__ == '__main__':
    app = AlpacaMarketDataApi()
    #app.save_all_ticker_data()

    df = app.get_data_by_ticker("AAPL", HOURLY, "2021-01-01", ONE_WEEK_AGO)
    print(df)

