import pandas as pd
import numpy as np


class Preprocessing:
    
    def __init__(self, trades):
        self.trades = trades
        self.results()
    
    def metaData(self, trades):
        #trades['returns'] = trades['value'].pct_change()
        trades['log_returns'] = np.log(trades['value']/trades['value'].shift(1))
        trades["price_returns"] = trades["price"].pct_change()
        trades["log_price_returns"] = np.log(trades["price"]/trades["price"].shift(1))
        trades.fillna(0, inplace = True)
        trades['cum_ret'] = (trades['returns'] + 1).cumprod()
        trades["price_cum_ret"] = trades["log_price_returns"].cumsum().apply(np.exp)
        trades['value_diff'] = trades['value'].diff()
        trades["win_loss"] = np.where(trades["returns"] > 0, 1, 0)
        trades['peak'] = trades['value'].cummax()
        trades['drawdown'] = (trades['value'] - trades['peak']) / trades['peak']
        trades['date'] = pd.to_datetime(trades['date'])
    
    def derivated(self):
        loc = np.where(self.trades["status"] != "-")
        self.reduit = self.trades.iloc[loc]
        
        self.reduit.drop(columns = ['returns'], inplace = True)
        self.reduit.rename(columns = {'cum_ret_per_trade' : 'returns'}, inplace = True)
        self.reduit['returns'] = self.reduit['returns'] - 1
        
        #self.reduit.loc[(self.reduit["status"] == "open_long") | (self.reduit["status"] == "open_short"), 'returns'] = 0
        
        self.long = self.reduit.loc[(self.reduit["status"] == "open_long") | (self.reduit["status"] == "close_long")]
        self.short = self.reduit.loc[(self.reduit["status"] == "open_short") | (self.reduit["status"] == "close_short")]
    
    def split(self, trades):
        trades_positif = trades.loc[trades['returns'] > 0]
        trades_negatif = trades.loc[trades['returns'] < 0]
        return trades_positif, trades_negatif
    
    def splitTrades(self):
        self.dataLS_positif , self.dataLS_negatif = self.split(self.dataLS)
        self.LS_reduit_positif , self.LS_reduit_negatif = self.split(self.LS_reduit)
        self.LS_long_positif , self.LS_long_negatif = self.split(self.LS_long)
        self.LS_short_positif , self.LS_short_negatif = self.split(self.LS_short)
    
    def results(self):
        self.derivated()
        self.metaData(self.trades)
        self.metaData(self.reduit)
        self.metaData(self.long)
        self.metaData(self.short)
        
    
    
    
        