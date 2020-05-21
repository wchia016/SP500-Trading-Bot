# PSAR, Bollinger Band Width and 200EMA Trading Bot

## Hypothesis
![200EMA_SP500](https://github.com/wchia016/Trading-Bot-v1/blob/master/image/200EMA_BB.png)
During low volatility periods, the tendency of the S&P500 is to be Bullish. In the long run, the S&P500 is well supported by the 200EMA line and any price downswings recovers quickly. The 200EMA support is usually broken when volatility starts to spike. For my analysis, I proxied the measurement of volatility using Bollinger Bandwith (BB-Width). It can be observed that when BB-Width starts to turn sharply upwards, it is almost always followed by a sharp fall in prices.
\
\
Hence, I concluded that in times of low volatility, it is best to Long the S&P500 index due to its natural Bullish tendencies. When volatility starts to rise rapidly, it is better to Short the S&P500 or stay on the sidelines due to natural Bearish tendences during periods of volatile trading. My algorithm will seek to minimize the losses from these sharp downturns.

## Technical Indicators
### Bollinger Band Width (BB-Width)
It represents the distance between the upper and lower bands of the Bollinger Bands, normalized by dividing against the centreline of the Bollinger Bands. When volatility rises, so too does BB-Width. I use it to monitor for volatility spikes above a certain threshold which could signal an imminent price crash. I term volatility as 'High' when BB-Width crosses my divider line.
### Parabolic SAR (PSAR)
![PSAR_SP500](https://github.com/wchia016/Trading-Bot-v1/blob/master/image/PSAR_BB.png)
PSAR are dots that appear above or below stock prices. When the dots are below prices (Green Dots), it indicates Bullishness. When the dots are above prices (Red Dots), it indicates Bearishness. Reversals are signalled when the dots flip over to the opposite end of prices. During periods of High BB-Width (high volatility), trend reversals signalled are generally accurate and identified trends prolonged (see Purple line & sharp price decline regions). Using PSAR to decide appropriate Long-Short positions helps position onself against large losses, potentially even profiting from volatile price movements.
\
\
However, for Low BB-Width (low volatility) periods, the rate of false reversal signals is high. In the Blue line regions, short signals are frequent but unreliable, only lasting a few trading days and prices generally continued to climb instead. Using PSAR to trade and position is likely to create more losses than gains. 
### 200 Exponential Moving Average (200EMA)
The 200EMA is natural support for the S&P500 index when uptrend. I mainly use it to identify the overall trend of the S&P500.

## Algorithm
From repeated backtesting, I have determined 0.071 as the optimal threshold BB-Width level to decide when volatility is high.
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
## Results
![Returns](https://github.com/wchia016/Trading-Bot-v1/blob/master/image/s%26p500_vs_cumul_ret.png)
Ticker | ^GSPC | SPY | ALgorithm
--- | --- | --- | ---
**CAGR** | 8.26% | 9.05% | 20.54%
**Sharpe** | - | 0.59 | 0.93

Data Sources: [Morningstar](https://www.morningstar.com/etfs/arcx/spy/performance) and [DQYDJ](https://dqydj.com/sp-500-return-calculator/)
\ 
