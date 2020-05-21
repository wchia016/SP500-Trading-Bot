'Credits given to the following resources:'
'Parabolic SAR in Python…PSAR keep growing instead of reversing(Greg D): https://stackoverflow.com/questions/54918485/parabolic-sar-in-python-psar-keep-growing-instead-of-reversing'
'How to Calculate the PSAR Using Excel - Revised Version (Mark Ursell): https://www.youtube.com/watch?v=MuEpGBAH7pw&t=291s'
'Parabolic SAR: https://en.wikipedia.org/wiki/Parabolic_SAR'
'Using Bollinger Bands to Gauge Trends (Cory Mitchell): https://www.investopedia.com/trading/using-bollinger-bands-to-gauge-trends/'
'Bollinger Band Width (Fidelity): https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/bollinger-band-width'
'Calculating Bollinger Band Correctly: https://quant.stackexchange.com/questions/11264/calculating-bollinger-band-correctly'
'Algorithmic Trading & Quantitative Analysis Using Python (Mayank Rasu): https://www.udemy.com/course/algorithmic-trading-quantitative-analysis-using-python/' 


'Some codes were referenced from the above-mentioned sources'
'Codes may have been edited and updated to better serve personal uses'
'                                                                        -Chia Wei Fong'

'Strategy: Chia Wei Fong'
'Overall Coding: Chia Wei Fong'
'Visualization: Chia Wei Fong'

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
ohlc = retrieve_ohlc(tickers, 1825+141,'1d') #10years + 20 days for BollB

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
#(1+SnP['ret']).cumprod().plot()

#-----------------------------------------------------------------------------
'Visualization'

df = SnP
df['Cumulative Ret'] = (1+df['ret']).cumprod()
df.reset_index(inplace=True)

#SP500 & Cumulative Returns Charts
fig1, (ax0, ax1) = plt.subplots(1,2, figsize=(21,9))
plt.style.use('dark_background')
df.plot(y='Adj Close', x='Date', color='turquoise', linewidth=0.75, ax=ax0)
df.plot(y='Cumulative Ret', x='Date', color='crimson',linewidth=0.75, ax=ax1)

ax0.set(title='S&P500 Index')
ax0.legend().set_visible(False)
ax0.set_xlabel('Year', fontsize=12)
ax0.set_ylabel('Price', fontsize=12)
ax0.tick_params(axis='both', labelsize=10)
ax0.yaxis.get_major_ticks()[1].label1.set_visible(False)

ax1.set(title='Cumulative Return with Time')
ax1.legend().set_visible(False)
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('Cumulative Ret.', fontsize=12)
ax1.tick_params(axis='both', labelsize=10)
ax1.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
#fig1.savefig('s&p500_vs_cumul_ret.png', transparent=False, dpi=80, bbox_inches="tight")


#SP500 & BB_Width + PSAR
fig2, axes = plt.subplots(2, 1, figsize=(27,16), sharex=True, sharey=False, gridspec_kw={'height_ratios':[4,1]})
df.plot(y='Adj Close', x='Date', color='turquoise', linewidth=0.75, ax=axes[0])
df.plot(y='PSAR_Long', x='Date', color='lime', linestyle=':', linewidth=2.25, ax=axes[0])
df.plot(y='PSAR_Short', x='Date', color='red', linestyle=':', linewidth=2.25, ax=axes[0])
df.plot(y='BB_width', x='Date', color='gold', linewidth=0.75, ax=axes[1])

fig2.suptitle('S&P500 Index',fontsize=25)

axes[0].set_ylabel('Price', fontsize=14)
axes[0].legend().set_visible(False)
axes[0].legend(['S&P500','PSAR_Bullish','PSAR_Bearish'], fontsize=14, loc=2)
axes[0].tick_params(axis='both', labelrotation=0, labelsize=12)

axes[1].axhline(y=0.071, color='white', linestyle='--', linewidth=1)
axes[1].yaxis.get_major_ticks()[1].label1.set_visible(False)
axes[1].set_xlabel('Year', fontsize=14)
axes[1].legend(['Normalized BB20 Width','High-Low Volatility Divider = 0.071'], fontsize=14, loc=2)
axes[1].tick_params(axis='both', labelrotation=0, labelsize=12)
#fig2.savefig('PSAR_BB', transparent=False, dpi=80, bbox_inches="tight")


#SP500 & BB_Width + 200EMA
fig3, axes = plt.subplots(2, 1, figsize=(27,16), sharex=True, sharey=False, gridspec_kw={'height_ratios':[4,1]})
df.plot(y='Adj Close', x='Date', color='turquoise', linewidth=0.75, ax=axes[0])
df.plot(y='200EMA', x='Date', color='white', linewidth=0.75, ax=axes[0])
df.plot(y='BB_width', x='Date', color='gold', linewidth=0.75, ax=axes[1])

fig3.suptitle('S&P500 Index',fontsize=25)

axes[0].set_ylabel('Price', fontsize=14)
axes[0].legend().set_visible(False)
axes[0].legend(['S&P500','200EMA'], fontsize=14, loc=2)
axes[0].tick_params(axis='both', labelrotation=0, labelsize=12)

axes[1].axhline(y=0.071, color='white', linestyle='--', linewidth=1)
axes[1].yaxis.get_major_ticks()[1].label1.set_visible(False)
axes[1].set_xlabel('Year', fontsize=14)
axes[1].legend(['Normalized BB20 Width','High-Low Volatility Divider = 0.071'], fontsize=14, loc=2)
axes[1].tick_params(axis='both', labelrotation=0, labelsize=12)
#fig3.savefig('200EMA_BB', transparent=False, dpi=80, bbox_inches="tight")
