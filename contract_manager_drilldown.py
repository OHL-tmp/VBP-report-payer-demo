#!/usr/bin/env python3

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

import pandas as pd
import numpy as np

import pathlib
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State

from utils import *
from figure import *

from modal_drilldown_tableview import *


app = dash.Dash(__name__, url_base_pathname='/vbc-payer-demo/contract-manager-drilldown/')

server = app.server


def create_layout(app):
#    load_data()
    return html.Div(
                [ 
                    html.Div([Header_mgmt(app, False, True, False, False)], style={"height":"6rem"}, className = "sticky-top navbar-expand-lg"),
                    
                    html.Div(
                        [
                            col_content_drilldown(app),
                        ],
                        className="mb-3",
                        style={"padding-left":"3rem", "padding-right":"3rem","padding-top":"1rem"},
                    ),
                    
                ],
                style={"background-color":"#f5f5f5"},
            )


def col_menu_drilldown():

	return html.Div(
				[
                    dbc.Row(
                        [
                            dbc.Col(html.Hr(className="ml-1", style={"background-color":"#1357DD"})),
                            dbc.Col(dropdownmenu_select_measures(), width="auto"),
                            dbc.Col(html.Hr(className="ml-1", style={"background-color":"#1357DD"})),
                            #dbc.Col(card_selected_measures(),)
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.Div()),
                            dbc.Col(html.H6("click to change measure", style={"font-size":"0.6rem"}), width="auto"),
                            dbc.Col(html.Div()),
                            #dbc.Col(card_selected_measures(),)
                        ]
                    )
				],
                style={"padding":"0.5rem"}
			)


def dropdownmenu_select_measures():
	return dbc.DropdownMenu(
                [
                    dbc.DropdownMenuItem("Drilldown Menu", header=True),
                    dbc.DropdownMenuItem("Total Cost"),
                    dbc.DropdownMenuItem("Quality Measures"),
                    dbc.DropdownMenuItem("Physician Profiling"),
                    dbc.DropdownMenuItem("Intervention Opportunities"),
                    dbc.DropdownMenuItem(divider=True),
                    html.P(
                        "Select one to drill.",
                    style={"padding-left":"1rem", "font-size":"0.6rem"}),
                ],
                label="Total Cost",
                toggle_style={"font-family":"NotoSans-SemiBold","font-size":"1.2rem","border-radius":"5rem","background-color":"#1357DD"},
            )


def col_content_drilldown(app):
	return html.Div(
			[
                html.Div([html.Div([col_menu_drilldown()], style={"border-radius":"5rem","background-color":"none"})], style={"padding-bottom":"3rem"}),
				dbc.Row(
					[
						dbc.Col(card_overview_drilldown(0.069),width=8),
						dbc.Col(card_key_driver_drilldown(app),width=4),
					]
				),
				card_confounding_factors(app),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Div(
                                        [
                                            html.H2("Drilldown Analysis Drilldown", style={"font-size":"3rem"}),
                                            html.H3("check table view for more details...", style={"font-size":"1rem"}),
                                        ],
                                        style={"padding-left":"2rem"}
                                    ), width=8),
                                dbc.Col(modal_drilldown_tableview(), width=4)
                            ]
                        )
                    ],
                    style={"padding-bottom":"1rem", "padding-top":"2rem"}
                ),
                html.Div(
                    dbc.Tabs(
                        [
                            dbc.Tab(tab_patient_cohort_analysis(), label="Patient Cohort Analysis", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
                            dbc.Tab(tab_clinical_condition_analysis(), label="Clinical Condition Analysis", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
                            dbc.Tab(tab_physician_analysis(), label="Physician Analysis", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
                        ], 
                        # id = 'tab_container'
                    ),
                )
                
			]
		)


def card_overview_drilldown(percentage):
    if percentage > 0:
        color = "#dc3545"
        condition = "worse than target"
    elif percentage == 0:
        color = "#1357DD"
        condition = "same as target"
    else:
        color = "#28a745"
        condition = "better than target"

    return html.Div(
			[
				dbc.Row(
                        [
                            dbc.Col(html.H1("ACO's Total Cost", style={"font-size":"1.6rem"}), width="auto"),
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H3("worse than target", style={"font-size":"0.8rem", "color":"#fff"}),
                                        html.H2(str(percentage*100)+"%", style={"font-size":"1.2rem", "margin-top":"-9px", "color":"#fff"}),
                                    ],
                                    style={"margin-top":"-20px"}
                                ),
                                style={"height":"2.5rem", "border":"none", "background-color":color, "text-align":"center", "margin-top":"-6px"},
                            ),
                        ],
                        style={"padding-left":"1rem"}
                    ),
                html.P("As of June 30th.", style={"color":"#000", "font-size":"0.8rem","padding-left":"1rem"}),
                html.Div(
                    [
                        dbc.Tabs(
                            [
                                dbc.Tab(html.Img(src=app.get_asset_url("logo-demo.png"), width="100%"), label="Total Cost", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
                                dbc.Tab(html.Img(src=app.get_asset_url("logo-demo.png"), width="100%"), label="PMPM", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
                                
                            ], 
                            # id = 'tab_container'
                        )
                    ],
                    className="mb-3",
                    style={"padding-left":"3rem", "padding-right":"3rem"},
                ),
            ],
		)


def card_key_driver_drilldown(app):
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
		                        dbc.Col(html.H4("Key Drivers", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                dbc.Col(
                                    [
                                        dbc.Button("See All Drivers",
                                                        # id = 'button-all-driver',
                                                        style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"},
                                                    ),
                                        # dbc.Modal([
                                        #         dbc.ModalHeader("All Drivers"),
                                        #         dbc.ModalBody(children = html.Div([table_driver_all(df_driver_all)], style={"padding":"1rem"})),
                                        #         dbc.ModalFooter(
                                        #                 dbc.Button("Close", 
                                        #                         # id = 'close-all-driver',
                                        #                         style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"},
                                        #                     )
                                        #                 )
                                        #         ], id = 'modal-all-driver', size="lg")
                                    ],
                                    width=3,
                                ),
                            ],
                            no_gutters=True,
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"))
                                    ],
                                    width=6),
                                dbc.Col(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"))
                                    ],
                                    width=6),
                                dbc.Col(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"))
                                    ],
                                    width=6),
                                
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )



def card_confounding_factors(app):
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Confounding Factors Unaccounted for in the Contract", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Col(element_confounding_factors(-0.002, "Change in Covered Services"), width=3),
                                dbc.Col(element_confounding_factors(0.003, "Benefit Change"), width=3),
                                dbc.Col(element_confounding_factors(-0.002, "Provider Contracting Change"), width=3),
                                dbc.Col(element_confounding_factors(-0.002, "Outlier Impact"), width=3),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )


def element_confounding_factors(percentage, factor):
    if percentage > 0:
        color = "danger"
    elif percentage == 0:
        color = "secondary"
    else:
        color = "success"

    return dbc.Row(
            [
                dbc.Col(dbc.Badge(str(percentage*100)+"%", color=color, className="mr-1"), width=3, style={"font-family":"NotoSans-SemiBold"}),
                dbc.Col(html.H6(factor, style = {"font-size":"1rem", "padding-top":"0.1rem"}), width=9),
            ],
            style={"padding":"1rem"}
        )

##### tab content #####
def tab_patient_cohort_analysis():
    return html.Div(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                        dbc.Col(html.H4("Patient Cohort Analysis: By Patient Risk Status", style={"font-size":"1rem", "margin-left":"10px"})),
                                        dbc.Col(
                                            dbc.Button("Modify Criteria",
                                                className="mb-3",
                                                style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem", "width":"8rem"},
                                                # id = 'button-submit-simulation'
                                            ),
                                            width=2
                                        )
                                    ],
                                    no_gutters=True,
                                ),
                                
                                html.Div(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"))
                                    ], 
                                    style={"max-height":"80rem"}
                                ),
                                html.Div(
                                    dbc.Button("Result Details",
                                        className="mb-3",
                                        style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem", "width":"8rem"},
                                        # id = 'button-submit-simulation'
                                    ),
                                    style={"text-align":"end", "padding-right":"5rem"}
                                ),
                                

                                html.Hr(),

                                dbc.Row(
                                    [
                                        dbc.Col(html.H4("Cost and Utilization by Service Categories", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                    ],
                                    no_gutters=True,
                                ),
                                
                                html.Div(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"))
                                    ], 
                                    style={"max-height":"80rem"}
                                ),

                                dbc.Row(
                                    [
                                        dbc.Col(html.H4("Drilldown by Subcategories", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                    ],
                                    no_gutters=True,
                                ),
                                
                                html.Div(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"))
                                    ], 
                                    style={"max-height":"80rem"}
                                ),

                                dbc.Row(
                                    [
                                        dbc.Col(html.H4("Other Key Utilization Measures", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                    ],
                                    no_gutters=True,
                                ),
                                
                                html.Div(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"))
                                    ], 
                                    style={"max-height":"80rem"}
                                ),
                            ]
                        ),
                        className="mb-3",
                        style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
                    ),

                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                        dbc.Col(html.H4("Total Cost Incurred In VS.Out of ACO", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                        
                                    ],
                                    no_gutters=True,
                                ),
                                
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png")), width=3),
                                        dbc.Col(
                                            html.Div(
                                                [
                                                    html.Img(src=app.get_asset_url("logo-demo.png")),
                                                    html.Img(src=app.get_asset_url("logo-demo.png")),
                                                ], 
                                                style={"max-height":"80rem"}
                                            ), 
                                            width=5
                                        ),
                                        dbc.Col(
                                            html.Div(
                                                [
                                                    html.Img(src=app.get_asset_url("logo-demo.png")),
                                                    html.Img(src=app.get_asset_url("logo-demo.png")),
                                                ], 
                                                style={"max-height":"80rem"}
                                            ), 
                                            width=4
                                        ),
                                    ]
                                    
                                ),
                            ]
                        ),
                        className="mb-3",
                        style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
                    ),
                ]
            )
            
def tab_clinical_condition_analysis():
    return html.Div(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                        dbc.Col(html.H4("Patient Cohort Analysis: By Patient Risk Status", style={"font-size":"1rem", "margin-left":"10px"})),
                                        dbc.Col(
                                            dbc.Button("Modify Criteria",
                                                className="mb-3",
                                                style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem", "width":"8rem"},
                                                # id = 'button-submit-simulation'
                                            ),
                                            width=2
                                        )
                                    ],
                                    no_gutters=True,
                                ),
                                
                                html.Div(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"))
                                    ], 
                                    style={"max-height":"80rem"}
                                ),
                                html.Div(
                                    dbc.Button("Result Details",
                                        className="mb-3",
                                        style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem", "width":"8rem"},
                                        # id = 'button-submit-simulation'
                                    ),
                                    style={"text-align":"end", "padding-right":"5rem"}
                                ),
                                

                                html.Hr(),

                                dbc.Row(
                                    [
                                        dbc.Col(html.H4("Cost and Utilization by Service Categories", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                    ],
                                    no_gutters=True,
                                ),
                                
                                html.Div(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"))
                                    ], 
                                    style={"max-height":"80rem"}
                                ),

                                dbc.Row(
                                    [
                                        dbc.Col(html.H4("Drilldown by Subcategories", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                    ],
                                    no_gutters=True,
                                ),
                                
                                html.Div(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"))
                                    ], 
                                    style={"max-height":"80rem"}
                                ),

                                dbc.Row(
                                    [
                                        dbc.Col(html.H4("Other Key Utilization Measures", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                    ],
                                    no_gutters=True,
                                ),
                                
                                html.Div(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"))
                                    ], 
                                    style={"max-height":"80rem"}
                                ),
                            ]
                        ),
                        className="mb-3",
                        style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
                    ),

                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                        dbc.Col(html.H4("Total Cost Incurred In VS.Out of ACO", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                        
                                    ],
                                    no_gutters=True,
                                ),
                                
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png")), width=3),
                                        dbc.Col(
                                            html.Div(
                                                [
                                                    html.Img(src=app.get_asset_url("logo-demo.png")),
                                                    html.Img(src=app.get_asset_url("logo-demo.png")),
                                                ], 
                                                style={"max-height":"80rem"}
                                            ), width=5
                                        ),
                                        dbc.Col(
                                            html.Div(
                                                [
                                                    html.Img(src=app.get_asset_url("logo-demo.png")),
                                                    html.Img(src=app.get_asset_url("logo-demo.png")),
                                                ], 
                                                style={"max-height":"80rem"}
                                            ), width=4
                                        ),   
                                    ]
                                    
                                ),
                            ]
                        ),
                        className="mb-3",
                        style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
                    ),
                ]
            )


def tab_physician_analysis():
    return html.Div(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                        dbc.Col(html.H4("Patient Cohort Analysis: By Patient Risk Status", style={"font-size":"1rem", "margin-left":"10px"})),
                                        dbc.Col(
                                            dbc.Button("Modify Criteria",
                                                className="mb-3",
                                                style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem", "width":"8rem"},
                                                # id = 'button-submit-simulation'
                                            ),
                                            width=2
                                        )
                                    ],
                                    no_gutters=True,
                                ),
                                
                                html.Div(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"))
                                    ], 
                                    style={"max-height":"80rem"}
                                ),
                                html.Div(
                                    dbc.Button("Result Details",
                                        className="mb-3",
                                        style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem", "width":"8rem"},
                                        # id = 'button-submit-simulation'
                                    ),
                                    style={"text-align":"end", "padding-right":"5rem"}
                                ),
                                

                                html.Hr(),

                                dbc.Row(
                                    [
                                        dbc.Col(html.H4("Cost and Utilization by Service Categories", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                    ],
                                    no_gutters=True,
                                ),
                                
                                html.Div(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"))
                                    ], 
                                    style={"max-height":"80rem"}
                                ),

                                dbc.Row(
                                    [
                                        dbc.Col(html.H4("Drilldown by Subcategories", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                    ],
                                    no_gutters=True,
                                ),
                                
                                html.Div(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"))
                                    ], 
                                    style={"max-height":"80rem"}
                                ),

                                dbc.Row(
                                    [
                                        dbc.Col(html.H4("Other Key Utilization Measures", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                    ],
                                    no_gutters=True,
                                ),
                                
                                html.Div(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"))
                                    ], 
                                    style={"max-height":"80rem"}
                                ),
                            ]
                        ),
                        className="mb-3",
                        style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
                    ),

                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                        dbc.Col(html.H4("Total Cost Incurred In VS.Out of ACO", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                        
                                    ],
                                    no_gutters=True,
                                ),
                                
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png")), width=3),
                                        dbc.Col(
                                            html.Div(
                                                [
                                                    html.Img(src=app.get_asset_url("logo-demo.png")),
                                                    html.Img(src=app.get_asset_url("logo-demo.png")),
                                                ], 
                                                style={"max-height":"80rem"}
                                            ), width=5
                                        ),
                                        dbc.Col(
                                            html.Div(
                                                [
                                                    html.Img(src=app.get_asset_url("logo-demo.png")),
                                                    html.Img(src=app.get_asset_url("logo-demo.png")),
                                                ], 
                                                style={"max-height":"80rem"}
                                            ), width=4
                                        ),
                                    ]
                                    
                                ),
                            ]
                        ),
                        className="mb-3",
                        style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
                    ),
                ]
            )


def card_graph1_performance_drilldown(app):
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Performance Drilldown by Patient Cohort", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(html.H1("By Comorbidity Type",id='dimname_on_lv1', style={"color":"#f0a800", "font-size":"1.5rem","padding-top":"0.8rem"}), width=9),
                                                dbc.Col(mod_criteria_button(), style={"padding-top":"0.8rem"}),
                                            ]
                                        )
                                    ],
                                    style={"padding-left":"2rem","padding-right":"1rem","border-radius":"5rem","background-color":"#f7f7f7","margin-top":"2rem"}
                                ), 
                                html.Div(drillgraph_lv1(drilldata_process(df_drilldown,'Patient Health Risk Level'),'dashtable_lv1','Patient Health Risk Level'),id="drill_lv1",style={"padding-top":"2rem","padding-bottom":"2rem"}), 
                            ], 
                            style={"max-height":"80rem"}
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )

def mod_criteria_button():
    return [
                                dbc.Button(
                                    "Click to modify criteria",
                                    id="button-mod-dim-lv1",
                                    className="mb-3",
                                    style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"},
                                ),
                                dbc.Popover([
                                    dbc.PopoverHeader("Modify criteria"),
                                    dbc.PopoverBody([
                                        html.Div(
                                            [
                                                dbc.RadioItems(
                                                    options = [{'label':c , 'value':c,'disabled' : False} if c not in disable_list else {'label':c , 'value':c,'disabled' : True} for c in dimensions
                                                              ],
                                                    value = "Patient Health Risk Level",
                                                    labelCheckedStyle={"color": "#057aff"},
                                                    id = "list-dim-lv1",
                                                    style={"font-family":"NotoSans-Condensed", "font-size":"0.8rem", "padding":"1rem"},
                                                ),
                                            ],
                                            style={"padding-top":"0.5rem", "padding-bottom":"2rem"}
                                        )
                                         
                                       
                                        
                                    ]
                                    ),
                                ],
                                id = "popover-mod-dim-lv1",
                                is_open = False,
                                target = "button-mod-dim-lv1",
                                placement = "top",
                                ),
                                
                            ]
    


app.layout = create_layout(app)


if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True)









