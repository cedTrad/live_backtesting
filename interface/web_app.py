
import pandas as pd
import sqlalchemy
import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import plotly.graph_objects as go

from dash.dependencies import Input, Output

from layout import layout_0, layout_1


PATH = "C:/Users/cc/Desktop/CedAlgo/AlgoTrading/data/trade/"

SYMBOL = "BTC"
NAME = 'BTCUSDT_LS'

def get_data(name, table, path = PATH):
    engine = sqlalchemy.create_engine(f'sqlite:///'+path+name+'.db')
    data = pd.read_sql(table, engine)
    return data


app = dash.Dash(__name__)

app.layout = html.Div([
                    layout_0,
                    layout_1
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
    Output(component_id = "main", component_property = "figure"),
    Input("interval-component", "n_intervals")
)
def update_graph(n):
    Trades = get_data(name = NAME, table = "DataLS")
    Trades_reduit = get_data(name = NAME, table = "LS_reduit")
    Long = get_data(name = NAME, table = "LS_long")
    Short = get_data(name = NAME, table = "LS_short")
    
    trades_line = go.Scatter(
        x = Trades["date"],
        y = Trades["cum_ret"],
        line = dict(color = 'blue' , width = 1.8),
        name = 'strategie'
        )
    
    price_line = go.Scatter(
        x = Trades["date"],
        y = Trades["price_cum_ret"],
        line = dict(color = 'black' , width = 1.8),
        name = 'price'
        )
    
    long_line = go.Scatter(
        x = Long["date"],
        y = Long["cum_ret"], 
        line = dict(color = 'green' , width = 1.8),
        name = 'long_line'
        )
    
    short_line = go.Scatter(
        x = Short["date"],
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


if __name__ == '__main__':
    app.run_server(debug=True)

