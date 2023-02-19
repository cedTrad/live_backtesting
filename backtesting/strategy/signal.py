import pandas as pd
import numpy as np

from .indicator import *
from .strategy import Strategy

class Signal():
    
    def __init__(self, data):
        self.data = data
        self.side = {"LONG" : False, "SHORT" : False}
        self.strategy = Strategy
        self.score_long = 0
        self.score_short = 0
    
    def preprocessing(self):        
        self.data['momentum'] = self.data['log_return'].rolling(self.m).mean()
        self.data["B_B.high"], self.data["B_B.low"], self.data["B_B.mavg"] = bande_bollingers(data = self.data, window = self.b_b_p[0], wind_dev = self.b_b_p[1])
        self.data["rsi"] = rsi(self.data, period = self.rsi_p)
        self.data["sar"], self.data["sar_up"], self.data["sar_down"] = sar(self.data)
        self.data["n_day_up"] = n_day_up(self.data, period = self.n_day_up_p)
    
    
    def set_params(self, MOMENTUM : int, RSI : int, BB : tuple, DAY_UP : int):
        self.m = MOMENTUM
        self.rsi_p = RSI
        self.b_b_p = BB
        self.n_day_up_p = DAY_UP
        
        self.preprocessing()

    def position(self, bar):
        signal = self.strategy(self.data)
        positionSide = signal.momentum(bar)
        #positionSide = signal.SAR(bar)
        #positionSide = signal.RSI(bar, up = 0.8, down = 0.2)
        
        if positionSide == "LONG":
            self.side["LONG"] = True
            self.side["SHORT"] = False
            
        elif positionSide == "SHORT":
            self.side["SHORT"] = True
            self.side["LONG"] = False
            
        else:
            self.side["SHORT"] = False
            self.side["LONG"] = False
            
            
    def s_score(self, bar):
        signal = self.strategy(self.data)
        momentum = signal.momentum(bar)
        sar = signal.SAR(bar)
        rsi = signal.RSI(bar)
        
        if momentum == "LONG":
            self.score_long +=1
        elif sar == "LONG":
            self.score_long +=1
        
        
        
        


