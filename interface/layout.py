import dash
import dash_core_components as dcc
import dash_html_components as html



layout_0 = html.Div([

                html.Div(
                    [
                    html.Div([
                        dcc.Slider(min = 0.5, max = 5,
                                step = 0.5, value = 1,
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
                
                html.Div([
                    
                    html.Div([
                        dcc.Graph(id = 'current_trade')
                    ],
                             style = {'display' : 'inline-block', 'width' : '50%'}
                             ),
                    
                    html.Div([
                        dcc.Graph(id = "cppi")
                    ],
                             style = {'display' : 'inline-block', 'width' : '50%'}
                             )
                ],
                        style = {'display' : 'inline-block', 'width' : '60%'}),
                
                html.Div([
                    html.H3("Current trade info"),
                    html.Br(),
                    html.H4("Entry"),
                    html.Div(id = "price"),
                    html.Div(id = "amount"),
                    html.Div(id = "units"),
                    html.Br(),
                    html.H4("Current"),
                    html.Div(id = "price_c"),
                    html.Div(id = "amount_c"),
                    html.Div(id = "cum_ret")
                ],
                        style = {'display' : 'inline-block', 'width' : '40%'})
            ]
                    )

layout_1 = html.Div([
                html.Br(),
                dcc.Graph(id = "main")
            ]
                    )


