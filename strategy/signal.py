import pandas as pd
import numpy as np

from .strategy import Strategy
from .indicator import *

class Signal():
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.side = {"LONG" : False, "SHORT" : False}
        self.strategy = Strategy
        
    
    def preprocessing(self, data):        
        data['momentum'] = data['log_returns'].rolling(self.m).mean()
        data["B_B.high"], data["B_B.low"], data["B_B.mavg"] = bande_bollingers(data = data, window = self.b_b_p[0], wind_dev = self.b_b_p[1])
        data["rsi"] = rsi(data, period = self.rsi_p)
        data["sar"], data["sar_up"], data["sar_down"] = sar(data)
        data["n_day_up"] = n_day_up(data, period = self.n_day_up_p)
        return data
    
    
    def set_params(self, momentum : int, rsi : int, bb : tuple, day_up : int):
        self.m = momentum
        self.rsi_p = rsi
        self.b_b_p = bb
        self.n_day_up_p = day_up
        
        
    
    def position(self, data):
        data = self.preprocessing(data)
        signal = self.strategy(data)
        
        positionSide = signal.momentum()
        #positionSide = signal.SAR()
        
        if positionSide == "LONG":
            self.side["LONG"] = True
            self.side["SHORT"] = False
            
        elif positionSide == "SHORT":
            self.side["SHORT"] = True
            self.side["LONG"] = False
            
        else:
            self.side["SHORT"] = False
            self.side["LONG"] = False
        



