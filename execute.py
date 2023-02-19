from asset import Asset

from risk_management.risk_strategy import CPPI
from strategy.signal import Signal
from asset import Asset

from risk_management.money_management import Money_management

from data.journal import Journal


class AssetObj:
    
    def __init__(self, symbol, amount, signal, money_management, risk = None):
        self.asset = Asset(symbol = symbol, amount = amount)
        self.journal = Journal(symbol)
        self.signal = signal
        self.money_manag = money_management
        self.risk = risk
        self.trade_id = 0
        
    
    def update_and_save_LS(self, date, price, trade_id, status, close = False):
        self.journal.update(date, price, amount = self.asset.amount,
                            quantity = self.asset.quantity, value = self.asset.value)
        self.journal.journal_LS(trade_id = trade_id, status = status, close = close,
                                position = self.asset.position)
        #self.risk.update(date, price)
        
        
    def long(self, price, quantity = 0):
        "" 
        
        
    def short(self):
        ""
        
        
    def execute(self, date, price):
        
        SIDE = self.signal.side
        POSITION = self.asset.position
        
        if (POSITION == 0) and (SIDE["LONG"]):
            self.asset.open_long(price)
            self.update_and_save_LS(date, price, trade_id = 0, status = "open_long")

            
            #   Close Short and Open Long
        elif (POSITION == -1) and (SIDE["LONG"]):
            self.asset.close_short(price)
            self.update_and_save_LS(date, price, trade_id = 0, status = "close_short", close = True)
            
            self.asset.open_long(price)
            self.update_and_save_LS(date, price, trade_id = 0, status = "open_long")
                
            #   Short
        elif (POSITION == 0) and (SIDE["SHORT"]):
            self.asset.open_short(price)
            self.update_and_save_LS(date, price, trade_id = 0, status = "open_short")
            
            
        #   Close Long and Open Short
        elif (POSITION == 1) and (SIDE["SHORT"]):
            self.asset.close_long(price)
            self.update_and_save_LS(date, price, trade_id = 0, status = "close_long", close = True)
            
            self.asset.open_short(price)
            self.update_and_save_LS(date, price, trade_id = 0, status = "open_short")
            
            
        else:
            self.asset.following(price)
            self.update_and_save_LS(date, price, trade_id = 0, status = "-")
        
        