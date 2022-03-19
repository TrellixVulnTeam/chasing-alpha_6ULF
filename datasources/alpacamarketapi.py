from alpaca_trade_api.rest import REST, TimeFrame
from dotenv import load_dotenv
from jupyternotebook.tickers import *

import os

'''
Requires .env file
'''

HOURLY = TimeFrame.Hour

config = load_dotenv("../.env")
ALPACA_API_KEY = os.getenv("ALPACA_MARKET_DATA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_MARKET_DATA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"
UNWANTED_FIFTH_LETTER = ["W", "R", "Q"]

class AlpacaMarketDataApi:

    def __init__(self):
        api = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, BASE_URL, api_version="v2")
        bar_iter = api.get_bars("AAPL", HOURLY, "2021-06-08", "2021-06-08", adjustment='raw')
        for bar in bar_iter:
            print(bar)


if __name__ == '__main__':
    app = AlpacaMarketDataApi()
    nasdaq = getNasdaqTickers()
    other = getOtherTickers()
    union = eliminateDuplicates(nasdaq, other)
    split = splitSetWantedAndUnwantedTickers(union, UNWANTED_FIFTH_LETTER)
    print(len(split[0]))
