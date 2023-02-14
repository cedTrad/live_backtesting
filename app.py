import pandas as pd
import numpy as np

from datetime import datetime
import time

import zmq

from asset import Asset
from execute import AssetObj
from portfolio import Portfolio

from strategy.signal import Signal

from risk_management.risk_strategy import CPPI
from risk_management.money_management import Money_management

from data.journal import Journal


class App:
    
    def __init__(self, symbols):
        self.symbols = symbols
        self.trade_id = 0
        
        self.portfolio = Portfolio(symbols = symbols)
        
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
        
    
    def config_asset(self, symbol, initial_amount, risky_amount, stopLoss, takeProfit, leverage = 1):
        SIGNAL = Signal(symbol)
        SIGNAL.set_params(MOMENTUM = 3, RSI = 7, BB = (7, 3), DAY_UP = 7)
        
        money_m = Money_management(symbol = symbol)
        money_m.config(risky_amount = risky_amount, stopLoss = stopLoss, takeProfit = takeProfit, leverage = leverage)
        
        asset = AssetObj(symbol = symbol, amount = initial_amount, signal = SIGNAL)
        return asset, money_m
    
    
    def on(self, asset, date, price, data, symbol):
        asset.signal.position(data)
        asset.execute(date, price)
        print("- ",symbol)
        
    
    def run(self):
        
        # INITIALISATION
        
        SYMBOL_1 = self.symbols[0]
        SYMBOL_2 = self.symbols[1]
        SYMBOL_3 = self.symbols[2]
        
        socket_1 = self.connect_server(symbol = SYMBOL_1)
        socket_2 = self.connect_server(symbol = SYMBOL_2)
        socket_3 = self.connect_server(symbol = SYMBOL_3)
        
        self.asset_1 , self.money_m_1 =self.config_asset(symbol = SYMBOL_1, initial_amount = 100,
                                                         risky_amount = 100, stopLoss = 0.01, takeProfit = 0.05)
        self.asset_2 , self.money_m_2 =self.config_asset(symbol = SYMBOL_2, initial_amount = 100,
                                                         risky_amount = 100, stopLoss = 0.01, takeProfit = 0.05)
        self.asset_3 , self.money_m_3 =self.config_asset(symbol = SYMBOL_3, initial_amount = 100,
                                                         risky_amount = 100, stopLoss = 0.01, takeProfit = 0.05)
        
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
            
            price_1 = data_1["close"]
            price_2 = data_2["close"]
            price_3 = data_3["close"]
            
            #   Run
            self.on(asset = self.asset_1, date = date_1, price = price_1, data = self.data_1, symbol = SYMBOL_1)
            self.on(asset = self.asset_2, date = date_2, price = price_2, data = self.data_2, symbol = SYMBOL_2)
            self.on(asset = self.asset_3, date = date_3, price = price_3, data = self.data_3, symbol = SYMBOL_3)
            
            # Update
            self.portfolio.update_account(assetObjs = self.my_asset_obj)
            