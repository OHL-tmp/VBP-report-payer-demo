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

import pathlib
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
from utils import *
from figure import *
from modal_dashboard_domain_selection import *


app = dash.Dash(__name__, url_base_pathname='/vbc-payer-demo/contract-manager/')

server = app.server



## load data


def create_layout(app):

    return html.Div(
                [ 
                    html.Div([Header_mgmt(app, True, False, False, False)], style={"height":"6rem"}, className = "sticky-top navbar-expand-lg"),
                    
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
                        style={"padding-left":"3rem", "padding-right":"3rem","padding-top":"1rem"},
                    ),
                    
                    html.Div(
                        [
                            manager_card_attributed_members(app),
                        ],
                        className="mb-3",
                        style={"padding-top":"1rem", "padding-left":"3rem", "padding-right":"3rem"},
                    ),

                    html.Div(
                        [
                            manager_card_quality_score(app),
                        ],
                        className="mb-3",
                        style={"padding-top":"1rem", "padding-left":"3rem", "padding-right":"3rem"},
                    )
                ],
                style={"background-color":"#f5f5f5"},
            )

def manager_div_year_to_date_metrics(app):
    return html.Div(
                [
                    html.H2("Key Performance Metrics", style={"padding-top":"2rem", "font-weight":"lighter", "font-size":"1rem"}),
                    manager_card_year_to_date_metrics("Attributed Members", "1,000", "#381610f"),
                    manager_card_year_to_date_metrics("YTD Total Cost", "$100M", "#381610f"),
                    manager_card_year_to_date_metrics("Projected Total Cost", "$230M", "#381610f"),
                    html.Hr(className="ml-1"),
                    manager_card_year_to_date_metrics("Projected Total Savings/Losses", "$15M", "#db2200"),
                    manager_card_year_to_date_metrics("Projected Plan's Shared Savings/Losses", "$7.5M", "#db2200"),
                    manager_card_year_to_date_metrics("Projected ACO's Shared Savings/Losses", "$7.5M", "#db2200"),
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
                        id = 'manager-button-openmodal-metricsdetail',
                        className="mb-3",
                        style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"},
                    ),
            dbc.Modal([
                dbc.ModalHeader("Header"),
                dbc.ModalBody("Modal body content"),
                dbc.ModalFooter(dbc.Button('Close', id = 'manager-button-closemodal-metricsdetail')),
                ], id = 'manager-modal-metricsdetail'),

        ])

def manager_card_year_to_date_metrics(title, value, color):
    return dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H3(title, style={"height":"1rem", "font-size":"1rem"}),
                            html.H2(value, style={"height":"2rem", "color":color}),
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
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H2("As of June 30th.", style={"font-size":"1.5rem", "margin-top":"-5px", "color":"#fff"}),
                                    ],
                                    style={"margin-top":"-16px"}
                                ),
                                style={"height":"3rem", "background-color":"#1357DD", "text-align":"center"},
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col("Total Cost", style={"text-align":"end"}, width=5),
                            dbc.Col(
                                daq.ToggleSwitch(
                                    value=False,
                                    id = 'manager-switch-totalcost-pmpm',
                                ), 
                                width=2
                            ),
                            dbc.Col("PMPM", width=5),
                        ]
                    ),
                    html.Div([dbc.Row(
                        [
                            dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"width":"100%","height":"100%"}), width=7),
                            dbc.Col(
                                html.Div(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"), style={"width":"100%","height":"100%"}),
                                        manager_modal_totalcost(app),
                                    ]
                                ),
                                width=5
                            ),
                        ], 
                    ),
                    ], id = 'manager-div-totalcost-container', hidden = False),
                    html.Div([dbc.Row(
                        [
                            dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"width":"100%","height":"100%"}), width=7),
                            dbc.Col(
                                html.Div(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"), style={"width":"100%","height":"100%"}),
                                        manager_modal_pmpm(app),
                                    ]
                                ),
                                width=5
                            ),
                        ], 
                    ),
                    ], id = 'manager-div-pmpm-container', hidden = True),
                    manager_card_key_driver(app)
                ],
                style={"padding-bottom":"30rem", "padding-right":"2rem", "max-height":"5rem"},
            )

def manager_modal_totalcost(app):
    return html.Div([
                dbc.Button(
                    "Target Adjustment Details",
                    id = 'manager-button-openmodal-totalcost',
                    className="mb-3",
                    style={"background-color":"#38160f", "border":"none", "border-radius":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem","height":"4rem","width":"80%"},
                ),
                dbc.Modal([
                    dbc.ModalHeader("Header"),
                    dbc.ModalBody("Modal body content"),
                    dbc.ModalFooter(dbc.Button('Close', id = 'manager-button-closemodal-totalcost')),
                    ], id = 'manager-modal-totalcost',
                style={"text-align":"center"}),
            ])

def manager_modal_pmpm(app):
    return html.Div([
                dbc.Button(
                    "Target Adjustment Details",
                    id = 'manager-button-openmodal-pmpm',
                    className="mb-3",
                    style={"background-color":"#38160f", "border":"none", "border-radius":"0.5rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem","height":"4rem","width":"80%"},
                ),
                dbc.Modal([
                    dbc.ModalHeader("Header"),
                    dbc.ModalBody("Modal body content"),
                    dbc.ModalFooter(dbc.Button('Close', id = 'manager-button-closemodal-pmpm')),
                    ], id = 'manager-modal-pmpm',
                style={"text-align":"center"}),
            ])

def manager_card_key_driver(app):
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Key Drivers", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                dbc.Col(
                                    manager_modal_alldrivers(app)),
                            ],
                            no_gutters=True,
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"), style={"width":"100%","height":"100%"}),    
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"), style={"width":"100%","height":"100%"}),    
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"), style={"width":"100%","height":"100%"}),    
                                    ],
                                    width=3
                                ),
                                dbc.Col(
                                    [
                                        html.Img(src=app.get_asset_url("logo-demo.png"), style={"width":"100%","height":"100%"}),    
                                    ],
                                    width=3
                                ),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )

def manager_modal_alldrivers(app):
    return html.Div([
                dbc.Button(
                    "See All Drivers", 
                    id = 'manager-button-openmodal-alldriver', 
                    style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"},
                ),
                 dbc.Modal([
                         dbc.ModalHeader("All Drivers"),
                         dbc.ModalBody(children = html.Div(["contents"], style={"padding":"1rem"})),
                         dbc.ModalFooter(
                                 dbc.Button("Close", id = 'manager-button-closemodal-alldriver',
                                                 style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"},
                                             )
                                 )
                         ], id = 'manager-modal-alldriver', size="lg")
            ],
            
        )

def manager_card_attributed_members(app):

    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Attributed Members", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"width":"100%","height":"100%"})),
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"width":"100%","height":"100%"})),
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"width":"100%","height":"100%"})),
                            ],
                            no_gutters=True,
                        ),
                    ]
                ),
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )


def manager_card_quality_score(app):

    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Quality Score", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"width":"100%","height":"100%"})),
                                dbc.Col(html.Img(src=app.get_asset_url("logo-demo.png"), style={"width":"100%","height":"100%"})),
                            ],
                            no_gutters=True,
                        ),
                        manager_modal_qualityscore(app),
                    ]
                ),
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )

def manager_modal_qualityscore(app):
    return html.Div([
                dbc.Button(
                    "Result Details", 
                    id = 'manager-button-openmodal-qualityscore', 
                    style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"},
                ),
                 dbc.Modal([
                         dbc.ModalHeader("Header"),
                         dbc.ModalBody(children = html.Div(["contents"], style={"padding":"1rem"})),
                         dbc.ModalFooter(
                                 dbc.Button("Close", id = 'manager-button-closemodal-qualityscore',
                                                 style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"},
                                             )
                                 )
                         ], id = 'manager-modal-qualityscore', size="lg")
            ],
            
        )


app.layout = create_layout(app)


@app.callback(
    [Output('manager-div-totalcost-container', 'hidden'),
    Output('manager-div-pmpm-container', 'hidden')],
    [Input('manager-switch-totalcost-pmpm', 'value')]
    )
def switch_totalcost_pmpm(v):
    if v == True:
        return True, False
    return False, True

@app.callback(
    Output('manager-modal-totalcost', 'is_open'),
    [Input('manager-button-openmodal-totalcost', 'n_clicks'),
    Input('manager-button-closemodal-totalcost', 'n_clicks')],
    [State('manager-modal-totalcost', 'is_open')]
    )
def open_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('manager-modal-pmpm', 'is_open'),
    [Input('manager-button-openmodal-pmpm', 'n_clicks'),
    Input('manager-button-closemodal-pmpm', 'n_clicks')],
    [State('manager-modal-pmpm', 'is_open')]
    )
def open_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('manager-modal-alldriver', 'is_open'),
    [Input('manager-button-openmodal-alldriver', 'n_clicks'),
    Input('manager-button-closemodal-alldriver', 'n_clicks')],
    [State('manager-modal-alldriver', 'is_open')]
    )
def open_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('manager-modal-metricsdetail', 'is_open'),
    [Input('manager-button-openmodal-metricsdetail', 'n_clicks'),
    Input('manager-button-closemodal-metricsdetail', 'n_clicks')],
    [State('manager-modal-metricsdetail', 'is_open')]
    )
def open_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('manager-modal-qualityscore', 'is_open'),
    [Input('manager-button-openmodal-qualityscore', 'n_clicks'),
    Input('manager-button-closemodal-qualityscore', 'n_clicks')],
    [State('manager-modal-qualityscore', 'is_open')]
    )
def open_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open



if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True, port = 8052)
