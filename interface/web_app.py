
import pandas as pd
import sqlalchemy
import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import plotly.graph_objects as go

from dash.dependencies import Input, Output

from layout import *
from plot import *


PATH = "C:/Users/cc/Desktop/CedAlgo/AlgoTrading/data/trade/"

PATH_ = "C:/Users/cc/Desktop/CedAlgo/AlgoTrading/data/data/"

SYMBOL = "BTC"
NAME = 'BTCUSDT_LS'

def get_data(name, table, path = PATH):
    engine = sqlalchemy.create_engine(f'sqlite:///'+path+name+'.db')
    data = pd.read_sql(table, engine)
    return data


app = dash.Dash(__name__)

app.layout = html.Div([
                    layout_0,
                    
                    html.Div([
                        layout_return,
                        layout_candle
                    ],
                            style = {'width' : '100%'}
                            ),
                ]
                      )

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



#  ---------------------------- Main ---------------------------
@app.callback(
    Output(component_id = "return", component_property = "figure"),
    Input("interval-component", "n_intervals")
)
def update_ret_graph(n):
    Trades = get_data(name = NAME, table = "DataLS")
    Trades_reduit = get_data(name = NAME, table = "LS_reduit")
    Long = get_data(name = NAME, table = "LS_long")
    Short = get_data(name = NAME, table = "LS_short")
    
    trades_line = add_line(x = Trades['date'], y = Trades['cum_ret'],
                              color = "blue", name = "strategie")
    price_line = add_line(x = Trades['date'], y = Trades["price_cum_ret"],
                          color = "black", name = "price")
    long_line = add_line(x = Long['date'], y = Long['cum_ret'],
                         color = 'green', name = 'long')
    short_line = add_line(x = Short['date'], y = Short['cum_ret'],
                          color = 'red', name = 'short')
    position = add_second_y(x = Trades['date'], y = Trades['position'],
                         color='black', name = 'position')
    
    layout = go.Layout(
        height = 200 , width = 1200,
        template="simple_white",
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
        yaxis=dict(title='cumulative return'),
        yaxis2=dict(title='Position', overlaying='y', side='right')
        )
    
    fig = go.Figure(
        data = [trades_line, price_line, long_line, short_line, position],
        layout = layout
    )    
    return fig



@app.callback(
    Output(component_id = "candle", component_property = "figure"),
    Input("interval-component", "n_intervals")
)
def update_candle_graph(n):
    dataLS = get_data(name = NAME, table = "DataLS")
    data = get_data(name = "BTCUSDT_raw", table = "data", path = PATH_)
    data.set_index("time", inplace = True)
    #data = data.loc["2023"]
    
    candle = add_candle(data, name = "BTCUSDT")
    position = add_second_y(x = dataLS['date'], y = dataLS['position'],
                         color='black', name = 'position')
    
    layout = go.Layout(
        height = 700 , width = 1200,
        template="simple_white",
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
        yaxis=dict(title='price'),
        yaxis2=dict(title='Position', overlaying='y', side='right'),
        )
    
    fig = go.Figure(
        data = [candle, position],
        layout = layout
    )    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

