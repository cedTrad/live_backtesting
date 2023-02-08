import pandas as pd
import numpy as np


class Strategy:
    
    def __init__(self, data):
        self.data = data
        
    
    def momentum(self):
        if self.data["momentum"].iloc[-1] > 0:
            return "LONG"
        elif self.data["momentum"].iloc[-1] < 0:
            return "SHORT"
    
    
    
    def BB(self):
        if self.data["close"] > self.data["B_B.high"]:
            return "LONG"
        elif self.data["close"] < self.data["B_B.low"]:
            return "SHORT"
    
    
    def SAR(self):
        if self.data["sar_up"].iloc[-1] > 0:
            return "LONG"
        elif self.data["sar_down"].iloc[-1] > 0:
            return "SHORT"
        
        
    def tripleMA(self):
        ""
        
    def tripleEMA(self):
        ""
        

    def RSI(self):
        ""
    