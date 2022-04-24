import unittest
import pandas as pd
from data.datacleaner.cleaner import *


class TestDataCleaner(unittest.TestCase):

    price_data = [["2022-04-01 07:49+00:00", 175.25, 17588, 17510, 175.27, 35143, 800, 175.35524]]

    def setUp(self) -> None:
        # timestamp, open, high, low, close, volume, trade_count, vwap
        self.price_dataframe = pd.DataFrame(
            self.price_data,
            columns=["timestamp", "open", "high", "low", "close", "volume", "trade_count", "vwap"]
        )

    # Test that ticker column is added to df, and it contains correct value
    def test_adding_ticker_column(self):
        df = add_ticker_column_and_populate(self.price_dataframe, "AAPL")
        ticker_is_df_column = "ticker" in df
        self.assertTrue(ticker_is_df_column)

        ticker_col_values = df.loc[:, "ticker"]
        for values in ticker_col_values:
            self.assertEqual(values, "AAPL")

    # Test removing an existing column
    def test_remove_column_exist(self):
        df = remove_columns(self.price_dataframe, "trade_count", in_place=False)
        df_contains_trade_count_col = "trade_count" in df
        self.assertFalse(df_contains_trade_count_col)



if __name__ == '__main__':
    unittest.main()
