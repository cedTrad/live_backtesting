from asset import Asset
from strategy.signal import Signal
from risk_management.money_management import Money_management

from execute import AssetObj

class Config:
    
    def __init__(self, symbol, initial_amount):
        self.symbol = symbol
        self.initial_amount = initial_amount
        self.signal = Signal(symbol)
        self.money_m = Money_management(symbol, initial_amount)
        
    def strategy(self, momentum, rsi, bb, day_up):
        self.signal.set_params(momentum = momentum, rsi = rsi, bb = bb, day_up = day_up)
        
    def money(self, risky_amount, stopLoss, takeProfit, leverage):
        self.money_m.config(risky_amount = risky_amount, stopLoss = stopLoss,
                            takeProfit = takeProfit, leverage = leverage)
        
    def done(self):
        asset = AssetObj(symbol = self.symbol, amount = self.initial_amount, signal = self.signal,
                         money_management = self.money_m)
        return asset
    
    
    
    
    