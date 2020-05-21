import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import time

import datetime
import json
import pandas as pd
import numpy as np

import pathlib
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State

from utils import *
from figure import *
from simulation_cal import *


app = dash.Dash(__name__, url_base_pathname='/vbc-payer-demo/contract-optimizer/')

server = app.server

file = open('configure/default_ds.json', encoding = 'utf-8')
default_input = json.load(file)
df_quality = pd.read_csv("data/quality_setup.csv")

#modebar display
button_to_rm=['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'hoverClosestCartesian','hoverCompareCartesian','hoverClosestGl2d', 'hoverClosestPie', 'toggleHover','toggleSpikelines']

def create_layout(app):
#    load_data()
    return html.Div(
                [ 
                    html.Div([Header_contract(app, True, False, False,False)], style={"height":"6rem"}, className = "sticky-top navbar-expand-lg"),
                    
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

                    # hidden div inside the app to store the temp data
                    html.Div(id = 'temp-data', style = {'display':'none'}),
                    html.Div(id = 'temp-result', style = {'display':'none'}),

                    
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
					# html.Div(
     #                    [
     #                        dbc.Row(
     #                            [
     #                                dbc.Col(html.H1("Performance Measure Setup", style={"color":"#f0a800", "font-size":"1rem","padding-top":"0.8rem"}), width=9),
                                    
     #                            ]
     #                        )
     #                    ],
     #                    style={"padding-left":"2rem","padding-right":"1rem","border-radius":"5rem","background-color":"#fff","margin-top":"2rem"}
     #                ),
                    html.Div(
                        [
                        	card_performance_measure_setup(app),
                        ]
                    ),                  
				]
			)


def card_performance_measure_setup(app):
	return dbc.Card(
                dbc.CardBody(
                    [
                        card_summary_improvement(app),
                        card_medical_cost_target(app),
                        card_sl_sharing_arrangement(app),
                        card_quality_adjustment(app),
                        html.Div(
                            dbc.Button("SUBMIT",
                                className="mb-3",
                                style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Black", "font-size":"1rem", "width":"8rem"},
                                id = 'button-submit-simulation'
                            ),
                            style={"text-align":"center"}
                        )
                    ]
                ),
                className="mb-3",
                style={"background-color":"#fff", "border":"none", "border-radius":"0.5rem"}
            )


def card_summary_improvement(app):
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Summary of Improvement Opportunities", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        [
                                            html.H6("Overuser Reduction", style={"height":"1.8rem"}),
                                            html.H1("0.7%", style={"font-size":"1.5rem","color":"#F5B111"})
                                        ],
                                        style={"padding":"1rem","text-align":"center"}
                                    ),
                                    width=2,
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                            html.H6("Service Optimization", style={"height":"1.8rem"}),
                                            html.H1("0.2%", style={"font-size":"1.5rem","color":"#F5B111"})
                                        ],
                                        style={"padding":"1rem","text-align":"center"}
                                    ),
                                    width=2,
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                            html.H6("Transition of Care Management", style={"height":"1.8rem"}),
                                            html.H1("0.3%", style={"font-size":"1.5rem","color":"#F5B111"})
                                        ],
                                        style={"padding":"1rem","text-align":"center"}
                                    ),
                                    width=2,
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                            html.H6("Chronic Disease Management", style={"height":"1.8rem"}),
                                            html.H1("0.5%", style={"font-size":"1.5rem","color":"#F5B111"})
                                        ],
                                        style={"padding":"1rem","text-align":"center"}
                                    ),
                                    width=2,
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                            html.H6("High Risk Patient Management", style={"height":"1.8rem"}),
                                            html.H1("0.7%", style={"font-size":"1.5rem","color":"#F5B111"})
                                        ],
                                        style={"padding":"1rem","text-align":"center"}
                                    ),
                                    width=2,
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                            html.H6("Coding Improvement Opportunity", style={"height":"1.8rem"}),
                                            html.H1("0.7%", style={"font-size":"1.5rem","color":"#F5B111"})
                                        ],
                                        style={"padding":"1rem","text-align":"center"}
                                    ),
                                    width=2,
                                ),
                            ]
                        )
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
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
                                						dbc.Col(html.H4("ACO's Member Count", style={"font-size":"0.8rem"})),
                                						dbc.Col(html.H4("ACO's Medical Cost PMPM", style={"font-size":"0.8rem"})),
                                                        dbc.Col(html.H4("Peer Group Medical Cost PMPM", style={"font-size":"0.8rem"})),
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
                                                        dbc.Col(
                                                            [
                                                                html.H4(
                                                                    [
                                                                        "Recommended",
                                                                        html.Span(
                                                                            "\u24D8",
                                                                            style={"font-size":"0.8rem"}
                                                                        )
                                                                    ],
                                                                    id="tooltip-vbc-measure",
                                                                    style={"font-size":"0.8rem"}
                                                                ),
                                                                dbc.Tooltip(
                                                                    "?????",
                                                                    target="tooltip-vbc-measure",
                                                                    style={"text-align":"start"}
                                                                ),
                                                            ]
                                                        ),
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
                            ],
                            style={"padding-right":"0rem", "padding-left":"0rem"}
                        ),
                        
                        card_med_cost_target(),
                        
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
            )

def card_med_cost_target():
    return dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.H6("Medical Cost Target"), width=4),
                                dbc.Col(
                                    dbc.Row(
                                        [
                                            dbc.Col(html.H6("5.7%")),
                                            dbc.Col(html.H6("3.5%")),
                                            dbc.Col(html.H6("3.1%")),
                                        ]
                                    )
                                    , width=4
                                ),
                                dbc.Col(
                                    dbc.Row(
                                        [
                                            dbc.Col(html.H6("3.9%")),
                                            dbc.Col([
                                                dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-tgt-trend', type = "number", step = 0.1, debounce = True, value = default_input['medical cost target']['user target']),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                            ],
                                            style={"margin-top":"-0.5rem"}),

                                        ]
                                    )
                                    , width=4
                                ),
                            ],
                            style={"text-align":"center","padding-top":"1.5rem","padding-bottom":"0.5rem"},
                        ),

                        dbc.Row(
                            [
                                dbc.Col(html.H6("Medical Cost Target PMPM"), width=4),
                                dbc.Col(
                                    dbc.Row(
                                        [
                                            dbc.Col(html.H6(default_input['medical cost target']['medical cost pmpm'])),
                                            dbc.Col(html.H6(default_input['medical cost target']['peer group medical cost pmpm'])),
                                            dbc.Col(html.H6(default_input['medical cost target']['bic medical cost pmpm'])),
                                        ]
                                    )
                                    , width=4
                                ),
                                dbc.Col(
                                    dbc.Row(
                                        [
                                            dbc.Col(html.H6(default_input['medical cost target']['recom target'], id = 'div-recom-tgt')),
                                            dbc.Col(html.H6( id = 'div-usr-tgt')),
                                        ]
                                    )
                                    , width=4
                                ),
                                
                            ],
                            style={"text-align":"center","padding-top":"1rem",},
                        )
                    ],
                    width=9,
                    style={"background-color":"#fff","border-radius":"0.5rem","height":"6.8rem"},
                ),

                dbc.Col(
                    dbc.Row(
                        [
                            dbc.Col(html.Div(html.H1("High", id = 'div-recom-like',style={"text-align":"center", "padding-top":"2.5rem", "padding-bottom":"2.5rem", "font-size":"1.5rem", "color":"#fff"}), style={"border-radius":"0.5rem", "background-color":"green"}), style={"padding-left":"1rem", "padding-right":"0.5rem"}, width=6),
                            dbc.Col(id = 'div-usr-like', style={"padding-left":"0.5rem", "padding-right":"0.5rem"}, width=6),
                        ]
                    ),
                    width=3
                )
            ]
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
                                		html.H3("Shared Savings", style={"font-size":"1rem"}),
                                        html.Hr(),
                                		dbc.Row(
	                    					[
	                    						dbc.Col(html.Div(),width=4),
	                    						dbc.Col(html.H6("Recommended"),width=4),
	                    						dbc.Col(html.H6("User Defined"),width=4),
	                    					],
	                            			style={"text-align":"center"},
	                            			
	                    				),
	                    				dbc.Row(
	                    					[
	                    						dbc.Col(html.H2("MSR (Minimum Savings Rate)", style={"font-size":"0.8rem"}),width=4),
	                    						dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom msr']),style={"text-align":"center"},width=4),
	                    						dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-msr', type = "number", debounce = True, value = default_input['savings/losses sharing arrangement']['msr']),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
	                    					],
                                            style={"padding-top":"1rem"}
	                    				),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.H2("ACO's Sharing", style={"font-size":"0.8rem"}),width=4),
                                                dbc.Col(dbc.Checklist(options = [{'label':'Quality Adjustment', 'value' : 'selected'}], value = [], id = 'switch-saving-method'))
                                            ],
                                            style={"padding-top":"1rem"}),
				                        dbc.Row(
	                    					[
	                    						dbc.Col(html.Div(), width = 1),
                                                dbc.Col(html.Div(id = 'text-saving'),width=3),
	                    						dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom savings sharing']),style={"text-align":"center"},width=4),
	                    						dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-planshare', type = "number", debounce = True, value = default_input['savings/losses sharing arrangement']['savings sharing']),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
	                    					],
                                            style={"padding-top":"1rem"}
	                    				),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.Div(), width = 1),
                                                dbc.Col(html.H5("Min Sharing %", id = 'text-saving-min', style={"font-size":"0.6rem"}),width=3),
                                                dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom savings sharing min'],id = 'text-saving-min-recom'),style={"text-align":"center"},width=4),
                                                dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-planshare-min', type = "number", disabled = True, debounce = True, value = default_input['savings/losses sharing arrangement']['savings sharing min']),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
                                            ],
                                            style={"padding-top":"1rem"}
                                        ),
                                        dbc.Row([
                                            dbc.Col(html.Div(), width = 1),
                                            dbc.Col(html.H5("First Dollar Sharing", id = 'text-saving-left',style={"font-size":"0.6rem"}),width=3),
                                            dbc.Col(daq.ToggleSwitch(id = 'toggleswitch-firstdollar-saving', value = False, size = 30, color = 'blue'), width = 4),
                                            dbc.Col(html.H5("Second Dollar Sharing (Above MSR)", id = 'text-saving-right',style={"font-size":"0.6rem"}),width=4),
                                            ],
                                             style={"padding-top":"1rem"}
                                        ),
                                        dbc.Row([
                                            dbc.Col(html.Div(), width = 1),
                                            ],
                                             style={"padding-top":"3.2rem"}
                                        ),
	                    				dbc.Row(
	                    					[
	                    						dbc.Col(html.H2("Shared Savings Cap", style={"font-size":"0.8rem"}),width=4),
	                    						dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom savings share cap']),style={"text-align":"center"},width=4),
	                    						dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-sharecap', type = "number", debounce = True, value = default_input['savings/losses sharing arrangement']['savings share cap']),
                                                    dbc.InputGroupAddon('% of target', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
	                    					],
                                            style={"padding-top":"1rem"}
	                    				),
                                	],
                                    style={"border-radius":"0.5rem", "background-color":"#fff", "padding":"1rem"}
                                ),
                                dbc.Col(width=1),
                                dbc.Col(
                                	[
                                		dbc.Checklist(
                                            options = [{'label': "Shared Losses", 'value': 'Shared Losses'}], 
                                            value = [], 
                                            id = 'switch-share-loss',
                                            switch = True,
                                            style={"font-family":"NotoSans-CondensedLight"}),
                                        html.Hr(),
                                		dbc.Row(
	                    					[
	                    						dbc.Col(html.Div(),width=4),
	                    						dbc.Col(html.H6("Recommended"),width=4),
	                    						dbc.Col(html.H6("User Defined"),width=4),
	                    					],
	                            			style={"text-align":"center"},
	                            			
	                    				),
	                    				dbc.Row(
	                    					[
	                    						dbc.Col(html.H2("MLR (Minimum Losses Rate)", style={"font-size":"0.8rem"}),width=4),
	                    						dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom mlr']),style={"text-align":"center"},width=4),
	                    						dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-mlr', type = "number", step = 0.1, debounce = True, value = default_input['savings/losses sharing arrangement']['mlr']),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
	                    					],
                                            style={"padding-top":"1rem"}
	                    				),
                                        dbc.Row([
                                            dbc.Col(html.H2("ACO's Sharing", style={"font-size":"0.8rem"}),width=4),
                                            dbc.Col(dbc.Checklist(options = [{'label':'Quality Adjustment', 'value' : 'selected'}], value = [], id = 'switch-loss-method'))
                                            ],
                                            style={"padding-top":"1rem"}),
				                        dbc.Row(
	                    					[
                                                dbc.Col(html.Div(), width = 1),
	                    						dbc.Col(html.Div(id = 'text-loss'),width=3),
	                    						dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom losses sharing min']),style={"text-align":"center"},width=4),
	                    						dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-planshare-l-min', type = "number", debounce = True, value = default_input['savings/losses sharing arrangement']['losses sharing min']),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
	                    					],
                                            style={"padding-top":"1rem"}
	                    				),
                                        dbc.Row(
                                            [
                                                dbc.Col(html.Div(), width = 1),
                                                dbc.Col(html.H5("Max Sharing %", style={"font-size":"0.6rem"}, id = 'text-loss-max'),width=3),
                                                dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom losses sharing'], id = 'text-loss-max-recom'),style={"text-align":"center"},width=4),
                                                dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-planshare-l', type = "number", debounce = True, value = default_input['savings/losses sharing arrangement']['losses sharing']),
                                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
                                            ],
                                            style={"padding-top":"1rem"}
                                        ),
                                        dbc.Row([
                                            dbc.Col(html.Div(), width = 1),
                                            dbc.Col(html.H5("First Dollar Sharing", id = 'text-loss-left',style={"font-size":"0.6rem"}),width=3),
                                            dbc.Col(daq.ToggleSwitch(id = 'toggleswitch-firstdollar-loss', value = False, size = 30, color = 'blue'), width = 4),
                                            dbc.Col(html.H5("Second Dollar Sharing (Below MLR)", id = 'text-loss-right',style={"font-size":"0.6rem"}),width=4),
                                            ],
                                             style={"padding-top":"1rem"}
                                        ),
                                        dbc.Row([
                                            dbc.Col(html.Div(), width = 1),
                                            dbc.Col(dbc.Checklist(options = [{'label':"Quality Adjusted Sharing Rate", 'value':"Quality Adjusted Sharing Rate"}], id = 'switch-quality-adj-rate',style={"font-size":"0.6rem"}),width=3),
                                            ],
                                             style={"padding-top":"1rem"}
                                        ),
	                    				dbc.Row(
	                    					[
	                    						dbc.Col(html.H2("Shared Losses Cap", style={"font-size":"0.8rem"}),width=4),
	                    						dbc.Col(html.H6(default_input['savings/losses sharing arrangement']['recom losses share cap']),style={"text-align":"center"},width=4),
	                    						dbc.Col([
                                                    dbc.InputGroup([
                                                    dbc.Input(id = 'input-usr-sharecap-l', type = "number", debounce = True, value = default_input['savings/losses sharing arrangement']['losses share cap']),
                                                    dbc.InputGroupAddon('% of target', addon_type = 'append'),
                                                    ],
                                                    size="sm")
                                                    ],style={"text-align":"center", "margin-top":"-0.5rem"},width=4),
	                    					],
                                            style={"padding-top":"1rem"}
	                    				),
                                	],
                                    style={"border-radius":"0.5rem", "background-color":"#fff", "padding":"1rem"}
                                ),
                            ],
                            style={"padding-left":"2rem", "padding-right":"2rem", "padding-top":"1rem", "padding-bottom":"1rem"}
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
                                dbc.Col(html.H4("Quality Adjustment", style={"font-size":"1rem", "margin-left":"10px"}), width=2),
                                dbc.Col(dbc.Button("Edit", className="mb-3",
                                            style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.7rem", "width":"4rem"},
                                            id = 'button-show-meas')),
                                
                            ],
                            no_gutters=True,
                        ),
                        html.Div([
                            html.Div([qualitytable(df_quality)],id='container-measure-setup', style={"padding-bottom":"1rem"}),
                            dbc.Row(
                                [
                                    dbc.Col(html.H2("Total Weight", style={"font-size":"1rem", "margin-left":"10px"}), width=10),
                                    dbc.Col(html.Div("100%", id = 'div-recom-overall', style={"text-align":"center","background-color":"#fff","border-radius":"10rem","font-size":"0.8rem"}), style={"padding-left":"0.5rem","padding-right":"0.3rem"}),
                                    dbc.Col(html.Div("100%", id ='div-usr-overall', style={"text-align":"center","background-color":"#fff","border-radius":"10rem","font-size":"0.8rem"}), style={"padding-left":"0.3rem"}),
                                ],
                                no_gutters=True,
                                style={"padding-right":"0.5rem","padding-top":"0.5rem", "padding-bottom":"0.2rem", "background-color":"#bbd4ff", "border-radius":"10rem","width":"101.5%"}
                            ),], id = 'div-meas-table-container', hidden = True, style={"padding-left":"4rem", "padding-right":"1rem"}),
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
                            dbc.Col([
                                dbc.Button("Edit Scenario Assumptions",
                                    className="mb-3",
                                    style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Black", "font-size":"1rem"},
                                    id = 'button-open-assump-modal'
                                ),
                            	dbc.Modal([
                            		dbc.ModalHeader(html.H1("Key Simulation Assumptions", style={"font-family":"NotoSans-Black","font-size":"1.5rem"})),
                            		dbc.ModalBody([sim_assump_input_session(),]),
                            		dbc.ModalFooter(
                            			dbc.Button('Close', id = 'button-close-assump-modal'))
                            		], id = 'modal-assump', size = 'xl', backdrop = 'static'),
                            	],
                                style={"padding-top":"1rem"}
                            ),
                            
                        ]
                    ),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                        dbc.Col(html.H4("Plan's Financial Projection", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                        dbc.Col(html.Div(html.H2("Metric", style={"padding":"0.5rem","color":"#fff", "background-color":"#1357DD", "font-size":"1rem", "border-radius":"0.5rem"}), style={"padding-right":"1rem"}), width="auto"),
                                        dbc.Col(dcc.Dropdown(
                                        	id = 'dropdown-cost',
                                        	options = [
                                        	{'label' : "Plan's Total Cost", 'value' : "Plan's Total Cost" },
                                        	{'label' : "ACO's Total Cost", 'value' : "ACO's Total Cost" },
                                        	{'label' : "ACO's PMPM", 'value' : "ACO's PMPM" },
                                        	],#{'label' : "Plan's Total Revenue", 'value' : "Plan's Total Revenue" }
                                            value = "ACO's PMPM",
                                        	))
                                    ],
                                    no_gutters=True,
                                ),
                                html.Div(
                                    dbc.Row(
                                        [
                                            dbc.Col(html.Div("1"), width=1),
                                            dbc.Col(dcc.Graph(id = 'figure-cost',config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},style={"height":"45vh", "width":"60vh"}), width=5),
                                            dbc.Col(html.Div(id = 'table-cost'), width=6),
                                        ],
                                        no_gutters=True,
                                    ),
                                    style={"padding":"1rem"}
                                )
                                
                            ],
                            className="mb-3",
                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem", "padding-top":"1rem"}
                        ),
                        style={"padding-top":"1rem"}
                    ),
                    
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                        dbc.Col(html.H4("ACO's Financial Projection", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                        dbc.Col(html.Div(html.H2("Metric", style={"padding":"0.5rem","color":"#fff", "background-color":"#1357DD", "font-size":"1rem", "border-radius":"0.5rem"}), style={"padding-right":"1rem"}), width="auto"),
                                        dbc.Col(dcc.Dropdown(
                                        	id = 'dropdown-fin',
                                        	options = [
                                        	{'label' : "ACO's Total Revenue", 'value' : "ACO's Total Revenue" },
                                        	{'label' : "ACO's Margin", 'value' : "ACO's Margin" },
                                        	{'label' : "ACO's Margin %", 'value' : "ACO's Margin %" }],
                                            value = "ACO's Total Revenue",
                                        	))
                                    ],
                                    no_gutters=True,
                                ),
                                html.Div(
                                    dbc.Row(
                                        [
                                            dbc.Col(html.Div("1"), width=1),
                                            dbc.Col(dcc.Graph(id = 'figure-fin',config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},style={"height":"45vh", "width":"60vh"}), width=5),
                                            dbc.Col(html.Div(id = 'table-fin'), width=6),
                                        ],
                                        no_gutters=True,
                                    ),
                                    style={"padding":"1rem"}
                                )
                                
                            ],
                            className="mb-3",
                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem", "padding-top":"1rem"}
                        )
                    )
                ],
                style={"padding-top":"2rem","padding-bottom":"2rem","padding-left":"1rem","padding-right":"1rem"}

        )

def sim_assump_input_session():
    return html.Div([
        html.Div(
            dbc.Row([
                dbc.Col(html.H1("Additional Patients Steered to ACO", style={"font-size":"1rem"})),
                dbc.Col([dbc.Input(value = "0%",)], width=3)
                ],
                style={"padding":"1rem","background-color":"#f3f3f3","border-radius":"0.5rem"}
            ),
            style={"padding-left":"1rem","padding-right":"1rem", "padding-bottom":"1rem"}
        ),

        html.Div(
            dbc.Row([
                dbc.Col(html.H1("Medical Cost Trend (without management)", style={"font-size":"1rem"})),
                dbc.Col([dbc.Input(value = "5.6%",)], width=3)
                ],
                style={"padding":"1rem","background-color":"#f3f3f3","border-radius":"0.5rem"}
            ),
            style={"padding-left":"1rem","padding-right":"1rem", "padding-bottom":"1rem"}
        ),
        
        html.Div(
            dbc.Row([
                dbc.Col(html.H1("Assumed Cost Trend Reduction", style={"font-size":"1rem"})),
                dbc.Col([dbc.Input(value = "-2.4%",)], width=3)
                ],
                style={"padding":"1rem","background-color":"#f3f3f3","border-radius":"0.5rem"}
            ),
            style={"padding-left":"1rem","padding-right":"1rem", "padding-bottom":"1rem"}
        ),

        html.Div(
            dbc.Row([
                dbc.Col(html.H1("Coding Improvement", style={"font-size":"1rem"})),
                dbc.Col([dbc.Input(value = "0.7%",)], width=3)
                ],
                style={"padding":"1rem","background-color":"#f3f3f3","border-radius":"0.5rem"}
            ),
            style={"padding-left":"1rem","padding-right":"1rem", "padding-bottom":"1rem"}
        ),

        html.Div(
            html.Div(
                [
                dbc.Row([
                    dbc.Col(html.H1("Quality Improvement", style={"font-size":"1rem"})),
                    ],
                    style={"padding":"1rem"}
                ),
                html.Hr(),
                dbc.Row([
                    dbc.Col([html.H1("Patient/ Caregiver Experience", style={"font-size":"0.8rem"})], width=3),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col("CAHPS: Getting Timely Care, Appointments, and Information"),
                            dbc.Col([dbc.Input(value = "10%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("CAHPS: How Well Your Providers Communicate"),
                            dbc.Col([dbc.Input(value = "10%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("CAHPS: Patients’ Rating of Provider"),
                            dbc.Col([dbc.Input(value = "10%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("CAHPS: Access to Specialists"),
                            dbc.Col([dbc.Input(value = "10%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("CAHPS: Health Promotion and Education"),
                            dbc.Col([dbc.Input(value = "10%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("CAHPS: Shared Decision Making"),
                            dbc.Col([dbc.Input(value = "0%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("CAHPS: Health Status/Functional Status"),
                            dbc.Col([dbc.Input(value = "0%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("CAHPS: Stewardship of Patient Resources"),
                            dbc.Col([dbc.Input(value = "0%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("CAHPS: Courteous and Helpful Office Staff"),
                            dbc.Col([dbc.Input(value = "0%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("CAHPS: Care Coordination"),
                            dbc.Col([dbc.Input(value = "0%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        ]),
                    ],
                    style={"padding":"1rem"}
                ),
                html.Hr(),
                dbc.Row([
                    dbc.Col([html.H1("Care Coordination/ Patient Safety", style={"font-size":"0.8rem"})], width=3),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col("Risk-Standardized, All Condition Readmission"),
                            dbc.Col([dbc.Input(value = "20%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("All-Cause Unplanned Admissions for Patients with Multiple Chronic Conditions"),
                            dbc.Col([dbc.Input(value = "20%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("Ambulatory Sensitive Condition Acute Composite (AHRQ Prevention Quality Indicator (PQI)#91)"),
                            dbc.Col([dbc.Input(value = "20%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("Falls: Screening for Future Fall Risk"),
                            dbc.Col([dbc.Input(value = "15%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        ]),
                    ],
                    style={"padding":"1rem"}
                ),
                html.Hr(),
                dbc.Row([
                    dbc.Col([html.H1("Preventive Health", style={"font-size":"0.8rem"})], width=3),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col("Preventive Care and Screening: Influenza Immunization"),
                            dbc.Col([dbc.Input(value = "25%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("Preventive Care and Screening:Tobacco Use: Screening and Cessation Intervention"),
                            dbc.Col([dbc.Input(value = "0%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("Preventive Care and Screening:Screening for Depression and Follow-up Plan"),
                            dbc.Col([dbc.Input(value = "0%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("Colorectal Cancer Screening"),
                            dbc.Col([dbc.Input(value = "10%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("Breast Cancer Screening"),
                            dbc.Col([dbc.Input(value = "10%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("Statin Therapy for the Prevention and Treatment of Cardiovascular Disease"),
                            dbc.Col([dbc.Input(value = "0%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        ]),
                    ],
                    style={"padding":"1rem"}
                ),
                html.Hr(),
                dbc.Row([
                    dbc.Col([html.H1("At-Risk Population", style={"font-size":"0.8rem"})], width=3),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col("Depression Remission at Twelve Months"),
                            dbc.Col([dbc.Input(value = "0%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("Diabetes Mellitus: Hemoglobin A1c Poor Control"),
                            dbc.Col([dbc.Input(value = "20%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        dbc.Row([
                            dbc.Col("Hypertension (HTN): Controlling High Blood Pressure"),
                            dbc.Col([dbc.Input(value = "10%")], width=4)], style={"padding-bottom":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"}),
                        ]),
                    ],
                    style={"padding":"1rem"}
                ),
                ],
                style={"background-color":"#f3f3f3","border-radius":"0.5rem"}
            ),
            style={"padding-bottom":"1rem"}
        ),

        html.Div(
            dbc.Row([
                dbc.Col(html.H1("ACO's Margin under FFS", style={"font-size":"1rem"})),
                dbc.Col([dbc.Input(value = "5%",)], width=3)
                ],
                style={"padding":"1rem","background-color":"#f3f3f3","border-radius":"0.5rem"}
            ),
            style={"padding-left":"1rem","padding-right":"1rem", "padding-bottom":"1rem"}
        ),
        

        
        ]
    )


app.layout = create_layout(app)

@app.callback(
    [Output('text-saving-left', 'style'),
    Output("text-saving-right", 'style')],
    [Input('toggleswitch-firstdollar-saving', 'value')]
    )
def toogle_saving(v):
    if v == False:
        return {"font-size":"0.6rem", "color":'blue'},{"font-size":"0.6rem"}
    return {"font-size":"0.6rem"},{"font-size":"0.6rem", 'color':'blue'}

@app.callback(
    [Output('text-loss-left', 'style'),
    Output("text-loss-right", 'style')],
    [Input('toggleswitch-firstdollar-loss', 'value')]
    )
def toogle_saving(v):
    if v == False:
        return {"font-size":"0.6rem", "color":'blue'},{"font-size":"0.6rem"}
    return {"font-size":"0.6rem"},{"font-size":"0.6rem", 'color':'blue'}

@app.callback(
    [Output('text-saving', 'children'),
    Output('input-usr-planshare-min', 'disabled'),
    Output('text-saving-min', 'style'),
    Output('text-saving-min-recom', 'style')],
    [Input('switch-saving-method', 'value')]
    )
def toggle_saving_method(v):
    if v and len(v)>0:
        return [html.H5("Max Sharing % (When quality targets are met)", style={"font-size":"0.6rem"})], False,{"font-size":"0.6rem"},{}
    return [html.H5("Sharing %", style={"font-size":"0.6rem"})],True,{"font-size":"0.6rem", "color":'#919191'},{"color":'#919191'}

@app.callback(
    [Output('text-loss', 'children'),
    Output('input-usr-planshare-l', 'disabled'),
    Output('text-loss-max', 'style'),
    Output('text-loss-max-recom', 'style'),
    Output('switch-quality-adj-rate', 'options')],
    [Input('switch-loss-method', 'value')]
    )
def toggle_loss_method(v):
    if v and len(v)>0:
        return [html.H5("Min Sharing % (When quality targets are met)", style={"font-size":"0.6rem"})], False,{"font-size":"0.6rem"},{}, [{'label':"Quality Adjusted Sharing Rate", 'value':"Quality Adjusted Sharing Rate", 'disabled':False}]
    return [html.H5("Sharing %", style={"font-size":"0.6rem"})],True,{"font-size":"0.6rem", "color":'#919191'},{"color":'#919191'}, [{'label':"Quality Adjusted Sharing Rate", 'value':"Quality Adjusted Sharing Rate", 'disabled':True}]



@app.callback(
    [Output('input-usr-mlr', 'disabled'),
#    Output('input-usr-planshare-l', 'disabled'),
    Output('input-usr-sharecap-l', 'disabled'),
    Output('input-usr-planshare-l-min', 'disabled'),
    Output('toggleswitch-firstdollar-loss', 'disabled'),
    Output('switch-loss-method', 'options')],
    [Input('switch-share-loss', 'value')]
    )
def toggle_share_loss(v):
    if 'Shared Losses' in v:
        return False, False, False, False, [{'label':'1 - Quality Adjustment', 'value' : 'selected'}]
    return True, True, True, True, [{'label':'1 - Quality Adjustment', 'value' : 'selected', 'disabled' : True}]


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
    Output('div-usr-tgt', 'children'),
    [Input('input-usr-tgt-trend', 'value')]
    )
def update_usr_target(v):
    base = default_input['medical cost target']['medical cost pmpm']
    base = int(base.replace("$",""))
    if v:
        tgt = int(round(base*v/100+base,0))
        return '$'+str(tgt)
    else:
        return '$800'
   

@app.callback(
    Output('div-usr-like', 'children'),
    [Input('div-usr-tgt', 'children')],
    [State('div-recom-like', 'children'),
    State('div-recom-tgt', 'children')]
    )
def cal_usr_like(usr_tgt, recom_like, recom_tgt):

    if usr_tgt:
        recom_tgt_int = int(recom_tgt.replace('$','').replace('%','').replace(',',''))
        usr_tgt_int = int(usr_tgt.replace('$','').replace('%','').replace(',',''))
        if usr_tgt_int >= recom_tgt_int:
            return html.Div(html.H1("High",style={"text-align":"center", "padding-top":"2.5rem", "padding-bottom":"2.5rem", "font-size":"1.5rem","color":"#fff"}), style={"border-radius":"0.5rem", "background-color":"green"})
        elif usr_tgt_int < recom_tgt_int*0.95:
            return html.Div(html.H1("Low",style={"text-align":"center", "padding-top":"2.5rem", "padding-bottom":"2.5rem", "font-size":"1.5rem","color":"#fff"}), style={"border-radius":"0.5rem", "background-color":"red"})
        else:
            return html.Div(html.H1("Mid",style={"text-align":"center", "padding-top":"2.5rem", "padding-bottom":"2.5rem", "font-size":"1.5rem"}), style={"border-radius":"0.5rem", "background-color":"#fff"})
    else:
        return html.Div()

@app.callback(
	Output('modal-assump', 'is_open'),
	[Input('button-open-assump-modal', 'n_clicks'),
	Input('button-close-assump-modal', 'n_clicks'),],
	[State('modal-assump', 'is_open')]
	)
def toggle_modal(n1, n2, is_open):
	if n1 or n2:
		return not is_open
	return is_open

@app.callback(
    [Output('div-recom-overall', 'children'),
    Output('div-usr-overall', 'children')],
    [Input('table-measure-setup', 'data'),]
    )
def cal_overall_weight(data):
    
    df = pd.DataFrame(data)
    recom_overall = np.sum(int(i.replace('%','')) for i in list(df.fillna('0%').iloc[:,7]))
    usr_overall = np.sum(0 if i.replace('%','')=='' else int(i.replace('%','')) for i in list(df.fillna('0%').iloc[:,8]))
    return str(recom_overall)+'%', str(usr_overall)+'%'

# table style update on selected_rows
@app.callback(
    Output('container-measure-setup', 'children'),
    [Input('table-measure-setup', 'selected_rows'),],
    [State('table-measure-setup', 'data'),])
def update_columns(selected_quality, data):
    for i in range(0,23):
        row=data[i]

        if i in selected_quality:
            row['tar_user']=row['tar_recom']
            if i in [6,8,9,15,16,19,20]:
                row['tar_user_type']='Report'
            else:
                row['tar_user_type']='Performance'
        else:
            row['tar_user']=float('nan')
            row['tar_user_type']=float('nan')

    return qualitytable(pd.DataFrame.from_dict(data),selected_quality)

# set up table selfupdate
@app.callback(
    Output('table-measure-setup', 'data'),
    [Input('table-measure-setup', 'data_timestamp'),],
    [State('table-measure-setup', 'data'),
     State('table-measure-setup', 'selected_rows'),])
def update_columns(timestamp, data,selected_quality):
    for i in range(0,23):
        row=data[i]
        if i in [4,11,16,21]:  
            row['userdefined']=str(row['userdefined']).replace('$','').replace('%','').replace(',','')+'%'
        else:
            row['userdefined']=float('nan')

        if i in selected_quality:
            if row['tar_user_type']=='Report':
                row['tar_user']='R'
            elif row['tar_user_type']=='Performance' and  row['tar_user']=='R':
                if row['tar_recom']=='R':
                    row['tar_user']=row['bic']

                else:
                    row['tar_user']=row['tar_recom']
            else:
                if i in range(10,23):
                    row['tar_user']=str(row['tar_user']).replace('$','').replace('%','').replace(',','')+'%'


        else:
            row['tar_user']=float('nan')

    return data  

# store data
@app.callback(
	Output('temp-data', 'children'),
	[Input('div-usr-tgt', 'children'),
	Input('input-usr-msr', 'value'),
	Input('input-usr-planshare', 'value'),
    Input('input-usr-planshare-min', 'value'),
	Input('input-usr-sharecap', 'value'),
	Input('input-usr-mlr', 'value'),
	Input('input-usr-planshare-l', 'value'),
    Input('input-usr-planshare-l-min', 'value'),
	Input('input-usr-sharecap-l', 'value'),
    Input('switch-share-loss', 'value'),
    Input('switch-loss-method', 'value'),
    Input('table-measure-setup', 'selected_rows'),
    Input('table-measure-setup', 'data')]
	)
def store_data(usr_tgt_int, usr_msr, usr_planshare, usr_planshare_min, usr_sharecap, usr_mlr, usr_planshare_l, usr_planshare_l_min, usr_sharecap_l, ts, lm, select_row, data):
    df = pd.DataFrame(data)

    if 'Shared Losses' in ts:
        two_side = True
    else:
        two_side = False

    if 'selected' in lm:
        loss_method = True
    else:
        loss_method = False


    usr_tgt = int(usr_tgt_int.replace('$',""))

    recom_dom_1 = int(df.iloc[4,7].replace('%',""))/100
    recom_dom_2 = int(df.iloc[11,7].replace('%',""))/100
    recom_dom_3 = int(df.iloc[16,7].replace('%',""))/100
    recom_dom_4 = int(df.iloc[21,7].replace('%',""))/100

    usr_dom_1 =(0 if df.iloc[4,8].replace('%','')=='' else int(df.iloc[4,8].replace('%',"")))/100
    usr_dom_2 =(0 if df.iloc[11,8].replace('%','')=='' else  int(df.iloc[11,8].replace('%',"")))/100
    usr_dom_3 =(0 if df.iloc[16,8].replace('%','')=='' else  int(df.iloc[16,8].replace('%',"")))/100
    usr_dom_4 =(0 if df.iloc[21,8].replace('%','')=='' else  int(df.iloc[21,8].replace('%',"")))/100

    user_tar_type=df['tar_user_type'].tolist()
    user_tar_value=df['tar_user'].tolist()

    datasets = {
        'medical cost target' : {'user target' : usr_tgt},
        'savings/losses sharing arrangement' : {'two side' : two_side, 'msr': usr_msr, 'savings sharing' : usr_planshare, 'savings sharing min' : usr_planshare_min, 'savings share cap' : usr_sharecap,
        'mlr' : usr_mlr, 'losses sharing' : usr_planshare_l, 'losses sharing min' : usr_planshare_l_min, 'losses share cap' : usr_sharecap_l, 'loss method' : loss_method},
        'quality adjustment' : {'selected measures' : select_row, 'recom_dom_1' : recom_dom_1, 'recom_dom_2' : recom_dom_2, 'recom_dom_3' : recom_dom_3, 'recom_dom_4' : recom_dom_4,
        'usr_dom_1' : usr_dom_1, 'usr_dom_2' : usr_dom_2, 'usr_dom_3' : usr_dom_3, 'usr_dom_4' : usr_dom_4,
        'user_tar_type':user_tar_type,'user_tar_value':user_tar_value}
    }
    
    with open('configure/input_ds.json','w') as outfile:
        json.dump(datasets, outfile)
    return json.dumps(datasets)

@app.callback(
    [Output('tab_container', 'active_tab'),
    Output('temp-result', 'children')],
    [Input('button-submit-simulation', 'n_clicks')],
    [State('temp-data', 'children')]
    )
def cal_simulation(submit, data):
    if submit:
        datasets = json.loads(data)
        selected_rows = datasets['quality adjustment']['selected measures']
        domian_weight =list( map(datasets['quality adjustment'].get, ['usr_dom_1','usr_dom_2','usr_dom_3','usr_dom_4']) ) 
        target_user_pmpm = datasets['medical cost target']['user target']
        msr_user = datasets['savings/losses sharing arrangement']['msr']/100
        mlr_user = datasets['savings/losses sharing arrangement']['mlr']
        max_user_savepct = datasets['savings/losses sharing arrangement']['savings sharing']/100
        min_user_savepct = datasets['savings/losses sharing arrangement']['savings sharing min']/100
        max_user_losspct = datasets['savings/losses sharing arrangement']['losses sharing']
        min_user_losspct = datasets['savings/losses sharing arrangement']['losses sharing min']
        cap_user_savepct = datasets['savings/losses sharing arrangement']['savings share cap']/100
        cap_user_losspct = datasets['savings/losses sharing arrangement']['losses share cap']
        twosided = datasets['savings/losses sharing arrangement']['two side']
        lossmethod = datasets['savings/losses sharing arrangement']['loss method']
        user_tar_type=datasets['quality adjustment']['user_tar_type']
        user_tar_value=datasets['quality adjustment']['user_tar_value']

        if twosided == True:
            mlr_user = mlr_user/100
            max_user_losspct = max_user_losspct/100
            min_user_losspct = min_user_losspct/100
            cap_user_losspct = cap_user_losspct/100

        df=simulation_cal(selected_rows,domian_weight,user_tar_type,user_tar_value,default_input,target_user_pmpm,msr_user,mlr_user,max_user_savepct,min_user_savepct,min_user_losspct,max_user_losspct,cap_user_savepct,cap_user_losspct,twosided,lossmethod)

        return 'tab-1', df.to_json(orient = 'split')
    return 'tab-0', ""

@app.callback(
    [Output('figure-cost', 'figure'),
    Output('table-cost', 'children')],
    [Input('dropdown-cost', 'value'),
    Input('temp-result', 'children')]
    )
def update_grapg_cost(metric, data):
    if data:
        dff = pd.read_json(data, orient = 'split')
        df = dff[dff['Metrics'] == metric]
        return sim_result_box(df), table_sim_result(df)
    return {},""

@app.callback(
    [Output('figure-fin', 'figure'),
    Output('table-fin', 'children')],
    [Input('dropdown-fin', 'value'),
    Input('temp-result', 'children')]
    )
def update_grapg_cost(metric, data):
    if data:
        dff = pd.read_json(data, orient = 'split')
        df = dff[dff['Metrics'] == metric]
        return sim_result_box(df),table_sim_result(df)
    return {}, ""

if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True,port=8049)


