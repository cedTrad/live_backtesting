import pandas as pd

from datetime import datetime
import time

import sqlalchemy
from asset import Asset

import asyncio
import threading

from evaluation.journal import Journal
from evaluation.preprocessing import Preprocessing
from evaluation.report import Report
from evaluation.plot import *

from risk.risk_strategy import CPPI
from strategy.signal import Signal

from portfolio import Portfolio



class AssetObj:
    
    def __init__(self, symbol, quantity, amount, signal, risk = None):
        self.asset = Asset(symbol = symbol, quantity = quantity, amount = amount)
        self.journal = Journal(symbol)
        self.signal = signal
        self.risk = risk
        self.trade_id = 0

        
    def update(self, date, price, bar):
        self.asset.update(date, price)
        self.journal.update(date, price, amount = self.asset.amount, quantity = self.asset.quantity)
        self.signal.position(bar)
        #self.risk.update(date, price)
        
    def saveLS(self, trade_id, status, close = False):
        self.journal.journal_LS(trade_id = trade_id, status = status,
                                close = close, position = self.asset.position)
    
    def execute(self, data, bar):
        
        date = str(data.index[bar])
        price = data.iloc[bar]['close']
        
        self.update(date = date, price = price, bar = bar)
        
        SIDE = self.signal.side
        POSITION = self.asset.position
        ORDER = self.asset
        
        if (POSITION == 0) and (SIDE["LONG"]):
                
            self.asset.open_long()
            self.saveLS(trade_id = self.trade_id, status = "open_long")
            
            #   Close Short and Open Long
        elif (POSITION == -1) and (SIDE["LONG"]):
            ORDER.close_short()
            self.saveLS(trade_id = self.trade_id, status = "close_short", close = True)
                
            ORDER.open_long()
            self.saveLS(trade_id = self.trade_id, status = "open_long")
                
            #   Short
        elif (POSITION == 0) and (SIDE["SHORT"]):
            ORDER.open_short()
            self.saveLS(trade_id = self.trade_id, status = "open_short")
            
        #   Close Long and Open Short
        elif (POSITION == 1) and (SIDE["SHORT"]):
            ORDER.close_long()
            self.saveLS(trade_id = self.trade_id, status = "close_long", close = True)
                
            ORDER.open_short()
            self.saveLS(trade_id = self.trade_id, status = "open_short")
            
        else:
            self.saveLS(trade_id = self.trade_id, status = "-")
        
             

class App:
    
    def __init__(self, symbols, interval , start = None, end = None):
        self.symbols = symbols
        self.interval = interval
        self.start = start
        self.end = end
        
        self.data = pd.DataFrame()
        self.trade_id = 0
        
        self.output = {}
        
        self.portfolio = Portfolio(symbols, interval, start, end)
        
        
    def get_date_price(self, data, bar):
        date = str(data.index[bar])
        price = data.iloc[bar]["close"]
        return date, price
    
    
    def get_data(self, symbol):
        engine = sqlalchemy.create_engine('sqlite:///data/database_{}.db'.format(self.interval))
        data = pd.read_sql(symbol ,engine)      # controle si symbol existe
        
        data = self.preprocessing(data)
        data = self.period(data)
        
        return data
        
    def preprocessing(self, data):
        data.set_index('time' , inplace=True)
        data['volume'] = pd.to_numeric(data['volume'])
        data = data[['open', 'high', 'low' , 'close' , 'volume', 'symbol', 'close_time']]
        
        data['return'] = data['close'].pct_change()
        data['log_return'] = np.log(data['close']/data['close'].shift(1))
        data['cum_return'] = data['log_return'].cumsum().apply(np.exp)
        return data
        
    
    def period(self, data):
        if self.start is None:
            self.start = data.index[0]
        if self.end is None:
            self.end = data.index[-1]
        return data.loc[self.start:self.end]
    
    
    def init(self):
        SYMBOL_1 = self.symbols[0]
        SYMBOL_2 = self.symbols[1]
        SYMBOL_3 = self.symbols[2]
        
        self.data_1 = self.get_data(symbol = SYMBOL_1)
        self.data_2 = self.get_data(symbol = SYMBOL_2)
        self.data_3 = self.get_data(symbol = SYMBOL_3)
        
        #       Signal
        SIGNAL_1 = Signal(self.data_1)
        SIGNAL_1.set_params(MOMENTUM = 3, RSI = 4, BB = (7, 3), DAY_UP = 7)
        
        SIGNAL_2 = Signal(self.data_2)
        SIGNAL_2.set_params(MOMENTUM = 3, RSI = 7, BB = (7, 3), DAY_UP = 7)
        
        SIGNAL_3 = Signal(self.data_3)
        SIGNAL_3.set_params(MOMENTUM = 3, RSI = 7, BB = (7, 3), DAY_UP = 7)
        
        
        #       Risk
        CPPI_1 = CPPI(symbol = SYMBOL_1)
        CPPI_1.set_parameters(m = 3, floor = 0.8)
        
        #       Object
        self.btcusdt = AssetObj(symbol = SYMBOL_1, quantity = 0, amount = 100, signal = SIGNAL_1, risk = CPPI_1)
        self.ethusdt = AssetObj(symbol = SYMBOL_2, quantity = 0, amount = 100, signal = SIGNAL_2)
        self.qntusdt = AssetObj(symbol = SYMBOL_3, quantity = 0, amount = 100, signal = SIGNAL_3)
        
        self.my_asset_obj = [self.btcusdt, self.ethusdt, self.qntusdt]
        self.data = {SYMBOL_1 : self.data_1, 
                     SYMBOL_2 : self.data_2, 
                     SYMBOL_3 : self.data_3}
    
    def run(self):
        
        self.init()
        
        N = min(len(self.data_1), len(self.data_2), len(self.data_3))
        
        for bar in range(3, N):
            
            self.btcusdt.execute(data = self.data_1, bar = bar)
            self.ethusdt.execute(data = self.data_2, bar = bar)
            self.qntusdt.execute(data = self.data_3, bar = bar)
            
    
    
    def result(self, assetObj = None):
        print(f" ==== {assetObj.asset.symbol} ==== ")
        dataLS = assetObj.journal.dataLS
        preprocess = Preprocessing(dataLS)
        LS_reduit = preprocess.reduit
        LS_long = preprocess.long
        LS_short = preprocess.short
        
        report = Report(dataLS = dataLS, LS_reduit = LS_reduit,
                        LS_long = LS_long, LS_short = LS_short)
        print(report.stats_return)
        return dataLS, LS_reduit, LS_long, LS_short, report
    
    
    
    
    def results(self):
        weights = [0.3, 0.3, 0.4]
        self.p_data = []
        for asset_obj in self.my_asset_obj:
            self.output[asset_obj.asset.symbol] = self.result(asset_obj)
            
            add = self.output[asset_obj.asset.symbol][0][["price_returns", "returns"]].drop_duplicates()
            
            add.columns = [asset_obj.asset.symbol+"_p", asset_obj.asset.symbol+"_returns"]
            self.p_data.append(
                add
            )
        
        self.p_data = pd.concat(self.p_data, axis = 1)
        self.p_data["p_returns"] = self.p_data[self.symbols[0]+"_returns"]*weights[0] + self.p_data[self.symbols[1]+"_returns"]*weights[1] + self.p_data[self.symbols[2]+"_returns"]*weights[2]
        self.p_data["cum_p_ret"] = (self.p_data["p_returns"] + 1).cumprod()
    
    
    
    def my_portfolio(self):
        ""
        # Portfolio returns
        self.portfolio.portfolio_return(weights, er)
        # Portfolio volatility
        self.portfolio.portfolio_vol(weights, covmat)
    
    
    
    def plot(self, symbol):
        dataLS, LS_reduit, LS_long, LS_short, _ = self.output[symbol]
        data = self.data[symbol]
        open_long = LS_long.loc[LS_long["status"]=="open_long"]["price"]
        close_long = LS_long.loc[LS_long["status"]=="close_long"]["price"]
        pnl_long = LS_long.loc[LS_long["status"]=="close_long"]["returns"]
        
        open_short = LS_short.loc[LS_short["status"]=="open_short"]["price"]
        close_short = LS_short.loc[LS_short["status"]=="close_short"]["price"]
        pnl_short = LS_short.loc[LS_short["status"]=="close_short"]["returns"]
        
        open_long_cr = LS_long.loc[LS_long["status"]=="open_long"]["cum_ret"]
        close_long_cr = LS_long.loc[LS_long["status"]=="close_long"]["cum_ret"]
        
        open_short_cr = LS_short.loc[LS_short["status"]=="open_short"]["cum_ret"]
        close_short_cr = LS_short.loc[LS_short["status"]=="close_short"]["cum_ret"]
        
        
        fig = subplots(nb_rows = 3, nb_cols = 1, row_heights = [0.2, 0.6, 0.2])
        plot_LSB(fig = fig, col = 1, row = 1, Benchmark = dataLS, Trades = LS_reduit,
                 Trades_long = LS_long, Trades_short = LS_short)
        
        # Add Candle
        plot_candle(fig = fig, col = 1, row = 2, data = data)
        
        # Add SAR
        add_scatter(fig=fig, col=1, row=2, data = data, name = "sar_up", color = "black")
        add_scatter(fig=fig, col=1, row=2, data = data, name = "sar_down", color = "blue")
        
        # Add BB
        add_line(fig=fig, col=1, row=2, data = data, name = "B_B.high")
        add_line(fig=fig, col=1, row=2, data = data, name = "B_B.low")
        add_line(fig=fig, col=1, row=2, data = data, name = "B_B.mavg")
        
        # Add RSI
        add_line(fig, col = 1, row = 3, data = data, name = "rsi")
        add_hline(fig, y = 80, col = 1, row = 3, color = 'red')
        add_hline(fig, y = 20, col = 1, row = 3, color = 'green')
        add_hline(fig, y = 0, col = 1, row = 3, color = 'black')
        
        # Add n day up
        add_line(fig, col = 1, row = 3, data = data, name = 'n_day_up')
        
        # Update params
        fig.update_layout(
            {
                'xaxis': {'rangeslider' : {'visible' : False}},
            }
        )
        
        
        signal_point(fig = fig, col = 1, row = 2, x = open_long.index, y = open_long,
                     marker = {"symbol":5, "size":10, "color":"blue"}, name = 'open_long')
        
        signal_point(fig = fig, col = 1, row = 2, x = close_long.index, y = close_long,
                     marker = {"symbol":6, "size":10, "color":"blue"}, name = "close_long")
        
        signal_point(fig = fig, col = 1, row = 2, x = open_short.index, y = open_short,
                    marker = {"symbol":8, "size":10, "color":"black"}, name = "open_short")

        signal_point(fig = fig, col = 1, row = 2, x = close_short.index, y = close_short,
                    marker = {"symbol":9, "size":10, "color":"black"}, name = "close_short")
        
        for xo, x1 ,yo, y1 in zip(open_long_cr.index, close_long_cr.index, open_long_cr, close_long_cr):
            color_returns(fig = fig, col = 1, row = 1, status = "long", x = (xo, x1), color="green", opacity=0.05)
        for xo, x1 ,yo, y1 in zip(open_short_cr.index, close_short_cr.index, open_short_cr, close_short_cr):
            color_returns(fig = fig, col = 1, row = 1, status = "short", x = (xo, x1), color="red", opacity=0.05)
        
        
        for xo, x1 ,yo, y1, pnl in zip(open_long.index, close_long.index, open_long, close_long, pnl_long):
            if pnl > 0:
                color_trades(fig = fig, col = 1, row = 2, status = "long", x = (xo, x1), y = (yo, y1), color="green", opacity=0.1)
            elif pnl < 0:
                color_trades(fig = fig, col = 1, row = 2, status = "long", x = (xo, x1), y = (yo, y1), color="red", opacity=0.1)
                
        for xo, x1 ,yo, y1, pnl in zip(open_short.index, close_short.index, open_short, close_short, pnl_short):
            if pnl > 0:
                color_trades(fig = fig, col = 1, row = 2, status = "short", x = (xo, x1), y = (yo, y1), color="green", opacity=0.1)
            elif pnl < 0:
                color_trades(fig = fig, col = 1, row = 2, status = "short", x = (xo, x1), y = (yo, y1), color="red", opacity=0.1)
        
        # Secondary axis:
        plot_second_y(fig = fig, col = 1, row = 2, data = dataLS)
        plot_second_y(fig = fig, col = 1, row = 1, data = dataLS)
        
        fig.update_layout(height = 1000 , width =1500)
        fig.show()
        
        
        
    def plot_returns(self, symbol):
        
        dataLS, LS_reduit, LS_long, LS_short, _ = self.output[symbol]
        
        fig = subplots(nb_rows=2, nb_cols=1)
        
        plot_return(fig, col = 1, row = 1, dataLS = dataLS, LS_reduit = LS_reduit,
                    LS_long = LS_long, LS_short = LS_short)
        fig.add_trace(
            go.Waterfall(
                x = LS_reduit.index,
                y = LS_reduit.returns,
                base = 1
            ),
            col = 1, row =1
        )
        fig.add_trace(
            go.Scatter(
                x = dataLS.index,
                y = dataLS.drawdown
            ),
            col = 1, row =2
        )
        fig.update_layout(height = 500 , width =1500)
        fig.show()
        
    

