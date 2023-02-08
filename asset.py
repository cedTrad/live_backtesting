import pandas as pd
import numpy as np

from order_management.order import Order


from utils import Token

class Asset(Order):
    
    def __init__(self, symbol, quantity, amount):
        
        Order.__init__(self, quantity, amount)
        
        self.symbol = symbol
        self.position = 0
        
    
    def update(self, price):
        self.value = self.quantity * price + self.amount
    
    
    def open_long(self, price, amount = None):
        if amount is None:
            self.buy(price = price, amount = self.amount)
        else:
            self.buy(price = price, amount = amount)
        self.position = 1
        self.update(price)

        
    def close_long(self, price, quantity = None):
        if quantity is None:
            self.sell(price = price, quantity = self.quantity)
        else:
            self.sell(price = price, quantity = quantity)    
        self.position = 0
        self.update(price)
        
        
    def open_short(self, price, amount = None):
        if amount is None:
            self.sell(price = price, amount = self.amount)
        else:
            self.sell(price = price, amount = amount)
        self.position = -1
        self.update(price)
        
        
    def close_short(self, price, quantity = None):
        if quantity is None:
            self.buy(price = price, quantity = self.quantity)
        else:
            self.buy(price = price, quantity = quantity)
        self.position = 0
        self.update(price)
        
        
    def following(self, price):
        self.update(price)
        
        