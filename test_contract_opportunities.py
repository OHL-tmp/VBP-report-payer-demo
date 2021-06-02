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
import math

import pathlib
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State

from utils import *
from figure import *


from app import app

#app = dash.Dash(__name__, url_base_pathname='/vbc-demo/')

#server = app.server

global default_input, custom_input

df_aco_bench = pd.read_csv('data/df_aco_bench.csv')
df_aco_byoppo = pd.read_csv('data/df_aco_byoppo.csv')
df_aco_oppo_dtl = pd.read_csv('data/df_aco_oppo_dtl.csv')
aco_oppo_drill_mapping = pd.read_csv('data/aco_oppo_drill_mapping.csv')
df_aco_oppo_drill = pd.read_csv('data/df_aco_oppo_drill.csv')



df_bundle_oppo = pd.read_csv('data/df_bundle_oppo.csv')
df_bundle_costbyoppo = pd.read_csv('data/df_bundle_costbyoppo.csv')
df_bundle_trend = pd.read_csv('data/df_bundle_trend.csv')
df_bundle_costbysvc = pd.read_csv('data/df_bundle_costbysvc.csv')
df_bundle_bydrg = pd.read_csv('data/df_bundle_bydrg.csv')
df_bundle_byphy = pd.read_csv('data/df_bundle_byphy.csv')
df_bundle_byreadmitdrg = pd.read_csv('data/df_bundle_byreadmitdrg.csv')
df_bundle_byer = pd.read_csv('data/df_bundle_byer.csv')
df_bundle_pac_rate = pd.read_csv('data/df_bundle_pac_rate.csv')
df_bundle_pac_los = pd.read_csv('data/df_bundle_pac_los.csv')
df_bundle_dme = pd.read_csv('data/df_bundle_dme.csv')



#modebar display
button_to_rm=['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'hoverClosestCartesian','hoverCompareCartesian','hoverClosestGl2d', 'hoverClosestPie', 'toggleHover','toggleSpikelines']


def create_layout(app):
    global default_input, custom_input
#    load_data()
    return html.Div(
                [ 

                    html.Div([Header_contract(app, True, False, False, False)], style={"height":"6rem"}, className = "sticky-top navbar-expand-lg"),
                    
                    html.A(id="top"),

                    html.Div(
                        [
                            dbc.Tabs(
                                [
                                    dbc.Tab(tab_aco(app), label="ACO Opportunities", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
                                    dbc.Tab(tab_bundle(app), label="Bundled Payment Opportunities", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
                                    
                                ], id = 'tab_container'
                            )
                        ],
                        className="mb-3",
                        style={"padding-left":"3rem", "padding-right":"3rem"},
                    ),

                    # hidden div inside the app to store the temp data
                    html.Div(id = 'temp-data', style = {'display':'none'}),
                    html.Div(id = 'temp-result', style = {'display':'none'}),
                    html.Div(id = 'temp-carveout', style = {'display':'none'}),
                    
                ],
                style={"background-color":"#f5f5f5"},
            )

def tab_aco(app):
    return html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.H2("Summary of ACO Opportunities", style={"padding-left":"2rem","font-size":"3"}), width=8),
                        ],
                        style={"padding-top":"2rem"}
                    ),
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                                            dbc.Col(html.H4("Medical Cost Benchmarking(PMPM, risk adjusted)", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                                        ],
                                                        no_gutters=True,
                                                        style={"padding-bottom":"2rem"}
                                                    ),
                                                    html.Div(
                                                        [
                                                            dcc.Graph(figure=bundle_avgcost(df_aco_bench), config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},)
                                                        ],
                                                        style={"padding-bottom":"2.5rem"}
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.H6("· Provider group PMPM is 6.2% higher ($60 higher) than Benchmark", style={"padding-top":"0.5rem"}),
                                                            html.H6("· Provider group PMPM is 11.4% higher ($105 higher) than Best-in-class", style={"padding-bottom":"0.5rem"})
                                                        ],
                                                        style={"background-color":"#FFE2AA", "border":"none", "border-radius":"0.5rem","padding-left":"1rem"}
                                                    )
                                                ]
                                            ),
                                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
                                        ),
                                        width=6
                                    ),
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                                            dbc.Col(html.H4("Potential Cost Reduction Opportunities*", style={"font-size":"1rem", "margin-left":"10px"}), width="auto"),
                                                            dbc.Col(html.H4("(PMPM)", style={"font-size":"1rem", "margin-left":"10px"}, id="cost-reduction-unit")),
                                                            dbc.Col(dbc.Button("Cost PMPM", className="mb-3", style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.7rem", "width":"8rem","margin-right":"1rem"}, id="switch-cost-reduction-pmpm"), width="auto"),
                                                            dbc.Col(dbc.Button("Cost %", className="mb-3", style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.7rem", "width":"8rem"}, id="switch-cost-reduction-pct"), width="auto")
                                                        ],
                                                        no_gutters=True,
                                                        style={"padding-bottom":"2rem"}
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.Hr(),
                                                            html.Div(
                                                                dcc.Graph(figure=aco_vertical(df_aco_byoppo),config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,}, ),
                                                                hidden=False,
                                                                id="cost-reduction-pmpm"
                                                            ),
                                                            html.Div(
                                                                dcc.Graph(figure=aco_vertical(df_aco_byoppo, 'pct'), config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},),
                                                                hidden=True,
                                                                id="cost-reduction-pct"
                                                            ),
                                                        ],
                                                        style={"padding-bottom":"2.5rem"}
                                                    ),
                                                    html.H6('* Cost reduction opportunities could overlap between categories '),
                                                ]
                                            ),
                                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
                                        ),
                                        width=6
                                    ),
                                ]
                            )
                            
                        ],style={"padding":"2rem"}
                    ),
                    html.Hr(),
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(html.H2("Cost Reduction Opportunity Details", style={"padding-left":"2rem","font-size":"3","margin-right":"2rem"}), width="auto"),
                                    dbc.Col(
                                        html.Div(
                                            [
                                                dbc.Button("View Details", className="mb-3", style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.7rem", "width":"10rem","margin-left":"4rem"}, id="open-aco-drilldown-modal"),
                                                dbc.Modal(
                                                    [
                                                        dbc.ModalHeader("Additional Drilldown Details"),
                                                        dbc.ModalBody(
                                                            html.Div([
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(html.H4("OPPORTUNITY: ")),
                                                                        dbc.Col(dcc.Dropdown(
                                                                                        id='oppo-filter-acolv1',
                                                                                        options=[{'label': item['oppo_label'], 'value': item['oppo']} for item in aco_oppo_drill_mapping[['oppo','oppo_label']].drop_duplicates().to_dict('records')],
                                                                                        value=aco_oppo_drill_mapping['oppo'].values[0],
                                                                                        clearable=False,
                                                                                    )),
                                                                        dbc.Col(dcc.Dropdown(
                                                                                        id='oppo-filter-acolv2',
                                                                                        clearable=False,
                                                                                    )),
                                                                   ],
                                                                ),
                                                                html.Div(
                                                                    [
                                                                        html.H2(id = 'oppo-text-drilltable_desc',style={"font-size":"1rem","padding-bottom":"1rem"}),
                                                                        html.Div([aco_oppo_drill_tbl(df_aco_oppo_drill)])
                                                                    ],
                                                                    style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem","padding":"2rem","margin-top":"3rem"}
                                                                ),
                                                            ])
                                                        ),
                                                        dbc.ModalFooter(
                                                            dbc.Button(
                                                                "Close", id="close-aco-drilldown-modal", className="ml-auto"
                                                            )
                                                        ),
                                                    ],
                                                    id="aco-drilldown-modal",
                                                    size="xl",
                                                    scrollable=True
                                                )
                                            ]
                                        )
                                    )
                                ]
                            )
                        ],style={"padding-left":"2rem"}
                    ),
                    html.Div(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                                dbc.Col(html.H4("High Risk Patient Management", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                            ],
                                            no_gutters=True,
                                            style={"padding-bottom":"2rem"}
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Div(
                                                        [
                                                            html.Div(html.H6('Potential Cost Reduction Opportunities by Patient Disease(PMPM)\u2020', style={"font-weight":"bold"}), style={"text-align":"center", "padding-bottom":"1rem"}),
                                                            html.Div(
                                                                [
                                                                    dcc.Graph(figure=aco_oppo_bar(df_aco_oppo_dtl,'pat_manage'), config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},)
                                                                ],
                                                                style={"padding-bottom":"2.5rem"}
                                                            ),
                                                            html.H6('* Patient mix adjusted'),
                                                            html.H6('\u2020 Cost reduction opportunities could overlap between categories')
                                                        ]
                                                    ),
                                                    width=5
                                                ),
                                                dbc.Col(html.Div(),width=1),
                                                dbc.Col(
                                                    html.Div(
                                                        [
                                                            html.Div(html.H6('Patient PMPM', style={"font-weight":"bold"}), style={"text-align":"center", "padding-bottom":"3rem"}),
                                                            html.Div(
                                                                [
                                                                    aco_oppo_tbl(df_aco_oppo_dtl,'pat_manage')
                                                                ],
                                                                style={"padding-bottom":"2.5rem"}
                                                            )
                                                        ]
                                                    )
                                                ),
                                            ],
                                            style={"padding-left":"2rem", "padding-right":"2rem"}
                                        )
                                        
                                    ]
                                ),
                                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
                            ),
                            
                        ],style={"padding":"2rem"}
                    ),
                    html.Div(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                                dbc.Col(html.H4("Overuse Reduction", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                            ],
                                            no_gutters=True,
                                            style={"padding-bottom":"2rem"}
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Div(
                                                        [
                                                            html.Div(html.H6('Estimated Cost Reduction Opportunities by Service Type(PMPM)', style={"font-weight":"bold"}), style={"text-align":"center", "padding-bottom":"1rem"}),
                                                            html.Div(
                                                                [
                                                                    dcc.Graph(figure=aco_oppo_bar(df_aco_oppo_dtl,'overuse_reduction'), config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},)
                                                                ],
                                                                style={"padding-bottom":"2.5rem"}
                                                            ),
                                                            html.H6('* Patient mix adjusted')
                                                        ]
                                                    ),
                                                    width=5
                                                ),
                                                dbc.Col(html.Div(),width=1),
                                                dbc.Col(
                                                    html.Div(
                                                        [
                                                            html.Div(html.H6('Utilization Rate Comparison (units per 1,000 member)', style={"font-weight":"bold"}), style={"text-align":"center", "padding-bottom":"3rem"}),
                                                            html.Div(
                                                                [
                                                                    aco_oppo_tbl(df_aco_oppo_dtl,'overuse_reduction')
                                                                ],
                                                                style={"padding-bottom":"2.5rem"}
                                                            )
                                                        ]
                                                    )
                                                ),
                                            ],
                                            style={"padding-left":"2rem", "padding-right":"2rem"}
                                        )
                                        
                                    ]
                                ),
                                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
                            ),
                            
                        ],style={"padding":"2rem"}
                    ),
                    html.Div(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                                dbc.Col(html.H4("Readmission Reduction", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                            ],
                                            no_gutters=True,
                                            style={"padding-bottom":"2rem"}
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Div(
                                                        [
                                                            html.Div(html.H6('Top 5 Diseases with the Biggest Estimated Cost Reduction Opportunities through Readmission Reduction(PMPM)', style={"font-weight":"bold"}), style={"text-align":"center", "padding-bottom":"1rem"}),
                                                            html.Div(
                                                                [
                                                                    dcc.Graph(figure=aco_oppo_bar(df_aco_oppo_dtl,'readmission_reduction'), config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},)
                                                                ],
                                                                style={"padding-bottom":"2.5rem"}
                                                            ),
                                                            html.H6('* Patient mix adjusted')
                                                        ]
                                                    ),
                                                    width=5
                                                ),
                                                dbc.Col(html.Div(),width=1),
                                                dbc.Col(
                                                    html.Div(
                                                        [
                                                            html.Div(html.H6('90-day Post Discharge Readmission Rate Comparison', style={"font-weight":"bold"}), style={"text-align":"center", "padding-bottom":"3rem"}),
                                                            html.Div(
                                                                [
                                                                    aco_oppo_tbl(df_aco_oppo_dtl,'readmission_reduction')
                                                                ],
                                                                style={"padding-bottom":"2.5rem"}
                                                            )
                                                        ]
                                                    )
                                                ),
                                            ],
                                            style={"padding-left":"2rem", "padding-right":"2rem"}
                                        )
                                        
                                    ]
                                ),
                                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
                            ),
                            
                        ],style={"padding":"2rem"}
                    ),
                    # html.Div(
                    #     [
                    #         dbc.Card(
                    #             dbc.CardBody(
                    #                 [
                    #                     dbc.Row(
                    #                         [
                    #                             dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                    #                             dbc.Col(html.H4("Referral Steerage", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                    #                         ],
                    #                         no_gutters=True,
                    #                         style={"padding-bottom":"2rem"}
                    #                     ),
                    #                     dbc.Row(
                    #                         [
                    #                             dbc.Col(
                    #                                 html.Div(
                    #                                     [
                    #                                         html.Div(html.H6('Estimated Cost Reduction Opportunities by Service Type(PMPM)', style={"font-weight":"bold"}), style={"text-align":"center", "padding-bottom":"1rem"}),
                    #                                         html.Div(
                    #                                             [
                    #                                                 dcc.Graph(figure=aco_oppo_bar(df_aco_oppo_dtl,'referral_steerage'), config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},)
                    #                                             ],
                    #                                             style={"padding-bottom":"2.5rem"}
                    #                                         ),
                    #                                         html.H6('* Service mix adjusted')
                    #                                     ]
                    #                                 ),
                    #                                 width=5
                    #                             ),
                    #                             dbc.Col(html.Div(),width=1),
                    #                             dbc.Col(
                    #                                 html.Div(
                    #                                     [
                    #                                         html.Div(html.H6('Utilization Rate and Unit Cost Comparison', style={"font-weight":"bold"}), style={"text-align":"center", "padding-bottom":"3rem"}),
                    #                                         html.Div(
                    #                                             [
                    #                                                 aco_oppo_tbl(df_aco_oppo_dtl,'referral_steerage')
                    #                                             ],
                    #                                             style={"padding-bottom":"2.5rem"}
                    #                                         )
                    #                                     ]
                    #                                 )
                    #                             ),
                    #                         ],
                    #                         style={"padding-left":"2rem", "padding-right":"2rem"}
                    #                     )
                                        
                    #                 ]
                    #             ),
                    #             style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
                    #         ),
                            
                    #     ],style={"padding":"2rem"}
                    # ),
                    html.Div(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                                dbc.Col(html.H4("Service Optimization", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                            ],
                                            no_gutters=True,
                                            style={"padding-bottom":"2rem"}
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Div(
                                                        [
                                                            html.Div(html.H6('Estimated Cost Reduction Opportunities by Service Type(PMPM)', style={"font-weight":"bold"}), style={"text-align":"center", "padding-bottom":"1rem"}),
                                                            html.Div(
                                                                [
                                                                    dcc.Graph(figure=aco_oppo_bar(df_aco_oppo_dtl,'service_optimize'), config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},)
                                                                ],
                                                                style={"padding-bottom":"2.5rem"}
                                                            ),
                                                            html.H6('* Service mix adjusted')
                                                        ]
                                                    ),
                                                    width=5
                                                ),
                                                dbc.Col(html.Div(),width=1),
                                                dbc.Col(
                                                    html.Div(
                                                        [
                                                            html.Div(html.H6('Service Rate Comparison', style={"font-weight":"bold"}), style={"text-align":"center", "padding-bottom":"3rem"}),
                                                            html.Div(
                                                                [
                                                                    aco_oppo_tbl(df_aco_oppo_dtl,'service_optimize')
                                                                ],
                                                                style={"padding-bottom":"2.5rem"}
                                                            )
                                                        ]
                                                    )
                                                ),
                                            ],
                                            style={"padding-left":"2rem", "padding-right":"2rem"}
                                        )
                                        
                                    ]
                                ),
                                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
                            ),
                            
                        ],style={"padding":"2rem"}
                    ),
                    html.Div(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                                dbc.Col(html.H4("Post Acute Care Optimization", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                            ],
                                            no_gutters=True,
                                            style={"padding-bottom":"2rem"}
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Div(
                                                        [
                                                            html.Div(html.H6('Top 5 Diseases with the Biggest Estimated Cost Reduction Opportunities through Post Acute Care Optimization(PMPM)', style={"font-weight":"bold"}), style={"text-align":"center", "padding-bottom":"1rem"}),
                                                            html.Div(
                                                                [
                                                                    dcc.Graph(figure=aco_oppo_bar(df_aco_oppo_dtl,'pac_optimize'), config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},)
                                                                ],
                                                                style={"padding-bottom":"2.5rem"}
                                                            ),
                                                            html.H6('* Patient mix adjusted')
                                                        ]
                                                    ),
                                                    width=5
                                                ),
                                                dbc.Col(html.Div(),width=1),
                                                dbc.Col(
                                                    html.Div(
                                                        [
                                                            html.Div(html.H6('% of Admissions Discharged to Institutional PAC Facilities (SNF and Inpatient Rehab)', style={"font-weight":"bold"}), style={"text-align":"center", "padding-bottom":"3rem"}),
                                                            html.Div(
                                                                [
                                                                    aco_oppo_tbl(df_aco_oppo_dtl,'pac_optimize')
                                                                ],
                                                                style={"padding-bottom":"2.5rem"}
                                                            )
                                                        ]
                                                    )
                                                ),
                                            ],
                                            style={"padding-left":"2rem", "padding-right":"2rem"}
                                        )
                                        
                                    ]
                                ),
                                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
                            ),
                            
                        ],style={"padding":"2rem"}
                    ),

                ]
            )

def tab_bundle(app):
    return html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.H2("Summary of Bundled Payment Cost Reduction Opportunities", style={"padding-left":"2rem","font-size":"3"}), width=8),
                        ],
                        style={"padding-top":"2rem"}
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                                dbc.Col(html.H4("Bundle Opportunity Overview", style={"font-size":"1rem", "margin-left":"10px"})),
                                            ],
                                            no_gutters=True,
                                        ),
                                        dcc.Graph(figure=bubble_bundle(df_bundle_oppo), id='oppo-figure-bundleoppo',config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,}, clickData={'points': [{'customdata': 'Congestive heart failure'}]},selectedData={'points': [{'customdata': 'Congestive heart failure'}]},)
                                    ]
                                )
                            , width=6),
                            dbc.Col(html.Div(), width=1),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                                    dbc.Col(html.H4("Top 10 Bundles with the Biggest Potential Cost Reduction Opportunities", style={"font-size":"1rem", "margin-left":"10px"})),
                                                ],
                                                no_gutters=True,
                                            ),
                                            html.Div(
                                                [
                                                    dcc.Graph(figure=bundle_vertical(df_bundle_oppo),config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,}, ),
                                                    html.Div(
                                                        [
                                                            dbc.Button("View all bundles", className="mb-3", style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.7rem", "width":"10rem","margin-left":"4rem"}, id="open-vab-modal"),
                                                            dbc.Modal(
                                                                [
                                                                    dbc.ModalHeader("Bundle Details"),
                                                                    dbc.ModalBody(
                                                                        html.Div([bundle_oppo_tbl(df_bundle_oppo)], style={"padding-left":"2rem", "padding-right":"2rem", "padding-bottom":"4rem"})
                                                                    ),
                                                                    dbc.ModalFooter(
                                                                        dbc.Button(
                                                                            "Close", id="close-vab-modal", className="ml-auto"
                                                                        )
                                                                    ),
                                                                ],
                                                                id="vab-modal",
                                                                size="xl",
                                                                scrollable=True
                                                            )
                                                        ]
                                                    )

                                                ],
                                                style={"padding-right":"1rem"}
                                            )
                                        ]
                                    ),
                                    style={"background-color":"#d4e6ff", "border":"none", "border-radius":"0.5rem"}
                                )
                                , width=5),
                        ],
                        style={"padding":"4rem", "padding-left":"4rem", "padding-right":"4rem"}
                    ),
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.H2(id='oppo-text-bundlename', style={"background-color":"#38160f", "border":"none", "border-radius":"0.5rem", "color":"#fff","padding-left":"2rem","padding-right":"2rem"}), width="auto"
                                    ),
                                    dbc.Col(
                                        html.H3("Details", style={"padding-top":"0.3rem"})
                                    ),
                                ]
                            )
                        ],style={"padding-left":"2rem","padding-top":"4rem"}
                    ),
                    html.Hr(),
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                                            dbc.Col(html.H4("Historical Bundle Volume Change", style={"font-size":"1rem", "margin-left":"10px"})),
                                                        ],
                                                        no_gutters=True,
                                                        style={"padding-bottom":"2rem"}
                                                    ),
                                                    html.Div(
                                                        [
                                                            dcc.Graph(figure=bundle_trend(df_bundle_trend[df_bundle_trend['bundle']=='Congestive heart failure']), id='oppo-figure-bundletrend', config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},)
                                                        ]
                                                    )
                                                ]
                                            ),
                                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
                                        ),
                                        width=6
                                    ),
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                                            dbc.Col(html.H4("Average Bundle Cost Benchmarking (2020)", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                                        ],
                                                        no_gutters=True,
                                                        style={"padding-bottom":"2rem"}
                                                    ),
                                                    html.Div(
                                                        [
                                                            dcc.Graph(figure=bundle_avgcost(df_bundle_oppo[df_bundle_oppo['bundle']=='Congestive heart failure']), id='oppo-figure-bundlebench', config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},)
                                                        ],
                                                        style={"padding-bottom":"2.5rem"}
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.H6(id='oppo-text-bundle-comparebench',style={"padding-top":"0.5rem"}),
                                                            html.H6(id='oppo-text-bundle-comparebest',style={"padding-bottom":"0.5rem"})
                                                        ],
                                                        style={"background-color":"#FFE2AA", "border":"none", "border-radius":"0.5rem","padding-left":"1rem"}
                                                    )
                                                ]
                                            ),
                                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
                                        ),
                                        width=6
                                    ),
                                ]
                            )
                            
                        ],style={"padding":"2rem"}
                    ),
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                                            dbc.Col(html.H4("Average Bundle Cost Difference by Service Category", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                                        ],
                                                        no_gutters=True,
                                                        style={"padding-bottom":"2rem"}
                                                    ),
                                                    html.Div(
                                                        [
                                                            dcc.Graph(figure=bundle_svccost(df_bundle_costbysvc[df_bundle_costbysvc['bundle']=='Congestive heart failure']), id='oppo-figure-bundlesvc', config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},)
                                                        ]
                                                    )
                                                ]
                                            ),
                                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
                                        ),
                                        width=6
                                    ),
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                                            dbc.Col(html.H4("Potential Cost Reduction Opportunities (reduction in average bundle cost)", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                                        ],
                                                        no_gutters=True,
                                                        style={"padding-bottom":"2rem"}
                                                    ),
                                                    html.Div(
                                                        [
                                                            dcc.Graph(figure=bundle_vertical(df_bundle_costbyoppo[df_bundle_costbyoppo['bundle']=='Congestive heart failure'], 'pct'), id='oppo-figure-costbyoppo', config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},)
                                                        ],
                                                        style={"padding-bottom":"2.5rem"}
                                                    )
                                                ]
                                            ),
                                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
                                        ),
                                        width=6
                                    ),
                                ]
                            )
                            
                        ],style={"padding":"2rem"}
                    ),
                    bundle_full_details(app)
                ]
            )


def bundle_full_details(app):
    return html.Div(
            [
                dbc.Button("View more details", 
                    className="mb-3", 
                    style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.7rem", "width":"10rem","margin-left":"4rem"}, 
                    id="show-bundle-vmd"),
                html.Div(
                    [
                        html.Div(
                            [
                                bundle_oppo_dtl_bydim(df_bundle_bydrg[df_bundle_bydrg['bundle']=='Congestive heart failure']), 
                            ],
                            id='oppo-table-bydrg',
                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem","padding":"2rem"}
                        ),
                        html.Div(
                            [
                                bundle_oppo_dtl_bydim(df_bundle_byphy[df_bundle_byphy['bundle']=='Congestive heart failure']), 
                            ],
                            id='oppo-table-byphy',
                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem","padding":"2rem"}
                        ),
                        html.Div(
                            [
                                bundle_oppo_dtl_bench(df_bundle_byreadmitdrg[df_bundle_byreadmitdrg['bundle']=='Congestive heart failure'], 'Readmission Rate Comparison'), 
                            ],
                            id= 'oppo-table-byreadm',
                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem","padding":"2rem"}
                        ),
                        html.Div(
                            [
                                bundle_oppo_dtl_bench(df_bundle_byer[df_bundle_byer['bundle']=='Congestive heart failure'], 'Readmission Rate Comparison'), 
                            ],
                            id='oppo-table-byer',
                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem","padding":"2rem"}
                        ),
                        html.Div(
                            [
                                bundle_oppo_dtl_bench(df_bundle_pac_rate[df_bundle_pac_rate['bundle']=='Congestive heart failure'], 'Discharge Rate Comparison'), 
                            ],
                            id='oppo-table-pacrate',
                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem","padding":"2rem"}
                        ),
                        html.Div(
                            [
                                bundle_oppo_dtl_bench(df_bundle_pac_los[df_bundle_pac_los['bundle']=='Congestive heart failure'], 'LOS Comparison'), 
                            ],
                            id='oppo-table-paclos',
                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem","padding":"2rem"}
                        ),
                        html.Div(
                            [
                                bundle_oppo_dtl_bench(df_bundle_dme[df_bundle_dme['bundle']=='Congestive heart failure'], 'Average Cost/Bundle'), 
                            ],
                            id='oppo-table-bydme',
                            style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem","padding":"2rem"}
                        ),
                    ],
                    hidden=True,
                    style={"padding":"2rem"},
                    id="bundle-vmd"
                )
                
            ]
        )

layout = create_layout(app)




# aco
@app.callback(
    [
        Output("cost-reduction-pmpm", "hidden"),
        Output("cost-reduction-pct", "hidden"),
        Output("cost-reduction-unit", "children"),
    ],
    [
        Input("switch-cost-reduction-pmpm", "n_clicks"), 
        Input("switch-cost-reduction-pct", "n_clicks")
    ],
    [
        State("cost-reduction-pmpm", "hidden"),
        State("cost-reduction-pct", "hidden"),
    ],
)
def toggle_figure_cost_reduction(n1, n2, is_hidden1, is_hidden2):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = 'No clicks yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "switch-cost-reduction-pct":
        return True, False, "(%)"
    else:
        return False, True, "(PMPM)"



@app.callback(
    [Output('oppo-filter-acolv2','options'),
    Output('oppo-filter-acolv2','value'),],
    [Input('oppo-filter-acolv1','value')]
    )
def update_filter(oppo_lv1):

    subcate_list = aco_oppo_drill_mapping[aco_oppo_drill_mapping['oppo']==oppo_lv1]['category'].tolist()
    option_lv2 = [ {'label': c, 'value': c} for c in subcate_list]
    value_lv2 = subcate_list[0]

    return option_lv2, value_lv2

@app.callback(
    [Output('oppo-text-drilltable_desc','children'),
    Output('oppo-table-acodrill','data'),
    Output('oppo-table-acodrill','columns'),],
    [Input('oppo-filter-acolv1','value'),
    Input('oppo-filter-acolv2','value'),]
    )
def update_table(oppo_lv1, oppo_lv2):
    tabel_desc = oppo_lv2+' Comparison Details '+ ('' if oppo_lv1=='pat_manage' else '(units per 1,000 member)' if oppo_lv1=='overuse_reduction' else '')

    df_table = df_aco_oppo_drill[(df_aco_oppo_drill['oppo']==oppo_lv1) & (df_aco_oppo_drill['category']==oppo_lv2)]
    fstcol_name = aco_oppo_drill_mapping[(aco_oppo_drill_mapping['oppo']==oppo_lv1) & (aco_oppo_drill_mapping['category']==oppo_lv2)]['drill_dim'].values[0]

    format_money = FormatTemplate.money(1)
    format_pct = FormatTemplate.percentage(1)
    format_num = Format( precision=0,group=',', scheme=Scheme.fixed,)

    if oppo_lv1 == 'referral_steerage':
        col = [['',fstcol_name], ['Preferred Provider','% of Total Units'], ['Preferred Provider','Avg Cost/Unit'], 
        ['Non-Preferred Provider','% of Total Units'], ['Non-Preferred Provider','Avg Cost/Unit'],['','Cost Reduction if Steering All Visits to Preferred Provider(PMPM)']]
        table_col = [{'name':col[k], 'id':df_table.columns[k], 'type':'numeric', 'format':format_money} if k in[2,4,5] \
        else {'name':col[k], 'id':df_table.columns[k], 'type':'numeric', 'format':format_pct}for k in range(6)]
    # elif oppo_lv1 in ['pat_manage']:
    #     table_col = [{'name':fstcol_name, 'id':df_table.columns[k]} if k==0 \
    #     else {'name':df_table.columns[k], 'id':df_table.columns[k], 'type':'numeric', 'format':format_money} for k in range(6)]
    elif oppo_lv1 in ['overuse_reduction','pat_manage']:
        table_col = [{'name':fstcol_name, 'id':df_table.columns[k]} if k==0 \
        else {'name':df_table.columns[k], 'id':df_table.columns[k], 'type':'numeric', 'format':format_num} if k in [1,2,4] \
        else {'name':df_table.columns[k], 'id':df_table.columns[k], 'type':'numeric', 'format':format_money} for k in range(6)]
    else:
        table_col = [{'name':fstcol_name, 'id':df_table.columns[k]} if k==0 \
        else {'name':df_table.columns[k], 'id':df_table.columns[k], 'type':'numeric', 'format':format_pct} if k in [1,2,4] \
        else {'name':df_table.columns[k], 'id':df_table.columns[k], 'type':'numeric', 'format':format_money} for k in range(6)]

    return  tabel_desc, df_table.to_dict('records'), table_col

@app.callback(
    Output("aco-drilldown-modal", "is_open"),
    [Input("open-aco-drilldown-modal", "n_clicks"), Input("close-aco-drilldown-modal", "n_clicks")],
    [State("aco-drilldown-modal", "is_open")],
)
def toggle_modal_aco_drilldown(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# bundle

@app.callback(
    [Output('oppo-text-bundlename', 'children'),
    Output('oppo-figure-bundletrend', 'figure'),
    Output('oppo-figure-bundlebench', 'figure'),
    Output('oppo-text-bundle-comparebench', 'children'),
    Output('oppo-text-bundle-comparebest', 'children'),
    Output('oppo-figure-bundlesvc', 'figure'),
    Output('oppo-figure-costbyoppo', 'figure'),
    Output('oppo-table-bydrg', 'children'),
    Output('oppo-table-byphy', 'children'),
    Output('oppo-table-byreadm', 'children'),
    Output('oppo-table-byer', 'children'),
    Output('oppo-table-pacrate', 'children'),
    Output('oppo-table-paclos', 'children'),
    Output('oppo-table-bydme', 'children'),
    ], 
    [Input('oppo-figure-bundleoppo', 'clickData')])
def update_y_timeseries(clickData):
    bundle = clickData['points'][0]['customdata']
    df_trend = df_bundle_trend[df_bundle_trend['bundle']==bundle]
    df_avgcost = df_bundle_oppo[df_bundle_oppo['bundle']==bundle]
    df_byoppo = df_bundle_costbyoppo[df_bundle_costbyoppo['bundle']==bundle]
    df_bysvc = df_bundle_costbysvc[df_bundle_costbysvc['bundle']==bundle]

    avgcost_compare_bench = df_avgcost['provider'].values[0] - df_avgcost['benchmark'].values[0]
    avgcost_compare_benchpct = avgcost_compare_bench/df_avgcost['benchmark'].values[0]
    avgcost_compare_benchsign = 'higher' if avgcost_compare_bench>=0 else 'lower'
    avgcost_compare_benchtext = 'Provider group bundle cost is {}% {}(${} {}) than Benchmark'.format(round(abs(avgcost_compare_benchpct*100),1),avgcost_compare_benchsign,abs(int(round(avgcost_compare_bench,0))),avgcost_compare_benchsign)

    avgcost_compare_best = df_avgcost['provider'].values[0] - df_avgcost['best_in_class'].values[0]
    avgcost_compare_bestpct = avgcost_compare_best/df_avgcost['best_in_class'].values[0]
    avgcost_compare_bestsign = 'higher' if avgcost_compare_best>=0 else 'lower'
    avgcost_compare_besttext = 'Provider group bundle cost is {}% {}(${} {}) than Best-in-Class'.format(round(abs(avgcost_compare_bestpct*100),1),avgcost_compare_bestsign,abs(int(round(avgcost_compare_best,0))),avgcost_compare_bestsign)

    df_bydrg = bundle_oppo_dtl_bydim(df_bundle_bydrg[df_bundle_bydrg['bundle']==bundle])
    df_byphy = bundle_oppo_dtl_bydim(df_bundle_byphy[df_bundle_byphy['bundle']==bundle])
    df_byreadmitdrg = bundle_oppo_dtl_bench(df_bundle_byreadmitdrg[df_bundle_byreadmitdrg['bundle']==bundle], 'Readmission Rate Comparison')
    df_byer = bundle_oppo_dtl_bench(df_bundle_byer[df_bundle_byer['bundle']==bundle], 'Readmission Rate Comparison')
    df_pacrate = bundle_oppo_dtl_bench(df_bundle_pac_rate[df_bundle_pac_rate['bundle']==bundle], 'Discharge Rate Comparison')
    df_paclos = bundle_oppo_dtl_bench(df_bundle_pac_los[df_bundle_pac_rate['bundle']==bundle], 'LOS Comparison')
    df_dme = bundle_oppo_dtl_bench(df_bundle_dme[df_bundle_dme['bundle']==bundle], 'Average Cost/Bundle')

    return bundle,bundle_trend(df_trend), bundle_avgcost(df_avgcost), avgcost_compare_benchtext, avgcost_compare_besttext, bundle_svccost(df_bysvc), bundle_vertical(df_byoppo, 'pct'), df_bydrg, df_byphy, df_byreadmitdrg, df_byer, df_pacrate, df_paclos, df_dme


@app.callback(
    Output("vab-modal", "is_open"),
    [Input("open-vab-modal", "n_clicks"), Input("close-vab-modal", "n_clicks")],
    [State("vab-modal", "is_open")],
)
def toggle_modal_view_all_bundles(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("bundle-vmd", "hidden"),
    [Input("show-bundle-vmd", "n_clicks")],
    [State("bundle-vmd", "hidden")],
)
def toggle_bundle_vmd(n1, hidden):
    if n1 :
        return not hidden
    return hidden


if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True,port=8050)


