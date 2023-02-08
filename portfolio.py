from utils import Token



class Portfolio:
    
    def __init__(self):
        self.tokens = {}
        #self.update()
        
    def add_token(self, token):  # token : class Token , token(name = "BTC")
        self.tokens[token.name] = token
        self.update()
    
    def drop_token(self, name): # token : class Token
        del self.tokens[name]
        self.update()
        
    def set_symbols(self):
        temp_list = []
        for token in self.tokens.values():
            temp_list.append(token.symbol)
        return temp_list
    
    def get_value(self):
        temp_list = {}
        for token in self.tokens.values():
            token[token.symbol] = token.value
        return temp_list
    
    
    def net_value(self):
        temp_list = []
        for token in self.tokens.values():
            temp_list.append(token.value)
        temp_list = np.array(temp_list)
        return np.sum(temp_list)
        
        
    def set_weight(self):
        temp_dict = {}
        for token in self.tokens.values():
            weight = token.value / self.net_wealth
            temp_dict[token.name] = weight            
        return temp_dict
    
    
    def update(self):
        self.symbols = self.set_symbols()
        self.values = self.get_value()
        self.net_wealth = self.net_value()
        self.weights = self.set_weight()
        
        
    def update_token(self, token_name, price, quantity):
        self.tokens[token_name].update(quantity, price)
    
    
    