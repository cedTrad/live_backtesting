import pandas as pd
import numpy as np

from datetime import datetime
import time

import zmq

from asset import Asset
from execute import AssetObj

from data.journal import Journal
from risk.risk_strategy import CPPI
from strategy.signal import Signal


class App:
    
    def __init__(self, symbols):
        self.symbols = symbols
        self.trade_id = 0
        
        self.data_1 = pd.DataFrame()
        self.data_2 = pd.DataFrame()
        self.data_3 = pd.DataFrame()
    
    
    def connect_server(self, symbol):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect('tcp://127.0.0.1:8080')
        socket.setsockopt_string(zmq.SUBSCRIBE, symbol)
        return socket
    
    
    def get_data(self, socket):
        data = socket.recv_string()
        _, date , opEn, high , low, close, volume, stop = data.split()
        date = datetime.fromtimestamp(float(date))
        date = date.strftime("%Y-%m-%d %H:%M")
        d = {'open':float(opEn), 'low':float(low),
            'high':float(high), 'close':float(close), 'volume':float(volume)}
        return date, d
    
    def preprocessing(self, data):
        data['returns'] = data['close'].pct_change()
        data['log_returns'] = np.log(data['close']/data['close'].shift(1))
        data['cum_ret'] = data['log_returns'].cumsum().apply(np.exp)
        
    
    def run(self):
        
        # INITIALISATION
        
        SYMBOL_1 = self.symbols[0]
        SYMBOL_2 = self.symbols[1]
        SYMBOL_3 = self.symbols[2]
        
        socket_1 = self.connect_server(symbol = SYMBOL_1)
        socket_2 = self.connect_server(symbol = SYMBOL_2)
        socket_3 = self.connect_server(symbol = SYMBOL_3)
        
        #       Signal
        SIGNAL_1 = Signal(SYMBOL_1)
        SIGNAL_1.set_params(MOMENTUM = 3, RSI = 7, BB = (7, 3), DAY_UP = 7)
        
        SIGNAL_2 = Signal(SYMBOL_2)
        SIGNAL_2.set_params(MOMENTUM = 3, RSI = 7, BB = (7, 3), DAY_UP = 7)
        
        SIGNAL_3 = Signal(SYMBOL_3)
        SIGNAL_3.set_params(MOMENTUM = 3, RSI = 7, BB = (7, 3), DAY_UP = 7)
        
        #       Object
        self.asset_1 = AssetObj(symbol = SYMBOL_1, quantity = 0, amount = 100, signal = SIGNAL_1)
        self.asset_2 = AssetObj(symbol = SYMBOL_2, quantity = 0, amount = 100, signal = SIGNAL_2)
        self.asset_3 = AssetObj(symbol = SYMBOL_3, quantity = 0, amount = 100, signal = SIGNAL_3)
        
        self.my_asset_obj = [self.asset_1, self.asset_2, self.asset_3]
        
        print('wait ...')
        while True:
            
            #           load data
            date_1 , data_1 = self.get_data(socket_1)
            self.data_1 = self.data_1.append(
                pd.DataFrame(data = data_1, index = [date_1])
            )
            self.preprocessing(data = self.data_1)
            
            date_2 , data_2 = self.get_data(socket_2)
            self.data_2 = self.data_2.append(
                pd.DataFrame(data = data_2, index = [date_2])
            )
            self.preprocessing(data = self.data_2)
            
            date_3 , data_3 = self.get_data(socket_3)
            self.data_3 = self.data_3.append(
                pd.DataFrame(data = data_3, index = [date_3])
            )
            self.preprocessing(data = self.data_3)
            
            
            #   Run
            price_1 = data_1["close"]
            self.asset_1.signal.position(self.data_1)
            self.asset_1.execute(date_1, price_1, c = self.data_1['momentum'].iloc[-1])
            print("-btc")
            
            