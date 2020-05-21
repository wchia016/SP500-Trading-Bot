# PSAR, Bollinger Band Width and 200EMA Trading Bot
## Table of Contents
- [Hypothesis](https://github.com/wchia016/Trading-Bot-v1/blob/master/README.md)
- [Technical Indicators](https://github.com/wchia016/Trading-Bot-v1/blob/master/README.md#technical-indicators)
    - [Bollinger Band Width](https://github.com/wchia016/Trading-Bot-v1/blob/master/README.md#bollinger-band-width-bb-width)
    - [Parabolic SAR](https://github.com/wchia016/Trading-Bot-v1/blob/master/README.md#parabolic-sar-psar)
    - [200 Exponential Moving Average](https://github.com/wchia016/Trading-Bot-v1/blob/master/README.md#200-exponential-moving-average-200ema)
- [Algorithm](https://github.com/wchia016/Trading-Bot-v1/blob/master/README.md#algorithm)
- [5 Year Historical Data](https://github.com/wchia016/Trading-Bot-v1/blob/master/README.md#5-year-historical-data)
- [Full Backtesting Code](https://github.com/wchia016/Trading-Bot-v1/blob/master/README.md#full-backtesting-code)

## Hypothesis
![200EMA_SP500](https://github.com/wchia016/Trading-Bot-v1/blob/master/image/200EMA_BB.png)
(Click image to expand)
\
During low volatility periods, the tendency of the S&P500 is to be Bullish. In the long run, the S&P500 is well supported by the 200EMA line and any price downswings recovers quickly. The 200EMA support is usually broken when volatility starts to spike. For my analysis, I proxied the measurement of volatility using Bollinger Bandwith (BB-Width). It can be observed that when BB-Width starts to turn sharply upwards, it is almost always followed by a sharp fall in prices.
\
\
Hence, I concluded that in times of low volatility, it is best to Long the S&P500 index due to its natural Bullish tendencies. When volatility starts to rise rapidly, it is better to Short the S&P500 or stay on the sidelines due to natural Bearish tendences during periods of volatile trading. My algorithm will seek to minimize the losses from these sharp downturns.

## Technical Indicators
### Bollinger Band Width (BB-Width)
It represents the distance between the upper and lower bands of the Bollinger Bands, normalized by dividing against the centreline of the Bollinger Bands. When volatility rises, so too does BB-Width. I use it to monitor for volatility spikes above a certain threshold which could signal an imminent price crash. I term volatility as 'High' when BB-Width crosses my divider line.
### Parabolic SAR (PSAR)
![PSAR_SP500](https://github.com/wchia016/Trading-Bot-v1/blob/master/image/PSAR_BB.png)
(Click image to expand)
\
PSAR are dots that appear above or below stock prices. When the dots are below prices (Green Dots), it indicates Bullishness. When the dots are above prices (Red Dots), it indicates Bearishness. Reversals are signalled when the dots flip over to the opposite end of prices. During periods of High BB-Width (high volatility), trend reversals signalled are generally accurate and identified trends prolonged (see Purple line & sharp price decline regions). Using PSAR to decide appropriate Long-Short positions helps position onself against large losses, potentially even profiting from volatile price movements.
\
\
However, for Low BB-Width (low volatility) periods, the rate of false reversal signals is high. In the Blue line regions, short signals are frequent but unreliable, only lasting a few trading days and prices generally continued to climb instead. Using PSAR to trade and position is likely to create more losses than gains. 
### 200 Exponential Moving Average (200EMA)
The 200EMA is natural support for the S&P500 index when uptrend. It will mainly be used to identify the overall trend of the S&P500.

## Algorithm
From repeated backtesting, I have determined 0.071 as the optimal threshold BB-Width level to decide when volatility is high. Any other values would lead to a drop in returns. Setting BB-Width any higher may delay switching to PSAR to protect against negative returns from imminent high volatility. Setting BB-Width lower may risk false signals from PSAR indicator affecting returns.
\
When BB-Width >= 0.071, PSAR will determine Long-Short positions
\
When BB-Width < 0.071, I am inclined to go Long for most situations since it would be safer to ride up the natural Bullish tendencies of the S&P500 index. I have only included 1 Short case which is when the drop in Day Lows is larger than the drop in Day Highs.

```
    if SnP['BB_width'][i] < 0.071:
        if signal == '':
            returns.append(0)
            signal = 'Long'
        
        elif signal == 'Long':
            returns.append((SnP['Adj Close'][i]-SnP['Adj Close'][i-1])/SnP['Adj Close'][i-1])
            if SnP['High'][i] < SnP['High'][i-1] and SnP['Low'][i] < SnP['Low'][i-1] and \
            abs(SnP['Low'][i] - SnP['Low'][i-1]) > abs(SnP['High'][i] - SnP['High'][i-1]):
                signal = 'Short'
            else:
                continue
        
        elif signal == 'Short':
            returns.append((SnP['Adj Close'][i-1]-SnP['Adj Close'][i])/SnP['Adj Close'][i])
            if SnP['High'][i] < SnP['High'][i-1] and SnP['Low'][i] < SnP['Low'][i-1] and \
            abs(SnP['Low'][i] - SnP['Low'][i-1]) > abs(SnP['High'][i] - SnP['High'][i-1]):
                signal = 'Short'
            else:
                signal = 'Long'
        
    elif SnP['BB_width'][i] >= 0.071:  #Use PSAR
        if signal == '':
            returns.append(0)
            if SnP['PSAR Trend'][i] == 'Up':
                signal = 'Long'
            elif SnP['PSAR Trend'][i] == 'Down':
                signal = 'Short'
        
        elif signal == 'Long':
            returns.append((SnP['Adj Close'][i]-SnP['Adj Close'][i-1])/SnP['Adj Close'][i-1])
            if SnP['PSAR Trend'][i] == 'Down':
                signal = 'Short'
            else:
                continue
            
        elif signal == 'Short':
            returns.append((SnP['Adj Close'][i-1]-SnP['Adj Close'][i])/SnP['Adj Close'][i])
            if SnP['PSAR Trend'][i] == 'Up':
                signal = 'Long'
            else:
                continue
  ```
## 5-Year Historical Data
![Returns](https://github.com/wchia016/Trading-Bot-v1/blob/master/image/s%26p500_vs_cumul_ret.png)
(Click image to expand)
\
Ticker | ^GSPC | SPY | ALgorithm
--- | --- | --- | ---
**CAGR** | 8.26% | 9.05% | 20.54%
**Sharpe** | - | 0.59 | 0.93

Data Sources: [Morningstar](https://www.morningstar.com/etfs/arcx/spy/performance) and [DQYDJ](https://dqydj.com/sp-500-return-calculator/)
 
Comparing with the volatile price swings of the S&P500, the algorithm successfully reduced the flucutations in cumulative returns. Upon reaching the recent crash in price in Feb-March 2020, cumulative returns shot up unlike the S&P500 which declined more than 50% before recovering. This also suggests that the algorithm has succeeded in protecting against negative price swings. Moving forward, I am testing this algorithm on a dummy account to ensure it holds in actual trading. 

## Full Backtesting Code
```
#-----------------------------------------------------------------------------
'List of Libraries'
import yfinance as yf
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

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

#-----------------------------------------------------------------------------
'Trading Indicators'

def PSAR(DF,initial_af=0.02 ,max_af=0.2, incr_af=0.02):
    df = DF.copy()
    
    'Initial Settings (First Row Data)'
    #We assume first row is downtrend. Doesn't matter since will auto-adjust
    trend = ['Down']                 #Direction wrt PSAR. Set first row as downtrend
    ep = [df['Low'][0]]              #Extreme Points. Downtrend: 1st EP is Day Low
    psar = [df['High'][0]]    #Actual PSAR. Downtrend: 1st PSAR is Day High          
    change_psar = [float(initial_af*(psar[0]-ep[0]))]  #PSAR(t+1) = PSAR(t) - af*(actual_PSAR - EP). Change in PSAR for next time period
    af = [float(initial_af)]         #Acceleration Factor. First af set to 0.02
      

    for i in range(1, len(df)):
        #Bearish Movement'
        if trend[i-1] == 'Down':
            psar.append(round(float(psar[i-1]-change_psar[i-1]),2)) #Formula for PSAR
            if df['High'][i] > psar[i-1]:   #Price broke above prev PSAR, reverse to Bull
                trend.append('Up')
                psar[i] = ep[i-1]                   #PSAR swaps to previous EP
                ep.append(df['High'][i-1])          #EP becomes previous High
                af.append(float(initial_af))        #Revert to initial af
            else:
                trend.append('Down')            #Remain Bearish, no change in trend
                if df['Low'][i] < ep[i-1]:      #Form a new low
                    ep.append(df['Low'][i])     #Update EP to new low
                    if af[i-1] <= round((max_af - incr_af), 2):
                        af.append(round(float((af[i-1] + incr_af)),2))  #Form new low, af increases
                    else:
                        af.append(float(max_af))#af can only increase to a max value set
                elif df['Low'][i] >= ep[i-1]:
                    ep.append(ep[i-1])          #No new EP formed
                    af.append(af[i-1])          #af doesn't increase
            change_psar.append(round(float(af[i]*(psar[i]-ep[i])),2))
        
        #Bullish Movement
        elif trend[i-1] == 'Up':
            psar.append(round(float(psar[i-1]-change_psar[i-1]),2)) #Formula for PSAR
            if df['Low'][i] < psar[i-1]:   #Price broke below prev PSAR, reverse to Bear
                trend.append('Down')
                psar[i] = ep[i-1]               #PSAR swaps to previous EP
                ep.append(df['Low'][i-1])       #EP becomes previous Low
                af.append(float(initial_af))    #Revert to initial af
            else:
                trend.append('Up')          #Remain Bullish, no change in trend
                if df['High'][i] > ep[i-1]:  #Form a new high
                    ep.append(df['High'][i])   #Update EP to new high
                    if af[i-1] <= round((max_af - incr_af), 2):
                        af.append(float(round((af[i-1] + incr_af),2)))  #Form new high, af increases
                    else:
                        af.append(float(max_af))    #af can only increase to a max value set            
                elif df['High'][i] <= ep[i-1]:
                    ep.append(ep[i-1])          #No new EP formed
                    af.append(af[i-1])          #af doesn't increase
            change_psar.append(round(float(af[i]*(psar[i]-ep[i])),2))
                
    'Updating the Dataframe'
    df['PSAR Trend'] = np.array(trend)
    df['Extreme Points'] = np.array(ep)
    df['Acceleration Factor'] = np.array(af)
    df['PSAR Delta'] = np.array(change_psar)
    df['PSAR'] = np.array(psar)
    return df


def BollB(DF,n):
    #Copy so don't edit original DF
    df = DF.copy()                                          
    df['MA']=df['Adj Close'].rolling(n).mean()                  #Create n-MA
    df['SD']=df['Adj Close'].rolling(n).std()
    df['Upper_B']=df['MA'] + (df['SD'] * 2)        #Upper band is 2sd above
    df['Lower_B']=df['MA'] - (df['SD'] * 2)        #Lower band is 2sd below
    df['BB_gap']=df['Upper_B'] - df['Lower_B']                #Distance between upper and lower bands
    df['BB_width']=df['BB_gap']/df['MA']        #Normalize the width
    df.dropna(inplace=True)
    return df

#------------------------------------------------------------------------------
'Strategy Algorithm & Backtesting'

tickers = ['^GSPC']
ohlc = retrieve_ohlc(tickers, 1825+141,'1d') #5years + 141days (take ref. from Jan 2015). 5 years only if calculate 5 year performance

#ohlc = yf.download('^GSPC', start=datetime.date.today()-datetime.timedelta(1825+141),end=datetime.date.today()-datetime.timedelta(141),interval='1d')
SnP = BollB(ohlc['^GSPC'], 20) #Try BollB Width 80
SnP = PSAR(SnP)
SnP['200EMA'] = SnP['Adj Close'].ewm(200).mean()
SnP.dropna(inplace=True)

signal = ''
returns = []

for i in range(len(SnP)):
    if SnP['BB_width'][i] < 0.071:
        if signal == '':
            returns.append(0)
            signal = 'Long'
        
        elif signal == 'Long':
            returns.append((SnP['Adj Close'][i]-SnP['Adj Close'][i-1])/SnP['Adj Close'][i-1])
            if SnP['High'][i] < SnP['High'][i-1] and SnP['Low'][i] < SnP['Low'][i-1] and abs(SnP['Low'][i] - SnP['Low'][i-1]) > abs(SnP['High'][i] - SnP['High'][i-1]):
                signal = 'Short'
            else:
                continue
        
        elif signal == 'Short':
            returns.append((SnP['Adj Close'][i-1]-SnP['Adj Close'][i])/SnP['Adj Close'][i])
            if SnP['High'][i] < SnP['High'][i-1] and SnP['Low'][i] < SnP['Low'][i-1] and abs(SnP['Low'][i] - SnP['Low'][i-1]) > abs(SnP['High'][i] - SnP['High'][i-1]):
                signal = 'Short'
            else:
                signal = 'Long'
        
    elif SnP['BB_width'][i] >= 0.071:  #Use PSAR
        if signal == '':
            returns.append(0)
            if SnP['PSAR Trend'][i] == 'Up':
                signal = 'Long'
            elif SnP['PSAR Trend'][i] == 'Down':
                signal = 'Short'
        
        elif signal == 'Long':
            returns.append((SnP['Adj Close'][i]-SnP['Adj Close'][i-1])/SnP['Adj Close'][i-1])
            if SnP['PSAR Trend'][i] == 'Down':
                signal = 'Short'
            else:
                continue
            
        elif signal == 'Short':
            returns.append((SnP['Adj Close'][i-1]-SnP['Adj Close'][i])/SnP['Adj Close'][i])
            if SnP['PSAR Trend'][i] == 'Up':
                signal = 'Long'
            else:
                continue
SnP['ret'] = np.array(returns)
SnP['PSAR_Long'] = np.where(SnP['PSAR']<SnP['Adj Close'],SnP['PSAR'],np.nan)
SnP['PSAR_Short'] = np.where(SnP['PSAR']>SnP['Adj Close'],SnP['PSAR'],np.nan)

CAGR(SnP)
sharpe(SnP,0.025)
max_dd(SnP)
(1+SnP['ret']).cumprod().plot()
```
