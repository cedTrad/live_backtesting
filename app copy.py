import pandas as pd

from datetime import datetime
import time

import zmq

from asset import Asset
from execute import Execute
from trade import Trade

from data.journal import Journal
from risk.risk_strategy import CPPI
from strategy.signal import Signal


class App:
    
    def __init__(self):
        self.signal = Signal
        self.data = pd.DataFrame()
        self.trade_id = 0
        
    
    def get_date_price(self):
        self.date = str(self.data.index[-1])
        self.price = self.data.iloc[-1]["close"]
    
    
    def connect_server(self, token = "BTCUSDT"):
        token = "BTCUSDT"
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect('tcp://127.0.0.1:8080')
        socket.setsockopt_string(zmq.SUBSCRIBE, token)
        return socket
    
    
    def get_data(self, socket):
        data = socket.recv_string()
        _, date , opEn, high , low, close, volume = data.split()
        date = datetime.fromtimestamp(float(date))
        d = {'open':float(opEn), 'low':float(low),
            'high':float(high), 'close':float(close), 'volume':float(volume)}
        self.data = self.data.append(
                pd.DataFrame(data = d, index=[date])
            )
    
    
    def run(self):
        socket = self.connect_server(token = "BTCUSDT")
        
        # Initialisation
        btcusdt = Asset(symbol="BTCUSDT", quantity = 0, amount = 100)
        self.journal_btc = Journal(symbol="BTCUSDT")
        
        btcusdt_cppi = CPPI(symbol = "BTCUSDT")
        btcusdt_cppi.set_parameters(m = 3, floor = 0.8)
        
        print('wait ...')
        while True:
            #   load data
            self.get_data(socket)
            
            #   update date & price
            self.get_date_price()
            
            #   Signal
            signal = self.signal(self.data)
            signal.position()                       # 1 : Long & -1 : Short  0 : None
            positionSide = signal.side
            
            #   Update
            btcusdt.update(date = self.date, price = self.price)
            self.journal_btc.update(date = self.date, price = self.price, amount = btcusdt.amount, quantity = btcusdt.quantity)
            
            #   risky
            #   Update - cppi
            btcusdt_cppi.update(date = self.date, price = self.price)
            
            #   Long
            if (btcusdt.position == 0) and (positionSide["LONG"]):
                #btcusdt_cppi.execute(value = btcusdt.value)
                #quantity = btcusdt_cppi.quantity
                #risky_value = btcusdt_cppi.risky_value
                
                #btcusdt.open_long(amount = risky_value)
                btcusdt.open_long()
                self.journal_btc.journal_LS(trade_id = self.trade_id, position = btcusdt.position, status = "open_long")
            
            
            #   Close Short and Open Long
            elif (btcusdt.position == -1) and (positionSide["LONG"]):
                btcusdt.close_short()
                self.journal_btc.journal_LS(trade_id = self.trade_id, position = btcusdt.position, status = "close_short", close = True)
                
                
                #btcusdt_cppi.execute(value = btcusdt.value)
                #quantity = btcusdt_cppi.quantity
                #risky_value = btcusdt_cppi.risky_value
                
                #btcusdt.open_long(amount = risky_value)
                btcusdt.open_long()
                self.journal_btc.journal_LS(trade_id = self.trade_id, position = btcusdt.position, status = "open_long")
                
            
            #   Short
            elif (btcusdt.position == 0) and (positionSide["SHORT"]):
                btcusdt.open_short()
                self.journal_btc.journal_LS(trade_id = self.trade_id, position = btcusdt.position, status = "open_short")
            
            #   Close Long and Open Short
            elif (btcusdt.position == 1) and (positionSide["SHORT"]):
                #btcusdt.close_long(quantity = btcusdt.quantity)
                btcusdt.close_long()
                self.journal_btc.journal_LS(trade_id = self.trade_id, position = btcusdt.position, status = "close_long", close = True)
                
                btcusdt.open_short()
                self.journal_btc.journal_LS(trade_id = self.trade_id, position = btcusdt.position, status = "open_short")
            
            else:
                btcusdt.following()
                self.journal_btc.journal_LS(trade_id = self.trade_id, position = btcusdt.position, status = "-")
                #btcusdt_cppi.record()
                print("-")
        
    

