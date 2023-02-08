import pandas as pd
import numpy as np

from scipy.optimize import minimize
import scipy.stats
from scipy.stats import norm

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Portfolio():
    
    def __init__(self, symbols, interval, begin=None, end=None):
        self.symbols = symbols
        self.interval = interval
        self.periods_per_year = 365
    
    
    def periodical_rets(self, r):  # r:pd.Series
        cum_r = (1 + r).prod()
        n_period = r.shape[0]
        return cum_r**(self.periods_per_year/n_period)-1
    
    
    def vols(self, r):      # r:pd.Series
        return r.std()*(self.periods_per_year**0.5)
    
    
    def drawdown(self,r):                # r:pd.Series
        cum_r = (1+r).cumprod()
        peak = cum_r.cummax()
        drawdowns = (cum_r - peak)/peak
        return pd.DataFrame({
            "cum_r":cum_r,
            "peak":peak,
            "drawdowns":drawdowns
        })
        
        
    def sharpe_ratio(self, r):      # r:pd.Series
        p_rets = self.periodicals_rets(r)
        p_vols = self.periodicals_vols(r)
        return p_rets/p_vols
    
    
    def var_historic(self, r, level=5):     # r:pd.Series
        if isinstance(r, pd.DataFrame):
            return r.aggregate(self.var_historic, level)
        elif isinstance(r, pd.Series):
            return -np.percentile(r, level)
    
    
    def var_gaussian(self, r, level=5, modified=False):     # r:pd.Series
        z = norm.ppf(level/100)
        if modified:
            s = scipy.stats.skewness(r)
            k = scipy.stats.kurtosis(r)
            z = ( z + 
                (z**2 - 1)*s/6 +
                (z**3 - 3*z)*(k-3)/24 -
                (2*z**3 - 5*z)*(s**2)/36
            )
        return -(r.mean() + z*r.std(ddof=0))
    
    def cvar_historic(self, r, level=5):        # r:pd.Series
        if isinstance(r, pd.Series):
            is_beyond = r<= -self.var_historic(r, level)
            return -r[is_beyond].mean()
        elif isinstance(r, pd.DataFrame):
            return r.aggregate(cvar_historic, level)
        else:
            raise TypeError("Expected r to be a Series or DataFrame")


    def portfolio_return(self, weights, er):
        return weights.T @ er

    def portfolio_vol(self, weights, covmat):
        return (weights.T @ covmat @ weights)**0.5
    
    
    
    def plot_ef2(self, n_points, er, cov):
        if er.shape[0] != 2 or cov.shape[0] != 2:
            raise ValueError("Plot_ef2 can only plot 2-asset frontiers")
        weights = [np.array([w, 1-w]) for w in np.linspace(0, 1, n_points)]
        rets = [self.portfolio_return(w, er) for w in weights]
        vols = [self.portfolio_vol(w, cov) for w in weights]
        ef = pd.DataFrame(
            {
                "Returns" : rets,
                "Vols" : vols 
            }
        )
        return px.scatter(y = ef["Returns"], x = ef["Vols"])
        #return ef.plot.line(y="Returns", x="Vols", style=".-", figsize=(15, 6))  
    
    def minimize_vol(self, target_return, er, cov):
        n = er.shape[0]
        init_guess = np.repeat(1/n , n)
        bounds = ((0.0 , 1.0), )*n
        return_is_target = {
            'type' : 'eq',
            'args' : (er,),
            'fun' : lambda weights, er : target_return - self.portfolio_return(weights, er)
            }
        weights_sum_to_1 = {
            'type' : 'eq',
            'fun' : lambda weights : np.sum(weights) - 1
        }
        results = minimize(self.portfolio_vol, init_guess,
                        args = (cov,), method = 'SLSQP',
                        options = {'disp' : False},
                        constraints = (return_is_target, weights_sum_to_1),
                        bounds = bounds
                        )
        return results.x
    
    def msr(self, er, cov):
        n = er.shape[0]
        init_guess = np.repeat(1/n , n)
        bounds = ((0.0 , 1.0), )*n
        weights_sum_to_1 = {
            'type' : 'eq',
            'fun' : lambda weights : np.sum(weights) - 1
        }
        def neg_sharpe_ratio(weights, er, cov):
            r = self.portfolio_return(weights, er)
            vol = self.portfolio_vol(weights,cov)
            return -r/vol
        results = minimize(neg_sharpe_ratio, init_guess,
                        args = (er, cov,), method = 'SLSQP',
                        options = {'disp' : False},
                        constraints = (weights_sum_to_1),
                        bounds = bounds
                        )
        return results.x
    
    def gmv(self, cov):
        n = cov.shape[0]
        return self.msr(np.repeat(1, n), cov)
    
    def optimal_weights(self, n_points, er, cov):
        target_rs = np.linspace(er.min(), er.max(), n_points)
        weights = [self.minimize_vol(target_return, er, cov) for target_return in target_rs]
        return weights
    
    def plot_ef(self, n_points, er, cov, show_cml = False, style=".-", riskfree_rate=0, show_ew = False, show_gmv = False):
        weights = self.optimal_weights(n_points, er, cov)
        rets = [self.portfolio_return(w, er) for w in weights]
        vols = [self.portfolio_vol(w, cov) for w in weights]
        ef = pd.DataFrame({
            "Returns" : rets,
            "Volatility" : vols
        })
        #ax = ef.plot.line(x = "Volatility", y = "Returns", style = ".-")
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x = ef["Volatility"],
                y = ef["Returns"],
                name = "EF"
            )
        )
        if show_ew:
            n = er.shape[0]
            w_ew = np.repeat(1/n, n)
            r_ew = self.portfolio_return(w_ew, er)
            vol_ew = self.portfolio_vol(w_ew, cov)
            # Display EW
            #ax.plot([vol_ew], [r_ew], color="goldenrod", marker="o", markersize=10)
            fig.add_trace(
                go.Scatter(
                    x = [vol_ew],
                    y = [r_ew],
                    name = 'EW'
                )
            )
        
        if show_gmv:
            w_gmv = self.gmv(cov)
            r_gmv = self.portfolio_return(w_gmv, er)
            vol_gmv = self.portfolio_vol(w_gmv, cov)
            # display GMV
            #ax.plot([vol_gmv], [r_gmv], color="midnightblue", marker="o", markersize=10)
            fig.add_trace(
                go.Scatter(
                    x =[vol_gmv],
                    y = [r_gmv],
                    name = 'GMV'
                )
            )
        return fig
        
    def summary_stats(self, r, level=5):       # level en % : 5%
        p_rets = r.aggregate(self.periodicals_rets)
        p_vols = r.aggregate(self.periodicals_vols)
        skew = r.aggregate(scipy.stats.skew)
        kurt = r.aggregate(scipy.stats.kurtosis)
        sharp_ratio = r.aggregate(self.sharpe_ratio)
        max_drawdown = r.aggregate(lambda r : self.drawdown(r)['drawdowns'].min())
        var_hist = r.aggregate(self.var_historic, level=level)
        var_guass = r.aggregate(self.var_gaussian, level=level)
        cvar = r.aggregate(self.cvar_historic, level=level)
        
        return pd.DataFrame({
            "Periodical_returns" : p_rets,
            "Periodical_volatility" : p_vols,
            "sharpe ratio" : sharp_ratio,
            "VaR historic" : var_hist,
            "VaR guaussian" : var_guass,
            "CVaR" : cvar,
            "drawdown" : max_drawdown,
            "Skew/Asymetrie" : skew,
            "kurtosis" : kurt
        })
        