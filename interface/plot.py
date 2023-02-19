import plotly.express as px
import plotly.graph_objects as go


def add_line(x, y, color, name):
    fig = go.Scatter(
        x = x, y = y,
        name = name,
        line = dict(color = color, width = 1),
        yaxis='y1'
    )
    return fig


def add_mark(x, y, color, name):
    fig = go.Scatter(
        x = x, y = y,
        name = name,
        line = dict(color = color, width = 1, mode = "markers"),
        yaxis='y1'
    )
    return fig
    
    
def add_candle(data, name):
    fig = go.Candlestick(
            x = data.index , open = data.open, close = data.close,
            high = data.high, low = data.low,
            yaxis='y1'
        )
    return fig


def add_second_y(x, y, name, color):
    fig = go.Scatter(
        x = x, y = y,
        name = name,
        line = dict(color = color, width = 1),
        yaxis='y2'
    )
    return fig
