# -*- coding: utf-8 -*-
"""
Created on Sat May 16 12:32:48 2020

@author: Wei Fong
"""
'Editing of Orignal Slope Function by Mayank Rasu: https://www.udemy.com/course/algorithmic-trading-quantitative-analysis-using-python/'
'Added simple trend generator so as to process indicators like RSI, OBV, etc and determine direction algorithmically rather than using charting'

def slopetrends(DF,n):
    'Calculate the slope angles'
    df = DF.copy()
    ser = df['Adj Close']
    slopes = [i*0 for i in range(n-1)]      #for 1st to (n-1), we don't generate slope since insufficient data
    for i in range(n,len(ser)+1):               
        y = ser[i-n:i]                      #Generate slope for every n datapoints
        x = np.array(range(n))              #x is just TimeSeries (index are time), we can just use 1,2,3,4,5
        y_scaled = (y - y.min())/(y.max() - y.min())    #Scaling y values
        x_scaled = (x - x.min())/(x.max() - x.min())    #Scaling x values
        x_scaled = sm.add_constant(x_scaled) #Default is y=mx, we add constant (y=mx+c). Diff 5 datapoints, diff timestamp, diff slopes, not all slopes pass thru origin
        model = sm.OLS(y_scaled,x_scaled)   #OLS is function for linreg
        results = model.fit()               #Fit a linreg
        slopes.append(results.params[-1])   #.params gives array of constant & coeff of x: [-1] since we only need coeff of x
    slope_angle = (np.rad2deg(np.arctan(np.array(slopes)))) #Convert radian to deg using trigo (arctan)
    df['Slope Angle'] = np.array(slope_angle)   #input slope angle into DF
    
    'Determine if flat, uptrend or downtrend'
    trend = []
    for i in range(len(df)):
        if df['Slope Angle'][i] == 0:
            trend.append('flat')
        elif df['Slope Angle'][i] > 0:
           trend.append('up')
        elif df['Slope Angle'][i] < 0:
           trend.append('down')
    df['Trend'] = np.array(trend)
    return df.iloc[n-1:,:]      #Drop first n rows with no slope angle reading
