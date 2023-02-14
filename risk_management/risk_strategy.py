import pandas as pd
import numpy as np

class CPPI:
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.data = pd.DataFrame()
        
    
    def set_parameters(self, m, floor, drawdown = None):
        self.m = m
        self.floor = floor
        self.drawdown = drawdown
    
    
    def update(self, date, price):
        self.date = date
        self.price = price
      
      
    def execute(self, value):
        self.value = value
        
        if self.drawdown is not None:
            peak = np.maximum(self.value , peak)
            self.floor_value = (1 - self.drawdown)*peak
        else:
            self.floor_value = self.value*self.floor
            
        # Cushion
        self.cushion = (self.value - self.floor_value)/self.value
        
        # Risky_weight
        self.risky_w = self.m * self.cushion
        
        # Borner risky_w, leverage
        self.risky_w = np.minimum(self.risky_w, 1)
        self.risky_w = np.maximum(self.risky_w, 0)
        self.safe_w = 1 - self.risky_w
        
        self.risky_value = self.value * self.risky_w
        self.safe_value = self.value * self.safe_w
        
        # Quantity
        self.quantity = self.risky_value / self.price
        self.amount = self.safe_value
        
        
        
        
