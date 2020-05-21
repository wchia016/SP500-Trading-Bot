# PSAR, Bollinger Band Width and 200EMA Trading Bot

## Hypothesis
![200EMA_SP500](https://github.com/wchia016/Trading-Bot-v1/blob/master/image/200EMA_BB.png)
Generally, in times of low volatility, the tendency of the S&P500 is to be bullish. In the long run, the S&P500 is well supported by the 200EMA line and any price downswings recover rather quickly. The times when the 200EMA support are broken were when volatility started to spike. For my analysis, I proxied the measurement of volatility using the Normalized Bollinger Bandwith (BB-Width) indicator. It can be observed that when the BB-Width starts to turn sharply upwards, it is almost always followed by a sharp fall in prices.
\
\
Hence, I concluded that in times of low volatility, it is best to long the S&P500 index due to its natural Bullish tendencies. However, when volatility starts to rise rapidly, it is better to short the S&P500 or stay on the sidelines due to natural Bearish tendences during periods of volatile trading. My algorithm were seek to minimize the losses from these sharp downturns.

## Technical Indicators
### Bollinger Band Width (BB-Width)
It represents the distance between the upper and lower bands of the Bollinger Bands, normalized by dividing against the centreline of the Bollinger Bands. When volatility rises, so too does BB-Width. Hence, I use it to monitor for volatility spikes above a certain threshold which could signal an imminent crash. I term volatility as 'High' when BB-Width crosses my divider line.
### Parabolic SAR (PSAR)
![PSAR_SP500](https://github.com/wchia016/Trading-Bot-v1/blob/master/image/PSAR_BB.png)
PSAR are dots that appear above or below stock prices. They are commonly used to trade trends and their reversals. When the dots are below prices (Green Dots), it indicates Bullishness. When the dots are above prices (Red Dots), it indicates Bearishness. Reversals are signalled when the dots flip over to the opposite end of prices. During periods of High BB-Width (high volatility), trend reversals signalled are generally accurate and identified trends prolonged (see Purple line & sharp price decline regions). Using PSAR to decide appropriate Long-Short positions helps position onself against large losses, potentially even profiting from volatile price movements.
\
\
However, for Low BB-Width (low volatility) periods, the rate of false reversal signals is high. In the Blue line regions, short signals are frequent but unreliable, only lasting a few trading days and prices generally continued to climb instead. Using PSAR would be bad as it would amplify our losses.  
### 200 Exponential Moving Average (200EMA)
Due to the 200EMA being the natural support for the S&P500 index, it is mainly used to identify the overall trend of S&P500. It will be viewed together with BB-Width to see if price downswings are minor or potential sharp declines that can breach the support.

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
