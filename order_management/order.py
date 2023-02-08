import pandas as pd
import numpy as np


class Order:
    
    def __init__(self, quantity, amount):
        self.quantity = quantity
        self.amount = amount
    
    def convert(self, price, amount = None, quantity = None):
        if (quantity is None) and (amount is None):
            return
        if quantity is None:
            quantity = amount / price
        if amount is None:
            amount = quantity*price
        return amount, quantity
    
    
    def buy(self, price, quantity = None, amount = None, type_ = "MARKET", side ="BUY"):
        amount, quantity = self.convert(price = price, amount = amount, quantity = quantity)
        self.quantity += quantity
        self.amount -= amount
        
        
    def sell(self, price, amount = None, quantity = None, type_ = "MARKET", side ="SELL"):
        amount, quantity = self.convert(price = price, amount = amount, quantity = quantity)
        self.quantity -= quantity
        self.amount += amount
    
    
    def re_alloc(self, date, price, new_amount = None, new_quantity = None):
        new_amount, new_quantity = self.convert(price = price, amount = new_amount, quantity = new_quantity)
        # Reduire le risky --> augmenter amount
        if new_amount > self.amount:
            self.buy(price = price, amount = new_amount)
        elif new_amount > self.amount:
            self.sell(price = price , amount = new_amount)



