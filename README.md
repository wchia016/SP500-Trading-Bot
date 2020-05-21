# PSAR, Bollinger Band Width and 200EMA Trading Bot

## Introduction
It is widely accepted that index investment is the best long-term investment method and that it is difficult to consistently beat the market year-on-year. However, index funding is still susceptible to negative price movements in times of high volatility which can affect the returns of an investor, especially if a new investor bought at the top. The goal of this trading bot is to ride up the natural bullish tendencies of indices while also reacting when necessary to possible sudden price falls to protect one's returns. For discussion, we will be using the S&P500 Index.

## Hypothesis

![200EMA_SP500](https://github.com/wchia016/Trading-Bot-v1/blob/master/image/200EMA_BB.png)
Generally, in times of low volatility, the tendency of the S&P500 is to be bullish. In the long run, the S&P500 is well supported by the 200EMA line and any price downswings recover rather quickly. The times when the 200EMA support are broken were when volatility started to spike. For my analysis, I proxied the measurement of volatility using the Normalized Bollinger Bandwith (BB-Width) indicator. It can be observed that when the BB-Width starts to turn sharply upwards, it is almost always followed by a sharp fall in prices. \
Hence, I concluded that in times of low volatility, it is best to long the S&P500 index due to its natural bullish tendencies. However, when volatility starts to rise rapidly, it is better to short the S&P500 or stay on the sidelines due to natural bearish tendences during periods of volatile trading. My algorithm were seek to minimize the losses from these sharp downturns.

## Technical Indicators
### Parabolic SAR

