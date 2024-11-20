import yfinance as yf
import pandas as pd
'''this function should pull stock history given a stock input,
       please follow this link to get example on how to use yahoo finance api
       https://github.com/ranaroussi/yfinance
    '''
def get_stock_history(stock:str) -> pd.DataFrame:
    # Initialize the Ticker object for the specified
    ticker = yf.Ticker(stock)
    # get all stock info
    stock_info = ticker.info
    # get historical market data
    history_data:pd.DataFrame = ticker.history(period = "ytd")
    
# Return the collected data
    return history_data
    
print(get_stock_history("MSFT"))


def get_stock_financials(stock:str) -> pd.DataFrame:
    '''this function should get share holders of a stock given a stock input,
       please follow this link to get example on how to use yahoo finance api
       https://github.com/ranaroussi/yfinance
    '''
    # Initialize the Ticker object for the specified
    ticker = yf.Ticker(stock)
    # get all stock info
    stock_info = ticker.info
    # get historical financial data
    financials:pd.DataFrame = ticker.financials
    transposed_financials = financials.transpose()

# Return the collected data
    return transposed_financials
    
print(get_stock_financials("MSFT"))


