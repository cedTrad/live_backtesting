import pandas as pd
import numpy as np
import uuid

import pathlib


class Journal:
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.dataLS = pd.DataFrame()
        self.dataLS_block = pd.DataFrame()
        self.dataCPPI = pd.DataFrame()
    
    def update(self, date, price, amount, quantity):
        self.date = date
        self.price = price
        self.amount = amount
        self.quantity = quantity
        
    def journal_LS(self, trade_id, position, status, close=False):
        self.trade_id = trade_id
        self.value = (self.quantity * self.price) + self.amount
        
        key = str(uuid.uuid1())
        
        add = { 
               'date' : self.date, 
               'trade_id' : self.trade_id, 
               'price' : self.price, 
               'position' : position, 
               'status' : status, 
               'amount' : self.amount, 
               'quantity' : self.quantity, 
               'value' : self.value
               }
        
        self.dataLS_block = self.dataLS_block.append(
            pd.DataFrame(add, index = [self.date])
        )
        self.dataLS_block['returns'] = self.dataLS_block['value'].pct_change()
        self.dataLS_block['cum_ret_per_trade'] = (self.dataLS_block['returns'] + 1).cumprod()
        
        if close:
            self.dataLS = self.dataLS.append(self.dataLS_block)
            self.dataLS_block = pd.DataFrame()
    
    def journalCPPI(self, m, floor_value, cushion, drawdown, risky_w, risky_value, safe_value, position, value):
        
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
        
        self.dataCPPI = self.dataCPPI.append(
            pd.DataFrame(add, index = [date])
        )
        
    
