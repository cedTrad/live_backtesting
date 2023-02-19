
class Config:
    
    def __init__(self, symbol, initial_amount):
        self.symbol = symbol
        self.signal = Signal(symbol)
        self.money_m = Money_management(symbol, initial_amount)
        
    def strategy(self, momentum, rsi, bb, day_up):
        self.signal.set_params(momentum = momentum, rsi = rsi, bb = bb, day_up = day_up)
        
    def money_m(self, risky_amount, stopLoss, takeProfit, leverage):
        self.money_m.config(risky_amount = risky_amount, stopLoss = stopLoss,
                            takeProfit = takeProfit, leverage = leverage)
        
    def done(self):
        asset = AssetObj(symbol = self.symbol, amount = initial_amount, signal = self.signal,
                         money_management = self.money_management)
        return asset
    
    
    
    
    