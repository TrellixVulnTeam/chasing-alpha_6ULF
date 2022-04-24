from pandas import DataFrame


def add_ticker_column_and_populate(dataframe: DataFrame, ticker_name: str) -> DataFrame:
    if "ticker" not in dataframe:
        dataframe["ticker"] = str(ticker_name)

    return dataframe

def remove_columns(dataframe: DataFrame, column_name, in_place=True) -> DataFrame:
    if column_name in dataframe.columns:
        return dataframe.drop(column_name, axis=1, inplace=in_place)

    raise Exception("Trying to remove a column that doesn't exist")

