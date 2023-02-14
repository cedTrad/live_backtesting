import pandas as pd
import numpy as np
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pathlib

from .preprocessing import Preprocessing


from .table_trade import Trades
from .base import Base

class Journal:
    
    def __init__(self, symbol):
        self.symbol = symbol
        
        self.dataBlock = pd.DataFrame()
        self.dataLS = pd.DataFrame()
        
        self.path = "C:/Users/cc/Desktop/CedAlgo/AlgoTrading/data/"
        self.engineLS = self.engine(folder = "trade", symbol = self.symbol, nature="LS")
        

    def engine(self, symbol, folder, nature = ""):
        """
        nature : "", LS, CPPI , risk ...
        """
        path = self.path + f"{folder}/"
        engine = create_engine("sqlite:///"+path+f"{symbol}_{nature}.db")
        return engine
    
    
    def update(self, date, price, amount, quantity, value):
        self.date = date
        self.price = price
        self.amount = amount
        self.quantity = quantity
        self.value = value
        
    def journal_LS(self, trade_id, position, status, close):
        
        self.trade_id = trade_id
        
        key = str(uuid.uuid1())
        
        add = {"key" : key, 
               'date' : self.date, 
               'trade_id' : self.trade_id, 
               'price' : self.price, 
               'position' : position, 
               'status' : status, 
               'amount' : self.amount, 
               'quantity' : self.quantity, 
               'value' : self.value,
               }
        
        self.dataBlock = self.dataBlock.append(
            pd.DataFrame(add, index =['date'])
        )
        self.dataBlock['returns'] = self.dataBlock['value'].pct_change()
        self.dataBlock['cum_ret_per_trade'] = (self.dataBlock['returns'] + 1).cumprod()
        
        # -------   database    ------
        Base.metadata.create_all(self.engineLS)
        Session = sessionmaker(bind = self.engineLS)
        session = Session()
        
        ADD = self.dataBlock.iloc[-1].to_dict()
        data_i = Trades(ADD)
        
        session.add(data_i)
        session.commit()
        session.close()
        
        # -------   database    ------
        self.dataLS = self.dataLS.append(
            self.dataBlock.iloc[-1]
        )
        data = Preprocessing(symbol = self.symbol, data = self.dataLS)
        data.save(key)
        
        if close:
            self.dataBlock = pd.DataFrame()
            
        
        
        
    
    def record(self, m, floor_value, cushion, drawdown, risky_w, risky_value, safe_value, position, value):
        
        engine = self.engine(folder = "raw_trade", symbol = self.symbol, nature="cppi")
        
        add = {"date" : self.date,
               "price" : self.price,
               "quantity" : quantity,
               "m" : self.m,
               "floor_value" : self.floor_value,
               "cushion" : self.cushion,
               "drawdown" : self.drawdown,
               
               "risky_w" : self.risky_w,
               "safe_w" : self.safe_w,
               
               "risky_value" : self.risky_value,
               "safe_value" : self.safe_value,
               "status" : self.position,
               "value" : self.value
               }
        
        self.data = self.data.append(
            pd.DataFrame(add, index = [date])
        )
        
        Session = sessionmaker(bind = engine)
        session = Session()

        Base.metadata.create_all(engine)
        
        temp = cppi(add)
        session.add(temp)
        session.commit()
        
        session.close()
    
