from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date, Float, Boolean, ForeignKey

from .base import Base


class Trades(Base):
    __tablename__ = 'trades'
    identifier = Column(String, primary_key = True)
    date = Column(String)
    trade_id = Column(Integer)
    price = Column(Float)
    position = Column(Float)
    status = Column(String)
    amount = Column(Float)
    quantity = Column(Float)
    value = Column(Float)
    returns = Column(Float)
    cum_ret_per_trade = Column(Float)
    
    
    def __init__(self, add):
        self.identifier = add["key"]
        self.date = add["date"]
        self.trade_id = add["trade_id"]
        self.price = add["price"]
        self.position = add["position"]
        self.status = add["status"]
        self.amount = add["amount"]
        self.quantity = add["quantity"]
        self.value = add["value"]
        self.returns = add["returns"]
        self.cum_ret_per_trade = add["cum_ret_per_trade"]
        
    

class Trade(Base):
    #__tablename__ = "trade"
    __abstract__ = True
    identifier = Column(String, primary_key = True)
    date = Column(String)
    trade_id = Column(Integer)
    price = Column(Float)
    position = Column(Float)
    status = Column(String)
    amount = Column(Float)
    quantity = Column(Float)
    value = Column(Float)
    
    returns = Column(Float)
    cum_ret_per_trade = Column(Float)
    log_returns = Column(Float)
    price_returns = Column(Float)
    
    cum_ret = Column(Float)
    price_cum_ret = Column(Float)
    value_diff = Column(Float)
    peak = Column(Float)
    drawdown = Column(Float)
    
    def __init__(self, add):
        self.identifier = add["key"]
        self.date = add["date"]
        self.trade_id = add["trade_id"]
        self.price = add["price"]
        self.position = add["position"]
        self.status = add["status"]
        self.amount = add["amount"]
        self.quantity = add["quantity"]
        self.value = add["value"]
        
        self.returns = add['returns']
        self.cum_ret_per_trade = add['cum_ret_per_trade']
        self.log_returns = add['log_returns']
        self.price_returns = add['price_returns']
        
        self.cum_ret = add['cum_ret']
        self.price_cum_ret = add['price_cum_ret']
        self.value_diff = add['value_diff']
        self.peak = add['peak']
        self.drawdown = add['drawdown']
        


def createTable(name, table):
    tablename = name
    class_name = name
    Model = type(
        class_name, (table,), {
        '__tablename__' : tablename
    })
    
    return Model


# --------------------     Table trade list   --------------------------

LS_Data =  createTable("DataLS", Trade)
LS_Reduit = createTable("LS_reduit", Trade)
LS_Long = createTable("LS_long", Trade)
LS_Short = createTable("LS_short", Trade) 


