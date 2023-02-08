import pandas as pd
import numpy as np
from .metrics import *


class Report:
    
    def __init__(self, dataLS, LS_reduit, LS_long, LS_short):
        
        self.dataLS = dataLS
        self.LS_reduit = LS_reduit
        self.LS_long = LS_long
        self.LS_short = LS_short
        
        self.kpi = {}
        
        self.metrics_per_trades = pd.DataFrame(index = ['total_PL','nb_periods', 'min_ret', 'max_ret',
                                               'peak', 'down', 'drawdown'])
        
        self.stats_return = pd.DataFrame(index = ['total_PL', 'nb_trades', 'min_ret', 'quartile_1', 'median', 'mean',
                                           'quartile_3', 'max_ret','drawdown', 'skew', 'kurt', 'VaR_hist',
                                           'VaR-gauss', 'CVaR'])
        
        self.stats = pd.DataFrame(index = ["return", "win_ret", "loss_ret",
                                            "mean", "win_mean", "loss_mean",
                                            "avg_amount", "avg_win_amount", "avg_loss_amount",
                                            "amount", "amount_win", "amount_loss",
                                            "win_rate", "loss_rate", "esperance", "george"])
        
        self.perf()
        
    
    def split(self):
        ""
    
    def metrics(self, r, col):
        r = r.dropna()
        
        PNL = pnl(r)
        nb_trades = 0
        
        Min = position_stats(r)[0]
        Q1 = position_stats(r)[1]
        Median = position_stats(r)[2]
        Mean = position_stats(r)[3]
        Q3 = position_stats(r)[4]
        Max = position_stats(r)[5]
        
        Drawdown = drawdown(r)
        
        Skew = skewness(r)
        Kurt = kurtosis(r)
        
        VaR_1 = var_historic(r)
        VaR_2 = var_gaussian(r)
        CVaR = cvar_historic(r)
        
        self.stats_return[col] = [PNL, nb_trades, Min, Q1, Median, Mean, Q3, Max, Drawdown,
                                  Skew, Kurt, VaR_1, VaR_2, CVaR]
        
    def statsWL(self, col, trades, trades_win, trades_loss):
        
        avg , amount , ret, avg , amount = win_loss_stat(trades)
        avg_win, amount_win, win_ret, win_avg, _ = win_loss_stat(trades_win)
        avg_loss, amount_loss, loss_ret, loss_avg, _ = win_loss_stat(trades_loss)
        
        if (len(trades_win) > 2) and (len(trades_loss) >2):
            nb_trades = len(trades)
            win_rate = len(trades_win) / nb_trades
            loss_rate = len(trades_loss) / nb_trades
            
            esperance = expectancy(win_rate, avg_win, avg_loss)
            esperance_geo = george(win_rate, avg_win, avg_loss)
        else:
            win_rate = "-"
            loss_rate = "-"
            esperance = "-"
            esperance_geo = "-"
        
        self.stats[col] = [ret, win_ret, loss_ret,
                            mean_, win_mean_, loss_mean_,
                            avg, avg_win, avg_loss,
                            amount, amount_win, amount_loss,
                            win_rate, loss_rate, esperance, esperance_geo]
    
    def benchmark(self, trades, col = "benchmark"):
        avg_, amount_, ret, mean, amount = win_loss_stat(trades)
        self.stats[col] = [ret , "-", "-",
                            mean, "-", "-",
                            avg_, "-", "-",
                            amount, "-", "-",
                            "-", "-","-", "-"]
    
    def KPI(self, trades):
        # supprimer les zeros
        loc = np.where(trades['returns'] != 0)
        trades = trades.iloc[loc]
        
        "nb trade"
        self.nb = trades['returns'].count()
        self.kpi['nb trade'] = self.nb
        
        "nombre de trade gagnant"
        self.nb_win = trades.loc[trades['returns'] > 0]['returns'].count()
        self.kpi['nb win'] = self.nb_win
        
        "nombre de trade perdant"
        self.nb_loss = trades.loc[trades['returns'] < 0]['returns'].count()
        self.kpi['nb loss'] = self.nb_loss
        
        "Taux de reussite"
        self.win_rate = (self.nb_win) / (self.nb_win + self.nb_loss)
        self.kpi['win rate'] = self.win_rate
        
        "Final amount"
        amount = trades['value_diff'].sum()
        self.kpi['amount'] = amount
        
        "Benefice total"
        self.profit = trades.loc[trades['returns'] > 0]['value_diff'].sum()
        self.kpi['profit'] = self.profit
        
        "Perte total"
        self.loss = trades.loc[trades['returns'] < 0]['value_diff'].sum()
        self.kpi['loss'] = self.loss
        
        "Average "
        average = trades['value_diff'].mean()
        self.kpi['average'] = average
        
        "Average profit per trade"
        self.profitAverage = trades[trades['returns'] > 0]['value_diff'].mean()
        self.kpi['average profit'] = self.profitAverage
        
        "Average loss per trade"
        self.lossAverage = trades[trades['returns'] < 0]['value_diff'].mean()
        self.kpi['average loss'] = self.lossAverage
        
        "Profit factor"
        self.profitFactor = self.profit / abs(self.loss)
        self.kpi['profit factor'] = self.profitFactor
        
    
    def perf(self):
        
        self.metrics(r = self.dataLS["returns"], col = "LS")
        self.metrics(r = self.LS_reduit["returns"], col = "LS_reduit")
        self.metrics(r = self.LS_long["returns"] , col = "long")
        self.metrics(r = self.LS_short["returns"] , col = "short")
        
        self.benchmark(trades = self.dataLS)
        
        self.KPI(self.LS_reduit)
        
    
    
        