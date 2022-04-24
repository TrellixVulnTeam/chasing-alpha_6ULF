import pandas as pd
from yahoo_fin import stock_info as si


'''
This py file helps to get a list of tickers we are interested in.

### OLD COMMENTS to be refactored ###
Open Jupyter Notebook to edit this file if needed, run: jupyter notebook.
http://theautomatic.net/yahoo_fin-documentation/#tickers_sp500

To manually convert ipynb to py file, run: jupyter nbconvert --to script my-notebook.ipynb
'''


UNWANTED_FIFTH_LETTER = ["W", "R", "Q"]

def get_all_tickers():
    """
    Gets ticker symbols from nasdaq and 'other' (see Alpaca docs)
    Eliminates any duplicate ticker symbols.
    Splits set into wanted and unwanted tickers.
    :return: A tuple where index 0 is the wanted (filtered) list of tickers and index 1 is the unwanted tickers
    """
    nasdaq = get_nasdaq_tickers()
    other = get_other_tickers()
    union_nasdaq_other = eliminate_duplicates(nasdaq, other)

    return split_set_wanted_and_unwanted_tickers(union_nasdaq_other, UNWANTED_FIFTH_LETTER)

def get_nasdaq_tickers():
    # Approximately 5608 symbols
    nasdaq = pd.DataFrame(si.tickers_nasdaq())
    nasdaq_set = set(symbol for symbol in nasdaq[0].values.tolist())
    return nasdaq_set

def get_other_tickers():
    # Approximately 6462 symbols
    other = pd.DataFrame(si.tickers_other())
    other_set = set(symbol for symbol in other[0].values.tolist())
    return other_set

def get_sp500_tickers():
    sp500 = pd.DataFrame(si.tickers_sp500())
    sp500_set = set(symbol for symbol in sp500[0].values.tolist())
    return sp500_set

def get_dow_tickers():
    dow = pd.DataFrame(si.tickers_dow())
    dow_set = set(symbol for symbol in dow[0].values.tolist())
    return dow_set

def eliminate_duplicates(*ticker_sets):
    union_set = set.union(*ticker_sets)
    return union_set

def split_set_wanted_and_unwanted_tickers(set_to_split, list_of_fifth_letters):
    """
    Remove certain tickers based on their 5th letter.
    :param set_to_split:
    :param list_of_fifth_letters: the 5th letter to filter out unwanted tickers
    :return: tuple index 0: wanted tickers, index 1: unwanted tickers
    """
    unwanted_tickers_set = set()
    wanted_tickers_set = set()

    for symbol in set_to_split:
        if len(symbol) < 1 or (len(symbol) > 4 and symbol[-1] in list_of_fifth_letters):
            unwanted_tickers_set.add(symbol)
        else:
            wanted_tickers_set.add(symbol)

    return wanted_tickers_set, unwanted_tickers_set