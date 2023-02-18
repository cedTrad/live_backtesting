import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# make subplot
def subplots(nb_rows , nb_cols, row_heights = None, column_widths = None, vertical_spacing=0.01, horizontal_spacing = 0.02):
    
    fig = make_subplots(rows = nb_rows, cols = nb_cols, shared_xaxes = True, shared_yaxes = False,
                        row_heights = row_heights, column_widths= column_widths,
                        vertical_spacing = vertical_spacing, horizontal_spacing = horizontal_spacing,
                         specs = [
                             [{"secondary_y": True}],
                             [{"secondary_y": True}],
                             [{"secondary_y": True}]
                           ]
                         )
    return fig


# Plot candle
def plot_candle(fig, col, row, data): 
    fig.add_trace(
        go.Candlestick(
            x = data.index , open = data.open, close = data.close,
            high = data.high, low = data.low, name = data.symbol[0]
        ),
        col = col, row = row
    )
    fig = fig.update_xaxes(rangeslider_visible=False)


def plot_second_y(fig, col, row, data):
    fig.add_trace(
        go.Scatter(
            x = data.index,
            y = data['position'],
            name = 'position',
            yaxis="y2"
        ),
        col = col, row = row,
        secondary_y=True,
    )


def add_line(fig, col, row, data, name, color = None):
    fig.add_trace(
        go.Scatter(
            x = data.index,
            y = data[name],
            name = name
        ),
        col = col, row = row
    )


def add_scatter(fig, col, row, data, name, color):
    fig.add_trace(
        go.Scatter(
            x = data.index,
            y = data[name],
            mode = 'markers',
            marker_color = color,
            name = name
        ),
        col = col, row = row
    )


def add_hline(fig, y, col, row, color):
    fig.add_hline(y = y , col = col, row = row, line_color = color)


# signal point
def signal_point(fig, col, row, x, y, name, marker, size = 10):
    fig.add_trace(
        go.Scatter(
            x = x,
            y = y,
            mode = "markers",
            marker_symbol = marker["symbol"],
            marker_size = marker["size"],
            marker_color = marker["color"],
            name = name
        ),
        col = col , row = row
    )
    
    
# Plot long short brenchmank
def plot_LSB(fig, col , row ,Benchmark, Trades, Trades_long, Trades_short):
    fig.add_trace(
        go.Scatter(
            x = Benchmark.index,
            y = Benchmark["price_cum_ret"],
            marker_color = "pink",
            name = "price"
        ),
        col = col , row = row
    )
    fig.add_trace(
        go.Scatter(
            x = Trades.index,
            y = Trades["cum_ret"],
            marker_color = "green",
            name = "trade"
        ),
        col = col , row = row
    )
    fig.add_trace(
        go.Scatter(
            x = Trades_long.index,
            y = Trades_long["cum_ret"],
            marker_color = "blue",
            name = "long"
        ),
        col = col , row = row
    )
    fig.add_trace(
        go.Scatter(
            x = Trades_short.index,
            y = Trades_short["cum_ret"],
            marker_color = "red",
            name = "short"
        ),
        col = col , row = row
    )



def color_trades(fig, col, row, status, x , y, color, opacity):
    '''
    x : tuple , x = (x0, x1)
    y : tuple , y = (y0, y1)
    '''
    fig.add_shape(x0 = x[0], x1 = x[1],
                  y0 = y[0]*0.6, y1 = y[1]*1.4,
                  fillcolor = color, opacity = opacity,
                  col = col , row = row)

def color_returns(fig, col, row, status, x , color, opacity):
    
    fig.add_vrect(x0 = x[0], x1 = x[1],
                  fillcolor = color, opacity = opacity,
                  col = col , row = row)


def plot_return(fig, col, row, dataLS, LS_reduit, LS_long, LS_short):
    fig.add_trace(
        go.Scatter(
            x = dataLS.index, y = dataLS["cum_ret"],
            name = "LS"
        )
    )
    fig.add_trace(
        go.Scatter(
            x = dataLS.index, y = dataLS["price_cum_ret"],
            name = "price"
        ),
        col = col, row = row
    )
    fig.add_trace(
        go.Scatter(
            x = LS_reduit.index, y = LS_reduit["cum_ret"],
            name = "LS_reduit"
        ),
        col = col, row = row
    )
    fig.add_trace(
        go.Scatter(
            x = LS_long.index, y = LS_long["cum_ret"],
            name = "LS_long"
        ),
        col = col, row = row
    )
    fig.add_trace(
        go.Scatter(
            x = LS_short.index, y = LS_short["cum_ret"],
            name = "LS_short"
        ),
        col = 1, row = 1
    )
    
    

def plot_macd(fig, row, col):
    fig.append_trace(
        go.Scatter(
            x = data.index , y = data.macd,
            line = {'color':'black'},
            name = "macd"
        ),
        row = row, col = col
    )
    
    fig.append_trace(
        go.Scatter(
            x = data.index , y = data.macd_signal,
            line = {'color':'green'},
            name = "macd signal"
        ),
        row = row, col = col
    )
    
    fig.append_trace(
        go.Scatter(
            x = data.index , y = data.macd_diff,
            #line = {'color':'#000000'},
            name = "macd_diff"
        ),
        row = row, col = col
    )
    
    colors = np.where(data['macd_diff'] < 0, 'red', 'green')
    fig.add_trace(
        go.Bar
        (
            x = data.index ,y = data.macd_diff,
            name="histogramme",
            marker_color = colors
        ),
        row = row, col = col
    )
    

def plot_stochastic(data, col, row):
    fig.append_trace(
        go.Scatter(
            x = data.index , y = data.K,
            line = {'color':'#ff9900'},
            name = "Fast"
        ),
        row = row, col = col
    )
    
    
    fig.append_trace(
        go.Scatter(
            x = data.index , y = data.D,
            line = {'color':'#000000'},
            name = "Slow"
        ),
        row = row, col = col
    )