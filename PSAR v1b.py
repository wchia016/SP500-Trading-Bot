# -*- coding: utf-8 -*-
"""
Created on Sat May 16 12:31:10 2020

@author: Wei Fong
"""


'PSAR Version 2'
def psar(DF,initial_af=0.02 ,max_af=0.2, incr_af=0.02):
    'Function to calculate PSAR and determine trend'
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
    df['Trend'] = np.array(trend)
    df['Extreme Points'] = np.array(ep)
    df['Acceleration Factor'] = np.array(af)
    df['PSAR Delta'] = np.array(change_psar)
    df['PSAR'] = np.array(psar)
    return df              