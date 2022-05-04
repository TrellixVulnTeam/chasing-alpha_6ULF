import yfinance as yf


def getStockInfo(symbol: str):
    """
    :return: dict in json format
    """
    stock = yf.Ticker(symbol)
    return stock.info


si = getStockInfo("MULN")
# info = jsonConverter(si)
print(si["fiftyTwoWeekLow"])