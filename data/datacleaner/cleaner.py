from pandas import DataFrame


def add_ticker_column_and_populate(dataframe: DataFrame, ticker_name: str) -> DataFrame:
    if "ticker" not in dataframe:
        dataframe["ticker"] = str(ticker_name)

    return dataframe

def remove_columns(dataframe: DataFrame, column_name, in_place=True) -> DataFrame:
    try:
        return dataframe.drop(column_name, axis=1, inplace=in_place)
    except KeyError:
        print("column: {} doesn't exist".format(column_name))
        pass

