import pandas as pd
import numpy as np

from order import Order
from utils import Token

class Asset(Order):
    
    def __init__(self, symbol, quantity, amount):        
        Order.__init__(self)
        
        self.symbol = symbol
        self.quantity = quantity
        self.amount = amount
        self.position = 0
        
    
    def current_value(self, price):
        self.value = self.quantity * price + self.amount
    
    
    def update(self, date, price):
        self.date = date
        self.price = price
        self.current_value(price)
    
    
    def open_long(self, amount = None):
        if amount is None:
            self.buy(price = self.price, amount = self.amount)
        else:
            self.buy(price = self.price, amount = amount)
        self.position = 1

        
    def close_long(self, quantity = None):
        if quantity is None:
            self.sell(price = self.price, quantity = self.quantity)
        else:
            self.sell(price = self.price, quantity = quantity)
        self.position = 0

        
        
    def open_short(self, amount = None):
        if amount is None:
            self.sell(price = self.price, amount = self.amount)
        else:
            self.sell(price = self.price, amount = amount)
        self.position = -1
        
        
    def close_short(self, quantity = None):
        if quantity is None:
            self.buy(price = self.price, quantity = self.quantity)
        else:
            self.buy(price = self.price, quantity = quantity)
        self.position = 0

