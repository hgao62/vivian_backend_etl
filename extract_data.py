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
    """Download stock history for a given ticker

    Args:
        stock (str): stock ticker name

    Returns:
        pd.DataFrame: data frame with stock price data
    """
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


### Task 2
# 1. add a function called get_exchange_rate to extract_data.py so it can download fx rate for us
def get_exchange_rate(from_currency:str, to_currency:str, interval:str):
    """
    Downloads historical foreign exchange rate data for a given currency pair.

    This function retrieves the historical exchange rate data between two currencies for a specified
    time interval using Yahoo Finance. The data is downloaded, processed, and formatted into a DataFrame,
    which includes the opening, high, low, closing, and adjusted closing prices, as well as additional 
    information such as the date and ticker symbols for the currency pair.

    Args:
        from_currency (str): The currency code of the base currency (e.g., 'USD' for US Dollar).
        to_currency (str): The currency code of the target currency (e.g., 'GBP' for British Pound).
        interval (str): The time interval for the data (e.g., '1d' for daily data, '1wk' for weekly data).

    Returns:
        pd.DataFrame: A DataFrame containing the foreign exchange rate data with columns for the date,
                      ticker symbol, base and target currencies, and the open, high, low, close, and adjusted
                      close prices.
    """
    fx_rate_ticker = f"{from_currency}{to_currency}=X"
    fx_rates = yf.download(fx_rate_ticker, period="ytd", interval=interval)
    fx_rates = fx_rates.reset_index()
    fx_rates["From Currency"] = from_currency
    fx_rates["To Currency"] = to_currency
    fx_rates["Ticker"] = f"{from_currency}{to_currency}=X"
    fx_rates = fx_rates[["Date","Ticker","From Currency", "To Currency", "Open", "High", "Low", "Close", "Adj Close"]]
    print(fx_rates.head())  # Inspect data
    return fx_rates
    
print(get_exchange_rate("USD", "GBP", "1d"))
print(get_exchange_rate("USD", "GBP", "1d").info())


# 2. add a function called get_stock_currency_code so that we know what currency this stock belongs to
def get_stock_currency_code(stock:str):
    """
    Retrieves the trading currency of a specific stock symbol.

    This function uses the Yahoo Finance API to fetch the stock information for the given symbol and 
    retrieves the currency used for trading that stock. The currency code is obtained from the `fast_info` 
    attribute of the `yf.Ticker` object. The result is printed, indicating the stock symbol and its corresponding
    trading currency.

    Args:
        stock (str): The stock ticker symbol (e.g., 'MSFT' for Microsoft).

    Returns:
        None: The function prints the trading currency directly, but does not return a value.
    """
    stock_info = yf.Ticker(stock)
    stock_currency = stock_info.fast_info.get("currency")
    print(f"The trading currency of {stock_info} is: {stock_currency}")

print(get_stock_currency_code("MSFT"))

#3. add function called get_news to extract_data.py so we can get relevant news belongs to that company
def get_news(stock:str):
    """
    Retrieves the latest news articles related to a specific stock symbol.

    This function uses the Yahoo Finance API to fetch news articles related to the specified stock symbol.
    It processes the news articles into a DataFrame with relevant columns, including the article's UUID, title,
    publisher, publishing time, and type. The function also adds a new column indicating the stock symbol 
    and ensures that the column names are capitalized for consistency.

    Args:
        stock (str): The stock ticker symbol (e.g., 'MSFT' for Microsoft) used to retrieve related news articles.

    Returns:
        pd.DataFrame: A DataFrame containing news articles, with columns for stock symbol, UUID, title, publisher, 
                      publishing time, type of article, and a link to the full article.
    """
    stock_info = yf.Ticker(stock)
    stock_news = stock_info.get_news()
    stock_df = pd.DataFrame(stock_news)
    stock_df["Stock"] =stock
    stock_df.columns = stock_df.columns.str.capitalize()
    stock_df = stock_df[["Stock","Uuid","Title", "Publisher", "Link", "Providerpublishtime", "Type"]]
    print(stock_df)
print(get_news("MSFT"))

# 4.Add a new python file called transform_data.py and it should round open, high, low, close columns to 2 decimal places and rename date column to trade_date
def normalize_stock_data(stock: str) -> pd.DataFrame:
    """ Normalizes stock data by rounding the 'Open', 'High', 'Low', and 'Close' columns to 2 decimal places
    and renaming the 'Date' column to 'Trade_Date'.
    
    This function assumes that `get_stock_history(stock)` returns a DataFrame with stock price history.
    The selected columns ('Open', 'High', 'Low', and 'Close') are rounded to 2 decimal places, and 
    the 'Date' column is renamed to 'Trade_Date' for better clarity and consistency.
    
    Args:
        stock (str): The stock ticker symbol (e.g., 'MSFT' for Microsoft) used to fetch historical stock data.

    Returns:
        pd.DataFrame: The DataFrame containing the normalized stock data, with rounded numerical values 
                      and the 'Date' column renamed to 'Trade_Date'.
    """
    stock_history_df = get_stock_history(stock)
    columns_to_round = ["Open", "High", "Low", "Close"]
    stock_history_df[columns_to_round] = stock_history_df[columns_to_round].round(2)
    # Rename the "Date" column to "Trade_Date"
    stock_history_df.rename(columns={"Date": "Trade_Date"}, inplace=True)
    print(stock_history_df)
print(normalize_stock_data("MSFT"))


