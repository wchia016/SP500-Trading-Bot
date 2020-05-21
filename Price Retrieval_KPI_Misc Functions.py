'Credits given to the following resources:'
'Algorithmic Trading & Quantitative Analysis Using Python (Mayank Rasu): https://www.udemy.com/course/algorithmic-trading-quantitative-analysis-using-python/' 

'Some codes were referenced from the above-mentioned sources'
'Codes may have been edited and updated to better serve personal uses'
'                                                                        -Chia Wei Fong'

#-----------------------------------------------------------------------------
'List of Libraries'
import yfinance as yf
import datetime
import numpy as np
import pandas as pd

#-----------------------------------------------------------------------------
'List of KPI Functions'
#Daily Trade Use: Adjust parameters where appropriate
#Trading days in a year: 252


def CAGR(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    n = len(df)/(252)
    CAGR = (df["cum_return"].tolist()[-1])**(1/n) - 1
    return CAGR

def volatility(DF):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    vol = df["ret"].std() * np.sqrt(252)
    return vol

def sharpe(DF,rf):
    "function to calculate sharpe ratio ; rf is the risk free rate"
    df = DF.copy()
    sr = (CAGR(df) - rf)/volatility(df)
    return sr
    
def max_dd(DF):
    "function to calculate max drawdown"
    df = DF.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    df["drawdown_pct"] = df["drawdown"]/df["cum_roll_max"]
    max_dd = df["drawdown_pct"].max()
    return max_dd

#-----------------------------------------------------------------------------
'Retrieving OHLC Data'

def retrieve_ohlc(tickers, t_delta,interval='1d'):
    'function to generate DF of price data up to t_delta days back'
    df = pd.DataFrame()
    ohlc_dict = {}  #Dictionary holding DF of tickers ohlc
    tries = 0       #Set number of passthroughs allowed during OHLC search
    extracted = []  #List of tickers successfully processed
    
    while len(tickers) != 0 and tries <= 3:
        tickers = [t for t in tickers if t not in extracted]
        for i in tickers:
            print('Retrieving price data for: ', i)
            try:
                df = yf.download(i, start=datetime.date.today()-datetime.timedelta(t_delta),end=datetime.date.today(),interval=interval)
                ohlc_dict[i] = df
                extracted.append(i)
            except:
                print('Failed to retrieve price data for: ',i)
                continue
    tries += 1
    return ohlc_dict
