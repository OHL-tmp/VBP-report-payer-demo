import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

import datetime
import pandas as pd
import numpy as np

import pathlib
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State

from utils import *
from figure import *


app = dash.Dash(__name__, url_base_pathname='/vbc-payer-demo/contract_optimizer/')

server = app.server



def create_layout(app):
#    load_data()
    return html.Div(
                [ 
                    html.Div([Header_contract(app, True, False, False, False)], style={"height":"6rem"}, className = "sticky-top navbar-expand-lg"),
                    
                    html.Div(
                        [
                            dbc.Tabs(
							    [
							        dbc.Tab(tab_setup(app), label="Contract Simulation Setup", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
							        dbc.Tab(tab_result(app), label="Result", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
							        
							    ], id = 'tab_container'
							)
                        ],
                        className="mb-3",
                        style={"padding-left":"3rem", "padding-right":"3rem"},
                    ),
                    
                ],
                style={"background-color":"#f5f5f5"},
            )


def tab_setup(app):
	return html.Div(
				[
					dbc.Row(
						[
							dbc.Col(html.H1("Contract Simulation Setup", style={"padding-left":"2rem","font-size":"3"}), width=9),
						],
                        style={"padding-top":"2rem"}
					),
					html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(html.H1("Performance Measure Setup", style={"color":"#f0a800", "font-size":"1rem","padding-top":"0.8rem"}), width=9),
                                    
                                ]
                            )
                        ],
                        style={"padding-left":"2rem","padding-right":"1rem","border-radius":"5rem","background-color":"#fff","margin-top":"2rem"}
                    ),
                    html.Div(
                        [
                        	card_performance_measure_setup(app),
                        ]
                    ),
#                    html.Div(
#                        [
#                            dbc.Row(
#                                [
#                                    dbc.Col(html.H1("Contractual Arrangement Setup", style={"color":"#f0a800", "font-size":"1rem","padding-top":"0.8rem"}), width=9),
#                                    
#                                ]
#                            )
#                        ],
#                        style={"padding-left":"2rem","padding-right":"1rem","border-radius":"5rem","background-color":"#fff","margin-top":"2rem"}
#                    ),
                    
				]
			)


def card_performance_measure_setup(app):
	return dbc.Card(
                dbc.CardBody(
                    [
                        card_medical_cost_target(app),
                        card_sl_sharing_arrangement(app),
                        card_quality_adjustment(app),
                    ]
                ),
                className="mb-3",
                style={"background-color":"#fff", "border":"none", "border-radius":"0.5rem"}
            )


def card_medical_cost_target(app):
	return dbc.Card(
                dbc.CardBody(
                    [
                    	dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Medical Cost Target", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                	html.Div(),
                                    width=3,
                                ),
                                dbc.Col(
                                	[
                                		html.Div(
                                			[
                                				html.H4("Baseline", style={"font-size":"1rem"}),
                                                html.Hr(className="ml-1"),
                                				dbc.Row(
                                					[
                                						dbc.Col(html.H4("Member Count", style={"font-size":"0.8rem"})),
                                						dbc.Col(html.H4("Medical Cost PMPM", style={"font-size":"0.8rem"})),
                                					]
                                				),
                                			]
                                		)
                                	],
                                    style={"text-align":"center"},
                                    width=3,
                                ),
                                dbc.Col(
                                	[
                                		html.Div(
                                			[
                                				html.Div(
                                                    [
                                                        html.H4(
                                                            [
                                                                "Target ",
                                                            ],
                                                            style={"font-size":"1rem"}
                                                        ),
                                                    ],
                                                ),
                                                html.Hr(className="ml-1"),
                                				dbc.Row(
                                					[
                                						dbc.Col(html.H4("Recommended", style={"font-size":"0.8rem"})),
                                						dbc.Col(html.H4("User Defined", style={"font-size":"0.8rem"})),
                                					]
                                				),
                                			]
                                		)
                                	],
                                    style={"text-align":"center"},
                                    width=3,
                                ),
                                dbc.Col(
                                	[
                                		html.Div(
                                			[
                                				html.H4("Likelihood to achieve", style={"font-size":"1rem"}),
                                                html.Hr(className="ml-1"),
                                				dbc.Row(
                                					[
                                						dbc.Col([
                                                            dbc.Button("Recommended", id = 'button-recom', color = 'link',style={"font-size":"0.8rem"}),
                                                            dbc.Popover([dbc.PopoverBody("PLACEHOLDER PLACEHOLDER PLACEHOLDER"),], 
                                                                id = 'popover-recom', is_open = False, target = 'button-recom', placement = 'top')
                                                            ]),
                                						dbc.Col(html.H4("User Defined", style={"font-size":"0.8rem"})),
                                					]
                                				),
                                			]
                                		)
                                	],
                                    style={"text-align":"center"},
                                    width=3,
                                ),
                            ],
                            style={"padding-right":"0rem", "padding-left":"0rem"}
                        ),

                        dbc.Row(
                        	[
                        		dbc.Col(html.H6("Medical Cost Target"), width=3),
                        		dbc.Col(
                    				dbc.Row(
                    					[
                    						dbc.Col(html.H6("1000")),
                    						dbc.Col(html.H6("$750")),
                    					]
                    				)
                        			, width=3
                        		),
                        		dbc.Col(
                    				dbc.Row(
                    					[
                    						dbc.Col(html.H6("$760", id = 'div-recom-tgt')),
                    						dbc.Col([
                                                dbc.InputGroup([
                                                    dbc.InputGroupAddon('$', addon_type = 'prepend'),
                                                    dbc.Input(id = 'input-usr-tgt', type = "number", debounce = True)
                                                    ])
                                                ]),
                    					]
                    				)
                        			, width=3
                        		),
                        		dbc.Col(
                    				dbc.Row(
                    					[
                    						dbc.Col(html.H6("High", id = 'div-recom-like')),
                    						dbc.Col(html.Div("Low", id = 'div-usr-like')),
                    					]
                    				)
                        			, width=3
                        		),
                        	],
                            style={"text-align":"center"},
                        )
                        
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
            )



def card_sl_sharing_arrangement(app):
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Savings/Losses Sharing Arrangement", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                	[
                                		html.Div("Shared Savings"),
                                		dbc.Row(
	                    					[
	                    						dbc.Col(html.Div(),width=3),
	                    						dbc.Col(html.H6("Recommended"),width=3),
	                    						dbc.Col(html.H6("User Defined"),width=3),
	                    					],
	                            			style={"text-align":"center"},
	                            			
	                    				),
	                    				dbc.Row(
	                    					[
	                    						dbc.Col(html.H6("MSR (Minimum Savings Rate)"),width=3),
	                    						dbc.Col(html.H6("2%"),style={"text-align":"center"},width=3),
	                    						dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-msr', type = "number", debounce = True),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ])
                                                    ],style={"text-align":"center"},width=3),
	                    					]
	                    				),
				                        dbc.Row(
	                    					[
	                    						dbc.Col(html.H6("Plan's Sharing %"),width=3),
	                    						dbc.Col(html.H6("40%"),style={"text-align":"center"},width=3),
	                    						dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-planshare', type = "number", debounce = True),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ])
                                                    ],style={"text-align":"center"},width=3),
	                    					]
	                    				),
	                    				dbc.Row(
	                    					[
	                    						dbc.Col(html.H6("Shared Savings Cap"),width=3),
	                    						dbc.Col(html.H6("10% of target"),style={"text-align":"center"},width=3),
	                    						dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-sharecap', type = "number", debounce = True),
                                                    dbc.InputGroupAddon('% of target', addon_type = 'append'),
                                                    ])
                                                    ],style={"text-align":"center"},width=3),
	                    					]
	                    				),
                                	]
                                ),
                                dbc.Col(
                                	[
                                		dbc.Checklist(
                                            options = [{'label': "Shared Losses", 'value': 'Shared Losses'}], 
                                            value = [], 
                                            id = 'switch-share-loss',
                                            switch = True),
#                                        html.Div("Shared Losses"),
                                		dbc.Row(
	                    					[
	                    						dbc.Col(html.Div(),width=3),
	                    						dbc.Col(html.H6("Recommended"),width=3),
	                    						dbc.Col(html.H6("User Defined"),width=3),
	                    					],
	                            			style={"text-align":"center"},
	                            			
	                    				),
	                    				dbc.Row(
	                    					[
	                    						dbc.Col(html.H6("MSR (Minimum Losses Rate)"),width=3),
	                    						dbc.Col(html.H6("2%"),style={"text-align":"center"},width=3),
	                    						dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-mlr', type = "number", debounce = True),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ])
                                                    ],style={"text-align":"center"},width=3),
	                    					]
	                    				),
				                        dbc.Row(
	                    					[
	                    						dbc.Col(html.H6("Plan's Sharing %"),width=3),
	                    						dbc.Col(html.H6("40%"),style={"text-align":"center"},width=3),
	                    						dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-planshare-l', type = "number", debounce = True),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ])
                                                    ],style={"text-align":"center"},width=3),
	                    					]
	                    				),
	                    				dbc.Row(
	                    					[
	                    						dbc.Col(html.H6("Shared Losses Cap"),width=3),
	                    						dbc.Col(html.H6("10% of target"),style={"text-align":"center"},width=3),
	                    						dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-sharecap-l', type = "number", debounce = True),
                                                    dbc.InputGroupAddon('% of target', addon_type = 'append'),
                                                    ])
                                                    ],style={"text-align":"center"},width=3),
	                    					]
	                    				),
                                	]
                                ),
                            ],
                            no_gutters=True,
                        ),
                        
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
            )


def card_quality_adjustment(app):
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Quality Adjustment", style={"font-size":"1rem", "margin-left":"10px"}), width="auto"),
                                dbc.Col(dbc.Button("Edit", id = 'button-show-meas')),
                                html.Div('measure table placeholder',id = 'div-meas-table-container', hidden = True)
                            ],
                            no_gutters=True,
                        ),
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
            )



def tab_result(app):
	return html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.H1("VBC Contract Simulation Result", style={"padding-left":"2rem","font-size":"3"}), width=9),
                            
                        ]
                    ),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                        dbc.Col(html.H4("Savings/Losses Sharing Arrangement", style={"font-size":"1rem", "margin-left":"10px"}), width=6),
                                        dbc.Col(html.Div("Metric"), width=2),
                                        dbc.Col(html.Div("dropdown"))
                                    ],
                                    no_gutters=True,
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(html.Div("1"), width=2),
                                        dbc.Col(html.Div("2"), width=4),
                                        dbc.Col(html.Div("3"), width=6),
                                    ],
                                    no_gutters=True,
                                ),
                            ],
                            className="mb-3",
                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem", "padding-top":"1rem"}
                        )
                    ),
                    
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                        dbc.Col(html.H4("Savings/Losses Sharing Arrangement", style={"font-size":"1rem", "margin-left":"10px"}), width=6),
                                        dbc.Col(html.Div("Metric"), width=2),
                                        dbc.Col(html.Div("dropdown"))
                                    ],
                                    no_gutters=True,
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(html.Div("1"), width=2),
                                        dbc.Col(html.Div("2"), width=4),
                                        dbc.Col(html.Div("3"), width=6),
                                    ],
                                    no_gutters=True,
                                ),
                            ],
                            className="mb-3",
                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem", "padding-top":"1rem"}
                        )
                    )
                ],
                style={"padding-top":"2rem","padding-bottom":"2rem","padding-left":"1rem","padding-right":"1rem"}

        )


app.layout = create_layout(app)

@app.callback(
    Output('popover-recom', 'is_open'),
    [Input('button-recom', 'n_clicks')],
    [State('popover-recom', 'is_open')]
    )
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    [Output('input-usr-mlr', 'disabled'),
    Output('input-usr-planshare-l', 'disabled'),
    Output('input-usr-sharecap-l', 'disabled'),],
    [Input('switch-share-loss', 'value')]
    )
def toggle_share_loss(v):
    if 'Shared Losses' in v:
        return False, False, False
    return True, True, True

@app.callback(
    Output('div-meas-table-container', 'hidden'),
    [Input('button-show-meas', 'n_clicks')],
    [State('div-meas-table-container', 'hidden')]
    )
def show_meas_table(n, hidden):
    if n:
        return not hidden 
    return hidden

@app.callback(
    [Output('div-usr-like', 'children'),
    Output('div-usr-like', 'style')],
    [Input('input-usr-tgt', 'value')],
    [State('div-recom-like', 'children'),
    State('div-recom-tgt', 'children')]
    )
def cal_usr_like(usr_tgt, recom_like, recom_tgt):
    if usr_tgt:
        recom_tgt_int = int(recom_tgt.replace('$','').replace('%','').replace(',',''))
        if usr_tgt >= recom_tgt_int:
            return 'High', {}
        elif usr_tgt < recom_tgt_int*0.95:
            return 'Low', {'background-color':'red'}
        else:
            return 'Mid', {}
    return '', {}



if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True,port=8052)


