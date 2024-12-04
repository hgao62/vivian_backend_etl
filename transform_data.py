import yfinance as yf
import pandas as pd
import numpy as np
from extract_data import get_stock_history
from extract_data import get_stock_currency_code
from extract_data import get_exchange_rate

def add_stock_returns(stock_history:pd.DataFrame) -> pd.DataFrame:
    """
    This function adds two columns to stock_history data frame
        a. "daily_return": this is caluclated using the "close" price column, google "how to calcualte daily return pandas"
        b. "cummulative_return": this is caculated using the "daily_return" caculated from step above(see stackoverflow below)
        https://stackoverflow.com/questions/35365545/calculating-cumulative-returns-with-pandas-dataframe
    """
    stock_history['daily_return'] = np.nan  # Initialize column
    stock_history['cumulative_return'] = np.nan
    for row_index in range(len(stock_history)-1):
        if row_index == 0:     
            # Initialize first row cumulative return to 0
            stock_history.loc[row_index, 'cumulative_return'] = 0
        else:
            yesterday_close_price = stock_history.iloc[row_index-1]["Close"]
            today_close_price = stock_history.iloc[row_index]["Close"]
            # Calculate Daily Return and assign it to the current row's 'Daily Return' column
            stock_history.loc[row_index,'daily_return'] = (today_close_price - yesterday_close_price) / yesterday_close_price * 100  

            # Calculate Cumulative Return and assign it to the current row's 'cumulativereturn' column
            prev_cum_return = stock_history.loc[row_index - 1, 'cumulative_return']
            daily_return = stock_history.loc[row_index, 'daily_return']/100
            stock_history.loc[row_index, "cumulative_return"] = prev_cum_return + daily_return*(1 + prev_cum_return)       
    return stock_history


def standardize_price_to_usd(
        stock_history:pd.DataFrame, 
        stock:str,
        stock_currency_code: str, 
        exchange_rate: pd.DataFrame = None
    ) -> pd.DataFrame:
    """
    Standardize the stock prices to USD by converting the 'Close' price column using exchange rates.
    """
    # Add stock returns
    added_stock_returns = add_stock_returns(stock_history)

    # Get the stock's currency code
    stock_currency_code = get_stock_currency_code(stock)

    # Fetch the exchange rate from stock currency to USD
    exchange_rate = get_exchange_rate(from_currency = stock_currency_code, to_currency = "USD",  interval="1d", period=len(added_stock_returns))

    # Extract the scalar exchange rate value (e.g., for a single day)
    #exchange_rate_value = exchange_rate.loc[:, "Close"].iloc[0]
    exchange_rate_values = exchange_rate["Close"].values

     # Align exchange rate with stock data (ensure the lengths match)
    if len(exchange_rate_values) == 0:
        raise ValueError("No exchange rate data available.")
    if len(exchange_rate_values) != len(added_stock_returns):
        print(f"Warning: Length of exchange rate data ({len(exchange_rate_values)}) does not match stock history data ({len(added_stock_returns)})")
    
    """
    Question: Unable to retrieve the exchange rate, why?
    """
    # Calculate USD close price
    added_stock_returns["usd_close_price"] = added_stock_returns["Close"] * (1 / exchange_rate_values)

    # Add currency code column
    added_stock_returns["currency_code"] = stock_currency_code
   
    return added_stock_returns


if __name__ == "__main__":
    stock_history = get_stock_history("MSFT")
    print(stock_history)

    calculated_stock_daily_return = add_stock_returns(stock_history)
    print(calculated_stock_daily_return)

    stock_history_usd = get_stock_history("SHOP.TO")
    print(stock_history_usd)

    stock_currency_code = get_stock_currency_code("SHOP.TO")
    print(stock_currency_code)
    
    # Convert to USD
    interval = "1d"
    period = len(stock_history_usd)

    exchange_rate = get_exchange_rate(stock_currency_code, "USD", interval, period)
    print(exchange_rate)

    stock_history = get_stock_history("SHOP.TO")
    stock = "SHOP.TO"

    converted_usd = standardize_price_to_usd(
        stock_history,
        stock,
        stock_currency_code,
        exchange_rate
    ) 
    print(converted_usd)

   



