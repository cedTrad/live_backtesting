import pandas

class Money_management:
    
    def __init__(self, symbol):
        self.symbol = symbol
        
        
    def config(self, risky_amount, stopLoss, takeProfit, leverage):
        self.risky_amount = risky_amount
        self.stopLoss = stopLoss
        self.takeProfit = takeProfit
        self.leverage = leverage
        
    
    def statics_metrics(self, price):
        self.stopSize = self.risky_amount*stop_loss
        self.rewardSize = self.risky_amount*takeProfit
        self.R_r = self.rewardSize / self.stopSize
        
    
    def done(self, price):
        self.statics_metrics(price)
        
        quantity = self.risky_amount / price
        
        return quantity
        