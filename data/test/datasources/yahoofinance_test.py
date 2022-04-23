import unittest

from data.datasources.yahoo_finance import *


class TestYahooFinanceApi(unittest.TestCase):
    def test_eliminate_duplicates(self):
        nasdaq_tickers = get_nasdaq_tickers()
        other_tickers = get_other_tickers()
        sp500_tickers = get_sp500_tickers()
        dow_tickers = get_dow_tickers()
        remove_duplicates = eliminate_duplicates(nasdaq_tickers, other_tickers, sp500_tickers, dow_tickers)
        # Compare sizes
        size_of_tickers = len(nasdaq_tickers) + len(other_tickers) + len(sp500_tickers) + len(dow_tickers)
        size_of_removed = len(remove_duplicates)

        self.assertLess(size_of_removed, size_of_tickers)

    def test_split_wanted_unwanted_5_letters(self):
        unwanted_fifth_letter = ['W', 'U']
        nasdaq_tickers = ['VLATU', 'NMTC', 'SESN', 'BRLIW', 'ITAQW', 'LAMR','ACHV', 'MCAAU']

        tuple_list = split_set_wanted_and_unwanted_tickers(nasdaq_tickers, unwanted_fifth_letter)
        size_nasdaq_wanted = 4
        size_list_wanted =  len(tuple_list[0])
        self.assertEqual(size_list_wanted, size_nasdaq_wanted)

    def test_split_wanted_unwanted_short_tickers(self):
        unwanted_fifth_letter = ['W', 'U']
        nasdaq_tickers = ['U', 'TC', 'ESN', '', 'ITAQW', 'LAMR','ACHV', 'MCAAU']

        tuple_list = split_set_wanted_and_unwanted_tickers(nasdaq_tickers, unwanted_fifth_letter)
        size_nasdaq_wanted = 5
        size_list_wanted =  len(tuple_list[0])
        self.assertEqual(size_list_wanted, size_nasdaq_wanted)

if __name__ == '__main__':
    unittest.main()
