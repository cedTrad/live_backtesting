import pandas as pd
import numpy as np

import sqlalchemy
import uuid
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



class Trade:
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.orderIdList = []
        
        self.returns = 0
    
    
    def engine(self, symbol, folder, nature = ""):
        """
        nature : "", LS, CPPI , risk ...
        """
        path = self.path.joinpath(folder, symbol+"_"+nature+".db")
        engine = create_engine("sqlite:///"+str(path))
        return engine
        
    def init(self, trade_id = 0):
        self.trade_id = trade_id
        self.data = pd.DataFrame()
    
    
    def add_orderId(self, orderId):
        self.add_orderIdList.append(orderId)
        
        
    def update_value(self, date, price, quantity, amount, status):
        self.date = date
        self.price = price
        self.quantity = quantity
        self.amount = amount
        self.status = status 
        
    
    def update(self, date, price, quantity, amount, status):
        self.update_value(date = date, price = price, quantity = quantity, amount = amount, status = status)
        add = {'date' : date,
               'trade_id' : self.trade_id,
               'price' : self.price ,
               'quantity' : self.quantity,
               'amount' : self.amount,
               'status' : self.status
               }
        self.data = self.data.append(
            pd.DataFrame(add, index = [date])
        )
        

        
        
    def open(self, date, price, quantity, amount, status):
        self.update(date, price, quantity, amount, status)
        self.start = date
        self.price_in = price
        
        
    def close(self, date, price, quantity, amount, status):
        self.update(date, price, quantity, amount, status)
        self.end = date
        self.price_out = price
        self.returns = (self.price_out - self.price_in)/self.price_in
        self.log_returns = np.log(self.price_out/self.price_in)
        
        
    def MetaData(self):
        trailing = pd.read_sql("trailing", engine)
        
        current = trailing.loc[trailing["trade_id"] == self.id] 
        
        current['returns'] = current['wallet'].pct_change()
        current['log_returns'] = np.log(current['wallet']/current['wallet'].shift(1))
        current["cum_ret"] = current['log_returns'].cumsum().apply(np.exp)
        #
        #Base.metadata.create_all(engine)
        
        #add = current[col].iloc[-1].to_dict()
        
        #session.add(MetaTrailing(add))
        #session.commit()
        #session.close()
        
        
        
        