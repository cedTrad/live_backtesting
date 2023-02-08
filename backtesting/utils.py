
import pandas

class Token:
    
    def __init__(self, name, quantity, amount):
        self.name = name
        self.base = "USDT"
        self.symbol = self.pair()
        self.quantity = quantity
        self.amount = amount
        
    def pair(self):
        return self.name+self.base
    
    def current_value(self, price):
        return self.quantity * price + self.amount
    
    def update(self, price, quantity, amount):
        self.quantity = quantity
        self.amount = amount
        self.value = self.current_value(price)
        