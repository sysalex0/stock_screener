import yfinance as yf
from pandas_datareader import data as pdr

from utils.datetime_utils import get_period

yf.pdr_override()


def get_stock_historical_price_data(date, stock_ticker, days=365):
    start_date, end_date = get_period(date, days)
    df = pdr.get_data_yahoo(stock_ticker, start=start_date, end=end_date)
    df = df.drop(['High', 'Low', 'Open', 'Close'], axis=1)
    df = df.rename(columns={'Adj Close': "adjusted_close"})

    if len(df) < 2:
        raise Exception(f'[{stock_ticker}] does not have enough historical price data')
    return df
