import pandas as pd
import numpy as np

import scipy.stats
from scipy.stats import norm


# ----------            ------------

def pnl(r):
    x = (1 + r).prod()
    return x

def mean_(r):
    if len(r) == 0:
        return 0
    else:
        x = (1+r).prod()
        return x**(1/len(r))

def position_stats(r):
    '''
    min , 25%, median, mean , 75%, max
    '''
    if len(r)>8:
        avg = mean_(r)
        return r.min() , np.percentile(r, 0.25), np.percentile(r, 0.5), avg, np.percentile(r, 0.75), r.max()
    else:
        return 0, 0, 0, 0, 0, 0

def kurtosis(r):
    if len(r) > 8:
        return scipy.stats.kurtosis(r)
    else:
        return 0

def skewness(r):
    if len(r) > 8:
        return scipy.stats.skew(r)
    else:
        return 0

# ----------            ------------

def win_loss_stat(trades):
    if len(trades) >= 2:
        trades.fillna(0, inplace = True)
        sum_ = trades['value_diff'].sum()
        avg_ = trades['value_diff'].mean()
        ret_avg_ = mean_(trades['returns'])
        ret_ = trades.iloc[-1]['cum_ret']
        amount_ = trades.iloc[-1]["value"]
        return avg_, sum_, ret_, ret_avg_, amount_
    else:
        return 0, 0, 0, 0, 0

def expectancy(win_rate, avg_win, avg_loss):
    return win_rate*avg_win + (1 - win_rate)*avg_loss

def george(win_rate , avg_win, avg_loss):
    return (1 + avg_win)**win_rate * (1 + avg_loss)**(1 - win_rate) - 1



# ----------            ------------

def drawdown(r):
    cum_r = (1 + r).cumprod()
    peak = cum_r.max()
    drawdowns = (cum_r - peak)/peak
    return drawdowns.min()


def var_historic(r, level=0.05):
    if len(r) > 5:
        return -np.percentile(r, level)


def var_gaussian(r, level=0.05, modified = False):
    if len(r) > 15:
        z = norm.ppf(level/100)
        if modified:
            s = scipy.stats.skewness(r)
            k = scipy.stats.kurtosis(r)
            z = ( z + 
                (z**2 - 1)*s/6 +
                (z**3 - 3*z)*(k-3)/24 -
                (2*z**3 - 5*z)*(s**2)/36
            )
        return -(r.mean() + z*r.std(ddof=0))
    else:
        return 0


def cvar_historic(r, level=0.05):
    if len(r)>5:
        is_beyond = r<= var_historic(r, level)
        return -r[is_beyond].mean()
    else:
        return 0


def volatility(r):
    return


def results():
    "Benefice"
    
    
    "Perte"
    
    
    "average profit"
    
    
    "average loss"
    
    
    "Profit factor"
    
    
    "Rapport Risk Recompense , RRR"
    
    
    "BreakEvent hit ratio"