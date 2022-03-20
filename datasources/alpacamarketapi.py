import datetime

from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
from dotenv import load_dotenv
from jupyternotebook.tickers import *
from utils.timer import Timer
from datetime import date
import time
import os

'''
Requires .env file
'''

config = load_dotenv("../.env")
ALPACA_API_VERSION = "v2"
ALPACA_API_KEY = os.getenv("ALPACA_MARKET_DATA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_MARKET_DATA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"
HOURLY = TimeFrame(59, TimeFrameUnit.Minute)

UNWANTED_FIFTH_LETTER = ["W", "R", "Q"]
ONE_WEEK_AGO = (date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
FIVE_YEARS_AGO = (date.today() - datetime.timedelta(days=(365*5))).strftime("%Y-%m-%d")

class AlpacaMarketDataApi:

    def __init__(self):
        self.api = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, BASE_URL, api_version=ALPACA_API_VERSION)
        self.timer = Timer()

    # start and end date format: %Y-%m-%d (2020-01-01)
    def get_data_by_ticker(self, ticker: str, start: str, end: str):
        self.timer.start("get_data_by_ticker")
        data = self.api.get_bars(ticker, HOURLY, start, end, adjustment='raw')
        self.timer.stop_and_print_elapsed_time("get_data_by_ticker")
        return data


    def get_all_tickers(self):
        nasdaq = getNasdaqTickers()
        other = getOtherTickers()
        union_nasdaq_other = eliminateDuplicates(nasdaq, other)

        wanted_unwanted_tickers = splitSetWantedAndUnwantedTickers(union_nasdaq_other, UNWANTED_FIFTH_LETTER)

if __name__ == '__main__':
    app = AlpacaMarketDataApi()
