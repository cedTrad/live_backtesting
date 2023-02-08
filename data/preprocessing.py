import pandas as pd
import numpy as np 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .table_trade import LS_Data, LS_Reduit, LS_Long, LS_Short
from .base import Base


class Preprocessing:
    
    def __init__(self, symbol, data):
        self.dataLS = data
        
        self.path = "C:/Users/cc/Desktop/CedAlgo/AlgoTrading/data/"
        self.engineLS = self.engine(folder = "trade", symbol = symbol, nature="LS")
        
        self.results()
        
        
    def engine(self, symbol, folder, nature = ""):
        """
        nature : "", LS, CPPI , risk ...
        """
        path = self.path + f"{folder}/"
        engine = create_engine("sqlite:///"+path+f"{symbol}_{nature}.db")
        return engine
    
    def metaData(self, trades):
        try:
            trades['cum_ret_per_trade'].fillna(1, inplace = True)
        except KeyError:
            None
        trades['log_returns'] = np.log(trades['value']/trades['value'].shift(1))
        trades["price_returns"] = trades["price"].pct_change()
        trades.fillna(0, inplace = True)
        trades['cum_ret'] = (trades['returns'] + 1).cumprod()
        trades["price_cum_ret"] = (trades['price_returns'] + 1).cumprod()
        trades['value_diff'] = trades['value'].diff()
        trades['peak'] = trades['value'].cummax()
        trades['drawdown'] = (trades['value'] - trades['peak']) / trades['peak']
        #trades['date'] = pd.to_datetime(trades['date'])
    
    def derivated(self):
        loc = np.where(self.dataLS["status"] != "-")
        self.reduit = self.dataLS.iloc[loc]
        
        self.reduit.drop(columns = ['returns'], inplace = True)
        self.reduit.rename(columns = {'cum_ret_per_trade' : 'returns'}, inplace = True)
        self.reduit['returns'] = self.reduit['returns'] - 1
        self.reduit['cum_ret_per_trade'] = None
        
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
        self.metaData(self.dataLS)
        self.metaData(self.reduit)
        self.metaData(self.long)
        self.metaData(self.short)
        
    
    def to_database(self, table, data):
        if data is not None:
            Base.metadata.create_all(self.engineLS)
            
            Session = sessionmaker(bind = self.engineLS)
            session = Session()
            
            data_i = table(data)
            session.add(data_i)
            
            session.commit()
            session.close()
    
    def add(self, data, key):
        try:
            loc = np.where(data['key'] == key)
            temp = data.iloc[loc].iloc[-1]
            return temp.to_dict()
        except:
            return None
        
    
        
    def save(self, key):
        
        dataLS = self.add(self.dataLS, key)
        self.to_database(table = LS_Data, data = dataLS)
        
        reduit = self.add(self.reduit, key)
        self.to_database(table = LS_Reduit, data = reduit)
        
        long_ = self.add(self.long, key)
        self.to_database(table = LS_Long, data = long_)
        
        short_ = self.add(self.short, key)
        self.to_database(table = LS_Short, data = short_)
        
        
        