import dash
import dash_core_components as dcc
import dash_html_components as html



layout_0 = html.Div([

                html.Div(
                    [
                    html.Div([
                        dcc.Slider(min = 0.5, max = 5,
                                step = 0.5, value = 10,
                                id = "interval-refresh")
                    ],
                            style = {"width" : "20%"}),
                    
                    html.Div(id='latest-timestamp', style={"padding": "20px"}),
                    dcc.Interval(
                            id='interval-component',
                            interval=1 * 1000,
                            n_intervals=0
                    ),
                ]
                         ),
            ])

layout_return = html.Div([
                html.Br(),
                dcc.Graph(id = "return")
            ],
                        style = {'display' : 'inline-block', 'width' : '100%'}
                        )

layout_candle = html.Div([
        html.Br(),
        dcc.Graph(id = "candle")
],
                         style = {'display' : 'inline-block', 'width' : '100%'}
                         )


layout_symbol_1 = html.Div([])

layout_symbol_2 = html.Div([])

layout_symbol_3 = html.Div([])

layout_portfolio = html.Div([])

layout_cppi = html.Div([])

layout_recovery = html.Div([])

layout_table = html.Div([])


