#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from yahoo_fin import stock_info as si

import itertools


# In[3]:


'''
Open Jupyter Notebook to edit this file if needed, run: jupyter notebook.
http://theautomatic.net/yahoo_fin-documentation/#tickers_sp500

To manually convert ipynb to py file, run: jupyter nbconvert --to script my-notebook.ipynb
'''

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
    # Approximately 6462 symbols
    sp500 = pd.DataFrame(si.tickers_sp500())
    sp500_set = set(symbol for symbol in sp500[0].values.tolist())
    return sp500_set


def get_dow_tickers():
    # Approximately 6462 symbols
    dow = pd.DataFrame(si.tickers_dow())
    dow_set = set(symbol for symbol in dow[0].values.tolist())
    return dow_set

# Set should eliminate duplicate, if there are any.
def eliminate_duplicates(setOne, setTwo):
    unionSet = set.union(setOne, setTwo)
    return unionSet

'''
Remove certain tickers based on their 5th letter.
@param list of 5th letters (e.g ["W", "R", "Q"])
@return tuple 0: wanted tickers, 1: unwanted tickers
'''
def split_set_wanted_and_unwanted_tickers(setToSplit, list_of_fifth_letters):
    unwanted_tickers_set = set()
    wanted_tickers_set = set()
    
    for symbol in setToSplit:
        if(len(symbol) < 1 or (len(symbol) > 4 and symbol[-1] in list_of_fifth_letters)):
            unwanted_tickers_set.add(symbol)
        else:
            wanted_tickers_set.add(symbol)
        
    return wanted_tickers_set, unwanted_tickers_set


# In[ ]:





# In[ ]:




