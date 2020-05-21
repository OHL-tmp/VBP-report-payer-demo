#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 14:10:52 2020
@author: yanen
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_table

import pandas as pd
import numpy as np
import json

import pathlib
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
from utils import *
from figure import *
from modal_dashboard_domain_selection import *

from app import app


#app = dash.Dash(__name__, url_base_pathname='/vbc-payer-demo/contract-bundle-manager/')

#server = app.server



## load data
df_overall_bundle=pd.read_csv("data/df_overall_bundle.csv")
df_target_adj_bundle=pd.read_csv("data/df_target_adj_bundle.csv")
df_result_details_bundle=pd.read_csv("data/df_result_details_bundle.csv")

df_bundle_performance=pd.read_csv("data/df_bundle_performance.csv")
df_bundle_performance_pmpm=pd.read_csv("data/df_bundle_performance_pmpm.csv")
df_bundle_performance_details=pd.read_csv("data/df_bundle_performance_details.csv")
df_bundle_performance_details_pmpm=pd.read_csv("data/df_bundle_perf_details_pmpm.csv")
df_measure_score_bundle=pd.read_csv("data/df_measure_score_bundle.csv")

df_network_cost_split_bundle=pd.read_csv('data/df_network_cost_split_bundle.csv')

#modebar display
button_to_rm=['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'hoverClosestCartesian','hoverCompareCartesian','hoverClosestGl2d', 'hoverClosestPie', 'toggleHover','toggleSpikelines']


#file = open('configure/input_ds.json', encoding = 'utf-8')
#custom_input = json.load(file)
#twoside = custom_input['savings/losses sharing arrangement']["two side"]


def create_layout(app):

    return html.Div(
                [ 
                    html.Div([Header_mgmt_bp(app, True, False, False, False)], style={"height":"6rem"}, className = "sticky-top navbar-expand-lg"),
                    
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(manager_div_year_to_date_metrics(app), width=3),
                                    dbc.Col(manager_div_overall_performance(app)),
                                ]
                            ),
                        ],
                        className="mb-3",
                        style={"padding-left":"3rem", "padding-right":"3rem","padding-top":"1rem","padding-bottom":"0rem"},
                    ),
                    
                    
                    html.Div(
                        [
                            manager_card_quality_score(app),
                        ],
                        className="mb-3",
                        style={"padding-top":"1rem", "padding-left":"3rem", "padding-right":"3rem"},
                    ),


                ],
                style={"background-color":"#f5f5f5"},
            )

def manager_div_year_to_date_metrics(app):
    return html.Div(
                [
                    html.H2("Key Performance Metrics", style={"padding-top":"2rem", "font-weight":"lighter", "font-size":"1rem"}),
                    manager_card_year_to_date_metrics("Attributed Members", "4,250", "#381610f"),
                    manager_card_year_to_date_metrics("YTD Total Cost", "$24.6M", "#381610f"),
                    manager_card_year_to_date_metrics("Projected Total Cost", "$54.1M", "#381610f"),
                    html.Hr(className="ml-1"),
                    manager_card_year_to_date_metrics("Projected Total Losses", "\u25bc $1.6M", "#db2200"),
                    manager_card_year_to_date_metrics("Projected Plan's Shared Losses", "\u25bc $1.1M", "#db2200"),
                    html.Hr(className="ml-1"),
                    manager_modal_metricsdetail(app),
                ],
                className="mb-3",
                style={"text-align":"center"},
            )

def manager_modal_metricsdetail(app):
    return html.Div([
            dbc.Button(
                        "Result Details",
                        id = 'bundle-manager-button-openmodal-metricsdetail',
                        className="mb-3",
                        style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"},
                    ),
            dbc.Modal([
                dbc.ModalHeader(
                    [
                        html.H1("Result Details", style={"font-size":"0.8rem"}),
                    ],
                    
                ),
                dbc.ModalBody(children=table_result_dtls(df_result_details_bundle), style={"padding":"2rem"}),
                dbc.ModalFooter(dbc.Button('Close', style={"border-radius":"10rem"}, id = 'bundle-manager-button-closemodal-metricsdetail')),
                ], id = 'bundle-manager-modal-metricsdetail'),

        ])

def manager_card_year_to_date_metrics(title, value, color):
    return dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H3(title, style={"height":"0.8rem", "font-size":"0.8rem"}),
                            html.H2(value, style={"height":"1.6rem", "color":color}),
                        ],
                        style={"padding-top":"0.8rem", "padding-bottom":"0.8rem"},
                    )
                ],
                className="mb-3",
                style={"background-color":"#dfdfdf", "border":"none", "border-radius":"0.5rem"}
            )

def manager_div_overall_performance(app):

    return html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.H1("OVERALL PERFORMANCE"), width="auto"),
                            dbc.Col(
                                html.Div(
                                    html.H5("05/18/2020", style={"font-size":"0.8rem","color":"#fff","background-color":"#1357DD", "text-align":"center","border-radius":"10rem"}),
                                ),
                                width=2,
                                style={"padding-top":"2rem"}
                            ),
                        ]
                    ),
                    
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(dcc.Graph(figure=waterfall_overall_bundle(df_overall_bundle), config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},style={"width":"100%","height":"100%"}), style={"height":"28rem"}),
                                    manager_modal_totalcost(app),
                                ]
                            )
                        ],
                    ),
                ],
                style={"padding-top":"1rem","padding-bottom":"0rem", "padding-right":"2rem", "max-height":"50rem"},
            )



def manager_card_quality_score(app):

    return html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                                    dbc.Col(html.H4("Performance of Each Bundle", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                                    ],
                                                no_gutters=True,
                                            ),
                                            
                                            html.Div(
                                                dbc.Tabs(
                                                    [
                                                        dbc.Tab(
                                                            html.Div( children=table_perform_bundle(df_bundle_performance)

                                                            ), 
                                                            label="Total Cost", style={"background-color":"#fff","height":"16rem","padding":"1rem"}, tab_style={"font-family":"NotoSans-Condensed"}
                                                        ),
                                                        dbc.Tab(
                                                            html.Div( children=table_perform_bundle(df_bundle_performance_pmpm)

                                                            ), 
                                                            label="PMPM", style={"background-color":"#fff","height":"16rem","padding":"1rem"}, tab_style={"font-family":"NotoSans-Condensed"}
                                                        ),
                                                        
                                                    ], 
                                                )
                                            ),

                                            manager_modal_bundle_performance_details(app),
                                            
                                        ]
                                    ),
                                    style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem","height":"24rem"}
                                ),

                                
                            ],
                            width=8,
                        ),

                        

                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                                dbc.Col(html.H4("Bundle Cost In VS. Out of PGP", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                                ],
                                            no_gutters=True,
                                        ),
                                        
                                        html.Div(children=dcc.Graph(figure=pie_cost_split(df_network_cost_split_bundle),config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,}, style={"height":"19.8rem"})
                                            
                                        )
                                        
                                    ]
                                ),
                                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
                            ),
                            width=4,
                        )
                    ]
                ),
                html.Div(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                        dbc.Col(html.H4("Quality Measures", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                        ],
                                    no_gutters=True,
                                ),
                                
                                html.Div(children=dcc.Graph(figure=measure_quality_bar_bundle(df_measure_score_bundle),config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,}, style={"padding":"1rem"})
                                    
                                )
                                
                            ]
                        ),
                        style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem","padding":"1rem"}
                    ),
                    style={"padding-top":"1rem"}
                ),
                
            ]
        )
        

            
def manager_modal_totalcost(app):
    return html.Div([
                dbc.Button(
                    "Details",
                    id = 'bundle-manager-button-openmodal-totalcost',
                    className="mb-3",
                    style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"},
                ),
                dbc.Modal([
                    dbc.ModalHeader(
                        [
                            html.H1("Target Adjustment Details", style={"font-size":"0.8rem"}),
                            html.H2("TOTAL COST", style={"font-size":"1.6rem","color":"#1357DD","background-color":"#c6d9ff","padding":"0.5rem","border-radius":"0.5rem"})
                        ],
                        
                    ),
                    dbc.ModalBody(dcc.Graph(figure=waterfall_target_adj(df_target_adj_bundle),config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,}, style={"padding":"2rem"})),
                    dbc.ModalFooter(dbc.Button('Close',style={"border-radius":"10rem"}, id = 'bundle-manager-button-closemodal-totalcost')),
                    ], id = 'bundle-manager-modal-totalcost',
                style={"text-align":"center"}),
            ],
            style={"text-align":"end","padding-right":"9rem"})


def manager_modal_bundle_performance_details(app):
    return html.Div([
            dbc.Button(
                        "Result Details",
                        id = 'bundle-manager-button-openmodal-bundle-performance-details',
                        className="mb-3",
                        style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"},
                    ),
            dbc.Modal([
                dbc.ModalHeader(
                    [
                        html.H1("Result Details", style={"font-size":"0.8rem"}),
                        html.H2("TOTAL COST", style={"font-size":"1.6rem","color":"#1357DD","background-color":"#c6d9ff","padding":"0.5rem","border-radius":"0.5rem"})
                    ],
                    
                ),
                dbc.ModalBody([
                    html.Div('Bundle Total'),
                    table_bundle_dtls(df_bundle_performance_details),
                    html.Div('Bundle Average'),
                    table_bundle_dtls(df_bundle_performance_details_pmpm),
                    ], style={"padding":"2rem"}),
                dbc.ModalFooter(dbc.Button('Close', style={"border-radius":"10rem"}, id = 'bundle-manager-button-closemodal-bundle-performance-details')),
                ], id = 'bundle-manager-modal-bundle-performance-details'),

        ])


layout = create_layout(app)


@app.callback(
    Output('bundle-manager-modal-metricsdetail', 'is_open'),
    [Input('bundle-manager-button-openmodal-metricsdetail', 'n_clicks'),
    Input('bundle-manager-button-closemodal-metricsdetail', 'n_clicks')],
    [State('bundle-manager-modal-metricsdetail', 'is_open')]
    )
def open_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output('bundle-manager-modal-totalcost', 'is_open'),
    [Input('bundle-manager-button-openmodal-totalcost', 'n_clicks'),
    Input('bundle-manager-button-closemodal-totalcost', 'n_clicks')],
    [State('bundle-manager-modal-totalcost', 'is_open')]
    )
def open_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output('bundle-manager-modal-bundle-performance-details', 'is_open'),
    [Input('bundle-manager-button-openmodal-bundle-performance-details', 'n_clicks'),
    Input('bundle-manager-button-closemodal-bundle-performance-details', 'n_clicks')],
    [State('bundle-manager-modal-bundle-performance-details', 'is_open')]
    )
def open_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open



if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True, port = 8052)
