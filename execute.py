from asset import Asset
from trade import Trade

from risk.risk_strategy import CPPI
from strategy.signal import Signal
from asset import Asset

from data.journal import Journal


class AssetObj:
    
    def __init__(self, symbol, quantity, amount, signal, risk = None):
        self.asset = Asset(symbol = symbol, quantity = quantity, amount = amount)
        self.journal = Journal(symbol)
        self.signal = signal
        self.risk = risk
        self.trade_id = 0
    
    def update_and_save_LS(self, date, price, trade_id, status, condition, close = False):
        self.journal.update(date, price, amount = self.asset.amount,
                            quantity = self.asset.quantity, value = self.asset.value)
        self.journal.journal_LS(trade_id = trade_id, status = status, close = close,
                                position = self.asset.position, condition = condition)
        #self.risk.update(date, price)
        
    def execute(self, date, price, c):
        
        SIDE = self.signal.side
        POSITION = self.asset.position
        
        if (POSITION == 0) and (SIDE["LONG"]):
            self.asset.open_long(price)
            self.update_and_save_LS(date, price, trade_id = 0, status = "open_long", condition = c)

            
            #   Close Short and Open Long
        elif (POSITION == -1) and (SIDE["LONG"]):
            self.asset.close_short(price)
            self.update_and_save_LS(date, price, trade_id = 0, status = "close_short", close = True, condition = c)
            
            self.asset.open_long(price)
            self.update_and_save_LS(date, price, trade_id = 0, status = "open_long", condition = c)
                
            #   Short
        elif (POSITION == 0) and (SIDE["SHORT"]):
            self.asset.open_short(price)
            self.update_and_save_LS(date, price, trade_id = 0, status = "open_short", condition = c)
            
            
        #   Close Long and Open Short
        elif (POSITION == 1) and (SIDE["SHORT"]):
            self.asset.close_long(price)
            self.update_and_save_LS(date, price, trade_id = 0, status = "close_long", close = True, condition = c)
            
            self.asset.open_short(price)
            self.update_and_save_LS(date, price, trade_id = 0, status = "open_short", condition = c)
            
            
        else:
            self.asset.following(price)
            self.update_and_save_LS(date, price, trade_id = 0, status = "-", condition = c)
        
        print(date, SIDE)