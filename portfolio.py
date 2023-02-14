import pandas as pd

class Portfolio:
    
    def __init__(self, symbols):
        self.symbols = symbols
        self.data = pd.DataFrame()
    
    def update_account(self, assetObjs):
        self.account = {}
        for assetObj in assetObjs:
            self.account[assetObj.asset.symbol] = {
                        'quantity' : assetObj.asset.quantity,
                        'amount' : assetObj.asset.amount,
                        'value' : assetObj.asset.value,
                        'position' : assetObj.asset.position,
                        'leverage' : assetObj.asset.leverage
                    }
        self.values()
    
    
    def get_asset_items(self, symbol):
        return self.account[symbol]
    
    
    def values(self):
        self.total_value = 0
        self.total_amount = 0
        for symbol in self.symbols:
            self.total_amount += self.get_asset_items(symbol)['amount']
            self.total_value += self.get_asset_items(symbol)['value']
    
    
    
    def journal(self, date):
        add = {
            'value' : self.total_value
        }
        self.data = self.data.append(
            pd.DataFrame(add, index = [date])
        ) 
        path = "data/"
        engine = create_engine("sqlite:///"+path+"portfolio.db")