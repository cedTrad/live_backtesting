import pandas as pd
import numpy as np

class Strategy:
    
    def __init__(self, data):
        self.data = data
        
    
    def momentum(self, bar):
        if self.data["momentum"].iloc[bar] > 0:
            return "LONG"
        elif self.data["momentum"].iloc[bar] < 0:
            return "SHORT"
    
    
    def BB(self, bar):
        if self.data["close"] > self.data["B_B.high"]:
            return "LONG"
        elif self.data["close"] < self.data["B_B.low"]:
            return "SHORT"
    
    
    def SAR(self, bar):
        if self.data["sar_up"].iloc[bar] > 0:
            return "LONG"
        elif self.data["sar_down"].iloc[bar] > 0:
            return "SHORT"
    
    
    def RSI(self, bar, up, down):
        if self.data["rsi"].iloc[bar] > up:
            return "LONG"
        elif self.data["rsi"].iloc[bar] < down:
            return "SHORT"    
    
    
    def tripleMA(self, bar):
        ""
        
    def tripleEMA(self, bar):
        ""
        
        
    
    def momentum_rsi(self, bar):
        ""
    
    
    
    