import yfinance as yf
import pandas as pd
'''this function should pull stock history given a stock input,
       please follow this link to get example on how to use yahoo finance api
       https://github.com/ranaroussi/yfinance
    '''

'''
1. Convert the index into column
2. Adding a new column into the dataframe
3. Select certain columns from the dataframe
'''
def get_stock_history(stock:str) -> pd.DataFrame:
    # Initialize the Ticker object for the specified
    ticker = yf.Ticker(stock)
    # get all stock info
    stock_info = ticker.info
    # get historical market data
    history_data:pd.DataFrame = ticker.history(period = "ytd")
    history_data = history_data.reset_index()
    history_data["Stock"] = stock
    history_data = history_data[["Date","Open", "High", "Low", "Close", "Volume","Dividends", "Stock"]] 
    
    
    # Return the collected data
    return history_data



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

    transposed_financials = transposed_financials.reset_index()
    transposed_financials.columns.values[0] = "Date"
    transposed_financials["Stock"] =stock
    transposed_financials = transposed_financials[["Date",
        "Tax Effect Of Unusual Items",
        "Tax Rate For Calcs",
        "Normalized EBITDA",
        "Net Income From Continuing Operation Net Minority Interest",
        "Reconciled Depreciation",
        "Reconciled Cost Of Revenue",
        "EBITDA",
        "EBIT",
        "Stock"]]

    # Return the collected data
    return transposed_financials



