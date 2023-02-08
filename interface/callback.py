
import pandas as pd
import sqlalchemy
import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import plotly.graph_objects as go

from dash.dependencies import Input, Output





@app.callback(
    [Output(component_id = "interval-component", component_property = "interval")],
    [Input("interval-refresh", "value")]
)
def update_refresh_rate(value):
    return [value * 1000]


@app.callback(
    [Output(component_id='latest-timestamp', component_property='children')],
    [Input('interval-component', 'n_intervals')]
)
def update_timestamp(interval):
    return [html.Span(f"Last updated: {datetime.datetime.now()}")]


# -------------------- Current trade  ------------------
@app.callback(
    Output(component_id='current_trade', component_property='figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph_current_trade(n):
    
    Trades = Data(symbol = symbol, table = "Trades")
    loc = np.where(Trades["trade_id"] == Trades["trade_id"].iloc[-1])
    current_trade = Trades.iloc[loc]
    
    trace = go.Scatter(
        x = current_trade.index ,
        y = current_trade["cum_ret"],
        line = dict(color = 'blue' , width = 1.8),
        name = 'current trade'
        )
    
    layout = go.Layout(
        height = 300 , width = 500,
        template="simple_white"
        )
    
    fig = go.Figure(
        data = [trace],
        layout = layout
    )    
    return fig


# ----------------------- CPPI ------------------------------
@app.callback(
    Output(component_id='cppi', component_property='figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph_current_histogram(n):
    Trades = merge("Trades", "TradesMeta")
    
    trace = go.Scatter(
        x = Trades.index ,
        y = Trades["returns"],
        line = dict(color = 'blue' , width = 1.8),
        name = 'returns'
        )
    
    layout = go.Layout(
        height = 300 , width = 500,
        template="simple_white"
        )
    
    fig = go.Figure(
        data = [trace],
        layout = layout
    )    
    return fig


#  ---------------------------- Main ---------------------------
@app.callback(
    Output(component_id = "main", component_property = "figure"),
    Input("interval-component", "n_intervals")
)
def update_graph(n):
    Trades = merge("Trades", "TradesMeta")
    Trades_reduit = merge("Reduit", "ReduitMeta")
    Long = merge("Long", "LongMeta")
    Short = merge("Short", "ShortMeta")
    
    trades_line = go.Scatter(
        x = Trades.index ,
        y = Trades["cum_ret"],
        line = dict(color = 'blue' , width = 1.8),
        name = 'strategie'
        )
    
    price_line = go.Scatter(
        x = Trades.index ,
        y = Trades["price_cum_ret"],
        line = dict(color = 'black' , width = 1.8),
        name = 'price'
        )
    
    long_line = go.Scatter(
        x = Long.index ,
        y = Long["cum_ret"], 
        line = dict(color = 'green' , width = 1.8),
        name = 'long_line'
        )
    
    short_line = go.Scatter(
        x = Short.index ,
        y = Short["cum_ret"], 
        line = dict(color = 'red' , width = 1.8),
        name = 'short_line'
        )
    
    layout = go.Layout(
        height = 500 , width = 1000,
        template="simple_white"
        )
    
    fig = go.Figure(
        data = [trades_line, price_line, long_line, short_line],
        layout = layout
    )    
    return fig
