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

from app import app

## load data
df_overall=pd.read_csv("data/df_overall.csv")
df_overall_pmpm=pd.read_csv("data/df_overall_pmpm.csv")
df_overall_driver=pd.read_csv("data/df_overall_driver.csv")

df_network_cost_split=pd.read_csv('data/df_network_cost_split.csv')
df_network_facility_split=pd.read_csv('data/df_network_facility_split.csv')
df_network_prof_split=pd.read_csv('data/df_network_prof_split.csv')

#modebar display
button_to_rm=['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'hoverClosestCartesian','hoverCompareCartesian','hoverClosestGl2d', 'hoverClosestPie', 'toggleHover','toggleSpikelines']

def create_layout(app):
#    load_data()
    return html.Div(
                [ 
                    html.Div([Header_mgmt_aco(app, False, True, False, False)], style={"height":"6rem"}, className = "sticky-top navbar-expand-lg"),
                    
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
                html.Div([html.Div([col_menu_drilldown()], style={"border-radius":"5rem","background-color":"none"})], style={"padding-bottom":"2rem"}),
                dbc.Row(
                    [
                        dbc.Col(card_overview_drilldown(0.031),width=8),
                        dbc.Col(card_key_driver_drilldown(app),width=4),
                    ],
                    style={"padding-bottom":"2rem"}
                ),
                card_confounding_factors(app),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Div(
                                        [
                                            html.H2("Drilldown Analysis", style={"font-size":"3rem"}),
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
                            dbc.Tab(tab_patient_cohort_analysis(), label="Patient Analysis", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
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
                html.P("As of 05/22/2020", style={"color":"#000", "font-size":"0.8rem","padding-left":"1rem"}),
                html.Div(
                    [
                        dbc.Tabs(
                            [
                                dbc.Tab(
                                    html.Div(
                                        dcc.Graph(figure=waterfall_overall(df_overall),config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},style={"height":"22rem"})
                                    ), 
                                    label="Total Cost", style={"background-color":"#fff","height":"24rem","padding":"1rem"}, tab_style={"font-family":"NotoSans-Condensed"}
                                ),
                                dbc.Tab(
                                    html.Div(
                                        dcc.Graph(figure=waterfall_overall(df_overall_pmpm),config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},style={"height":"22rem"})
                                    ), 
                                    label="PMPM", style={"background-color":"#fff","height":"24rem","padding":"1rem"}, tab_style={"font-family":"NotoSans-Condensed"}
                                ),
                                
                            ], 
                            # id = 'tab_container'
                        )
                    ],
                    className="mb-3",
                    style={"padding-left":"1rem", "padding-right":"1rem"},
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
                                dbc.Col(html.H4("Key Drivers", style={"font-size":"1rem", "margin-left":"10px"}), width=7),
                                dbc.Col(
                                    [
                                        dbc.Button("See All Drivers",
                                                         id = 'button-all-driver',
                                                        style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"},
                                                    ),
                                         dbc.Modal([
                                                 dbc.ModalHeader(html.H2("All Drivers", style={"font-size":"1.2rem"})),
                                                 dbc.ModalBody(children = html.Div([table_driver_all(df_overall_driver)], style={"padding":"1rem"})),
                                                 dbc.ModalFooter(
                                                         dbc.Button("Close", 
                                                                  id = 'close-all-driver',
                                                                 style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"},
                                                             )
                                                         )
                                                 ], id = 'modal-all-driver', size="lg", backdrop = 'static')
                                    ],
                                    width=4,
                                ),
                            ],
                            no_gutters=True,
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div([gaugegraph(df_overall_driver,0)], style={"padding-top":"1.5rem"}),
                                        html.Div(html.H4("{:.1f} %".format(abs(df_overall_driver['%'][0]*100)),style={"color":"#ff4d17"}), style={"margin-top":"-1.5rem","text-align":"center","font-size":"1rem","color":"#ffeb78"}),
                                    ],
                                    width=6),
                                dbc.Col(
                                    [
                                        html.Div([gaugegraph(df_overall_driver,1)], style={"padding-top":"1.5rem"}),
                                        html.Div(html.H4("{:.1f} %".format(abs(df_overall_driver['%'][1]*100)),style={"color":"#ff4d17"}), style={"margin-top":"-1.5rem","text-align":"center","font-size":"1rem","color":"#ffeb78"}),
                                    ],
                                    width=6),
                                dbc.Col(
                                    [
                                        html.Div([gaugegraph(df_overall_driver,2)], style={"padding-top":"1.5rem"}),
                                        html.Div(html.H4("{:.1f} %".format(abs(df_overall_driver['%'][2]*100)),style={"color":"#ff4d17"}), style={"margin-top":"-1.5rem","text-align":"center","font-size":"1rem","color":"#ffeb78"}),
                                    ],
                                    width=6),
                                dbc.Col(
                                    [
                                        html.Div([gaugegraph(df_overall_driver,3)], style={"padding-top":"1.5rem"}),
                                        html.Div(html.H4("{:.1f} %".format(abs(df_overall_driver['%'][3]*100)),style={"color":"#ff4d17"}), style={"margin-top":"-1.5rem","text-align":"center","font-size":"1rem","color":"#ffeb78"}),
                                    ],
                                    width=6),
                            ],
                            style={"padding-top":"2rem"}
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
                                dbc.Col(element_confounding_factors(-0.002, "Change in Covered Services"), width=4),
                                dbc.Col(element_confounding_factors(0.003, "Benefit Change"), width=4),
                                dbc.Col(element_confounding_factors(-0.002, "Outlier Impact"), width=4),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )


def element_confounding_factors(percentage, factor):
    if percentage < 0:
        color = "danger"
    elif percentage == 0:
        color = "secondary"
    else:
        color = "success"

    return dbc.Row(
            [
                dbc.Col(dbc.Badge(str(percentage*100)+"%", color=color, className="mr-1"), width="auto", style={"font-family":"NotoSans-SemiBold"}),
                dbc.Col(html.H6(factor, style = {"font-size":"1rem", "padding-top":"0.1rem"})),
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
                                        dbc.Col(html.H4("Patient Cohort Analysis: By ", style={"font-size":"1rem", "margin-left":"10px"})),
                                        dbc.Col(html.H4("Patient Health Risk Status",id='name-patient-drill-lv1', style={"font-size":"1rem", "margin-left":"10px"})),
                                        dbc.Col(mod_criteria_button(['Patient Health Risk Level','Gender','Age Band'],'1'),width=2)
                                    ],
                                    no_gutters=True,
                                ),
                                
                                html.Div(
                                    [
                                        drilltable_lv1(drilldata_process('Patient Health Risk Level'),'table-patient-drill-lv1')
                                    ], id="table-patient-drill-lv1-container",
                                    style={"max-height":"80rem","padding-left":"2rem","padding-right":"2rem"}
                                ),
                                
                                

                                html.Hr(style={"padding":"1rem"}),

                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                        dbc.Col(html.H4("Clinical Condition Analysis: ", style={"font-size":"1rem", "margin-left":"10px"})),
                                        dbc.Col(html.H4("Top 10 Chronic",id='name-patient-drill-lv2',  style={"font-size":"1rem", "margin-left":"10px"})),
                                        dbc.Col(mod_criteria_button(['Top 10 Chronic','Top 10 Acute'],'2'),width=2)
                                    ],
                                    no_gutters=True,
                                ),
                                
                                html.Div(
                                    [
                                        drilltable_lv1(drilldata_process('Top 10 Chronic'),'table-patient-drill-lv2')
                                    ], id="table-patient-drill-lv2-container",
                                    style={"max-height":"80rem","padding":"1rem"}
                                ),
                                

                                html.Hr(style={"padding":"1rem"}),

                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                        dbc.Col(html.H4("Cost and Utilization by Service Categories", style={"font-size":"1rem", "margin-left":"10px"})),
                                    ],
                                    no_gutters=True,
                                ),
                                html.Div(
                                    [
                                        drilltable_lv3(drilldata_process('Service Category'),'Service Category','table-patient-drill-lv3',1)
                                    ], id="table-patient-drill-lv3-container",
                                    style={"max-height":"80rem","padding":"1rem"}
                                ),

                                html.Hr(style={"padding":"1rem"}),

                                dbc.Row(
                                    [
                                        dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                        dbc.Col(html.H4("Drilldown by Subcategories", style={"font-size":"1rem", "margin-left":"10px"})),
                                    ],
                                    no_gutters=True,
                                ),
                                html.Div(
                                    [
                                         drilltable_lv3(drilldata_process('Sub Category'),'Sub Category','table-patient-drill-lv4',0)
                                    ], id="table-patient-drill-lv4-container",
                                    style={"max-height":"80rem","padding":"1rem"}
                                ),

                            ]
                        ),
                        className="mb-3",
                        style={"border":"none", "border-radius":"0.5rem","padding-top":"1rem"}
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
                                        dbc.Col(html.H4("Physician Summary: By Specialty", style={"font-size":"1rem", "margin-left":"10px"})),
                                        
                                    ],
                                    no_gutters=True,
                                ),
                                
                                html.Div(
                                    [
                                        drilltable_physician(drilldata_process('Managing Physician Specialty'),'table-physician-drill-lv1',1)
                                    ], id='table-physician-drill-lv1-container',
                                    style={"max-height":"80rem", "padding":"1rem"}
                                ),
                                
                                

                                html.Hr(),

                                dbc.Row(
                                    [
                                        dbc.Col(html.H4("Physician Performance: ", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                        dbc.Col(html.H4("Cardiology",id='name-physician-drill-lv2', style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                                    ],
                                    no_gutters=True,
                                ),
                                
                                html.Div(
                                    [
                                        drilltable_physician(drilldata_process('Managing Physician'),'table-physician-drill-lv2',0)
                                    ], id='table-physician-drill-lv2-container',
                                    style={"padding":"1rem"}
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
                                                dbc.Col(mod_criteria_button(['1'],'3'), style={"padding-top":"0.8rem"}),
                                            ]
                                        )
                                    ],
                                    style={"padding-left":"2rem","padding-right":"1rem","border-radius":"5rem","background-color":"#f7f7f7","margin-top":"2rem"}
                                ), 
                                html.Div(drilltable_lv1(drilldata_process('Patient Health Risk Level'),'dashtable_lv1'),id="drill_lv1",style={"padding-top":"2rem","padding-bottom":"2rem"}), 
                            ], 
                            style={"max-height":"80rem"}
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )

def mod_criteria_button(choice_list,lv='1'):
    return [
                                dbc.Button(
                                    "modify criteria",
                                    id="button-mod-dim-lv"+lv,
                                    className="mb-3",
                                    style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"},
                                ),
                                dbc.Popover([
                                    dbc.PopoverHeader("Modify criteria"),
                                    dbc.PopoverBody([
                                        html.Div(
                                            [
                                                dbc.RadioItems(
                                                    options = [{'label':c , 'value':c}  for c in choice_list #['Risk Status','Gender','Age Band']
                                                              ],
                                                    value = choice_list[0],
                                                    labelCheckedStyle={"color": "#057aff"},
                                                    id = "list-dim-lv"+lv,
                                                    style={"font-family":"NotoSans-Condensed", "font-size":"0.8rem", "padding":"1rem"},
                                                ),
                                            ],
                                            style={"padding-top":"0.5rem", "padding-bottom":"2rem"}
                                        )
                                         
                                       
                                        
                                    ]
                                    ),
                                ],
                                id = "popover-mod-dim-lv"+lv,
                                is_open = False,
                                target = "button-mod-dim-lv"+lv,
                                placement = "top",
                                ),
                                
                            ]
    


layout = create_layout(app)

@app.callback(
    Output("modal-all-driver","is_open"),
    [Input("button-all-driver","n_clicks"),
     Input("close-all-driver","n_clicks")],
    [State("modal-all-driver","is_open")]        
)
def open_all_driver(n1,n2,is_open):
    if n1 or n2:
        return not is_open
    return is_open

# modify lv1 criteria
@app.callback(
    Output("popover-mod-dim-lv1","is_open"),
    [Input("button-mod-dim-lv1","n_clicks"),],
   # Input("mod-button-mod-measure","n_clicks"),
    [State("popover-mod-dim-lv1", "is_open")],
)
def toggle_popover_mod_criteria1(n1, is_open):
    if n1 :
        return not is_open
    return is_open

# modify lv2 criteria
@app.callback(
    Output("popover-mod-dim-lv2","is_open"),
    [Input("button-mod-dim-lv2","n_clicks"),],
   # Input("mod-button-mod-measure","n_clicks"),
    [State("popover-mod-dim-lv2", "is_open")],
)
def toggle_popover_mod_criteria2(n1, is_open):
    if n1 :
        return not is_open
    return is_open


#update lv1 table based on criteria button1
@app.callback(
    [Output("table-patient-drill-lv1-container","children"),
    Output("name-patient-drill-lv1","children"),],
   [Input("list-dim-lv1","value"),] 
)
def update_table_lv1(dim):     

    return drilltable_lv1(drilldata_process(dim),'table-patient-drill-lv1'),dim


#update lv2 table based on criteria button2 and lv1 selected rows
@app.callback(
    [Output("table-patient-drill-lv2-container","children"),
    Output("name-patient-drill-lv2","children"),],
   [Input("list-dim-lv2","value"),
    Input("list-dim-lv1","value"),
    Input("table-patient-drill-lv1","selected_row_ids")] 
)
def update_table_lv2(dim,d1,selected_lv1):

    if selected_lv1 is None or  selected_lv1==[]:
        d1v='All'
    else:
        d1v=selected_lv1[0]

    return drilltable_lv1(drilldata_process(dim,d1,d1v),'table-patient-drill-lv2'),dim

#update lv3 table based on criteria button1,criteria button2, and lv1 selected rows,lv2 selected rows
@app.callback(
    Output("table-patient-drill-lv3-container","children"),
   [Input("list-dim-lv1","value"),
    Input("table-patient-drill-lv1","selected_row_ids"),
    Input("list-dim-lv2","value"),
    Input("table-patient-drill-lv2","selected_row_ids")] 
)
def update_table_lv3(d1,selected_lv1,d2,selected_lv2):

    if selected_lv1 is None or  selected_lv1==[]:
        d1v='All'
    else:
        d1v=selected_lv1[0]

    if selected_lv2 is None or  selected_lv2==[]:
        d2v='All'
    else:
        d2v=selected_lv2[0]


    return drilltable_lv3(drilldata_process('Service Category',d1,d1v,d2,d2v),'Service Category','table-patient-drill-lv3',1)


#update lv4 table based on criteria button1,criteria button2, and lv1 selected rows,lv2 selected rows,lv3 selected rows
@app.callback(
    Output("table-patient-drill-lv4-container","children"),
   [Input("list-dim-lv1","value"),
    Input("table-patient-drill-lv1","selected_row_ids"),
    Input("list-dim-lv2","value"),
    Input("table-patient-drill-lv2","selected_row_ids"),
    Input("table-patient-drill-lv3","selected_row_ids")] 
)
def update_table_lv3(d1,selected_lv1,d2,selected_lv2,selected_lv3):

    if selected_lv1 is None or  selected_lv1==[]:
        d1v='All'
    else:
        d1v=selected_lv1[0]

    if selected_lv2 is None or  selected_lv2==[]:
        d2v='All'
    else:
        d2v=selected_lv2[0]

    if selected_lv3 is None or  selected_lv3==[]:
        d3v='All'
    else:
        d3v=selected_lv3[0]

    return drilltable_lv3(drilldata_process('Sub Category',d1,d1v,d2,d2v,'Service Category',d3v),'Sub Category','table-patient-drill-lv4',0)

#update physician lv2 table based on lv1 selected rows
@app.callback(
    [Output("table-physician-drill-lv2-container","children"),
    Output("name-physician-drill-lv2","children"),],
   [Input("table-physician-drill-lv1","selected_row_ids")] 
)
def update_table_lv2(selected_lv1):

    if selected_lv1 is None or  selected_lv1==[]:
        d1v='All'
    else:
        d1v=selected_lv1[0]

    return drilltable_physician(drilldata_process('Managing Physician','Managing Physician Specialty',d1v),'table-physician-drill-lv2',0),d1v

#update lv1 table based on sort_by
@app.callback(
    Output("table-patient-drill-lv1","data"),
   [Input('table-patient-drill-lv1', 'sort_by'),],
   [State("table-patient-drill-lv1","data")] 
)
def sort_table_lv1(sort_dim,data):
    df=pd.DataFrame(data)

    if sort_dim==[]:
        sort_dim=[{"column_id":"Contribution to Overall Performance Difference","direction":"desc"}]


    df1=df[0:len(df)-1].sort_values(by=sort_dim[0]['column_id'],ascending= sort_dim[0]['direction']=='asc')
    df1=pd.concat([df1,df.tail(1)]).reset_index(drop=True)
    df1['id']=df1[df1.columns[0]]
    df1.set_index('id', inplace=True, drop=False)
    
    return df1.to_dict('records')

#update lv2 table based on sort_by
@app.callback(
    Output("table-patient-drill-lv2","data"),
   [Input('table-patient-drill-lv2', 'sort_by'),],
   [State("table-patient-drill-lv2","data")] 
)
def sort_table_lv2(sort_dim,data):
    df=pd.DataFrame(data)

    if sort_dim==[]:
        sort_dim=[{"column_id":"Contribution to Overall Performance Difference","direction":"desc"}]


    df1=df[0:len(df)-1].sort_values(by=sort_dim[0]['column_id'],ascending= sort_dim[0]['direction']=='asc')
    df1=pd.concat([df1,df.tail(1)]).reset_index(drop=True)
    df1['id']=df1[df1.columns[0]]
    df1.set_index('id', inplace=True, drop=False)
    
    return df1.to_dict('records')

#update lv3 table based on sort_by
@app.callback(
    Output("table-patient-drill-lv3","data"),
   [Input('table-patient-drill-lv3', 'sort_by'),],
   [State("table-patient-drill-lv3","data")] 
)
def sort_table_lv3(sort_dim,data):
    df=pd.DataFrame(data)

    if sort_dim==[]:
        sort_dim=[{"column_id":"Contribution to Overall Performance Difference","direction":"desc"}]


    df1=df[0:len(df)-1].sort_values(by=sort_dim[0]['column_id'],ascending= sort_dim[0]['direction']=='asc')
    df1=pd.concat([df1,df.tail(1)]).reset_index(drop=True)
    df1['id']=df1[df1.columns[0]]
    df1.set_index('id', inplace=True, drop=False)
    
    return df1.to_dict('records')

#update lv4 table based on sort_by
@app.callback(
    Output("table-patient-drill-lv4","data"),
   [Input('table-patient-drill-lv4', 'sort_by'),],
   [State("table-patient-drill-lv4","data")] 
)
def sort_table_lv4(sort_dim,data):
    df=pd.DataFrame(data)

    if sort_dim==[]:
        sort_dim=[{"column_id":"Contribution to Overall Performance Difference","direction":"desc"}]

    if 'Others' in df[df.columns[0]].tolist():
        df1=df[0:len(df)-2].sort_values(by=sort_dim[0]['column_id'],ascending= sort_dim[0]['direction']=='asc')
        df1=pd.concat([df1,df.tail(2)]).reset_index(drop=True)

    else:
        df1=df[0:len(df)-1].sort_values(by=sort_dim[0]['column_id'],ascending= sort_dim[0]['direction']=='asc')
        df1=pd.concat([df1,df.tail(1)]).reset_index(drop=True)

    df1['id']=df1[df1.columns[0]]
    df1.set_index('id', inplace=True, drop=False)
    
    return df1.to_dict('records')

#update physician lv1 table based on sort_by
@app.callback(
    Output("table-physician-drill-lv1","data"),
   [Input('table-physician-drill-lv1', 'sort_by'),],
   [State("table-physician-drill-lv1","data")] 
)
def sort_table_pyhsician_lv1(sort_dim,data):
    df=pd.DataFrame(data)

    if sort_dim==[]:
        sort_dim=[{"column_id":"Avg Cost/Episode Diff % from Best-in-Class","direction":"desc"}]


    df1=df[0:len(df)-1].sort_values(by=sort_dim[0]['column_id'],ascending= sort_dim[0]['direction']=='asc')
    df1=pd.concat([df1,df.tail(1)]).reset_index(drop=True)
    df1['id']=df1[df1.columns[0]]
    df1.set_index('id', inplace=True, drop=False)
    
    return df1.to_dict('records')

#update physician lv2 table based on sort_by
@app.callback(
    Output("table-physician-drill-lv2","data"),
   [Input('table-physician-drill-lv2', 'sort_by'),],
   [State("table-physician-drill-lv2","data")] 
)
def sort_table_pyhsician_lv2(sort_dim,data):
    df=pd.DataFrame(data)

    if sort_dim==[]:
        sort_dim=[{"column_id":"Avg Cost/Episode Diff % from Best-in-Class","direction":"desc"}]


    df1=df[0:len(df)-1].sort_values(by=sort_dim[0]['column_id'],ascending= sort_dim[0]['direction']=='asc')
    df1=pd.concat([df1,df.tail(1)]).reset_index(drop=True)
    df1['id']=df1[df1.columns[0]]
    df1.set_index('id', inplace=True, drop=False)
    
    return df1.to_dict('records')


##### table view #####
@app.callback(
    Output("drilldown-modal-centered", "is_open"),
    [Input("drilldown-open-centered", "n_clicks"), Input("drilldown-close-centered", "n_clicks")],
    [State("drilldown-modal-centered", "is_open")],
)
def toggle_modal_dashboard_domain_selection(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    [Output('drilldown-dropdown-dimension-filter', 'options'),
    Output('drilldown-dropdown-dimension-filter', 'value'),
    Output('drilldown-dropdown-dimension-filter', 'disabled')],
    [Input('drilldown-dropdown-dimension-filter-selection', 'value')]
    )
def update_filter(v):
    if v:
#       if v=='Service Category':
#           return [{'label': k, 'value': k} for k in list(filter_list.keys())], list(filter_list.keys()), False 
#       else:
        return [{'label':k, 'value':k} for k in dimension[v]], dimension[v], False
    return [],[],True

@app.callback(
    [Output("drilldown-dropdown-dimension-filter-1", 'options'),
    Output("drilldown-dropdown-dimension-filter-1", 'value'),
    Output("drilldown-dropdown-dimension-filter-1", 'disabled')],
    [Input('drilldown-dropdown-dimension-1', 'value'),
    Input('drilldown-dropdown-dimension-filter-selection', 'value'),
    Input('drilldown-dropdown-dimension-filter', 'value'),
    Input('drilldown-dropdown-dimension-filter', 'options')]
    )
def update_dimension_filter_1(v1, v2, v3, op):
    if v1:
        if v2 and v1 == v2:
            return op, v3, False
        else:
            if v1 == 'Service Category':
                return [{'label': k, 'value': k} for k in list(filter_list.keys())], list(filter_list.keys()), False 
            else:
                if v2 and v3:
                    df = df_pt_epi_phy_srv_lv1[df_pt_epi_phy_srv_lv1[v2].isin(v3)]
                else:
                    df = df_pt_epi_phy_srv_lv1
                options = list(df[v1].unique())
                return [{'label':k, 'value':k} for k in options], options, False 
    return [],[],True

@app.callback(
    [Output('drilldown-dropdown-dimension-2', 'options'),
    Output('drilldown-dropdown-dimension-2', 'disabled')],
    [Input('drilldown-dropdown-dimension-1', 'value')]
    )
def update_dimension_option_2(v):
    if v:
        if v =='Service Category':
            dropdown_option = [{"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys()) if len(dimension[k]) != 0] + [{"label": 'Service Category', "value": 'Service Category', 'disabled' : True}, {"label": 'Sub Category', "value": 'Sub Category'}] + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension.keys()) if len(dimension[k]) == 0]
            return dropdown_option, False
        else:
            dropdown_option = [{"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys()) if len(dimension[k]) != 0 and k != v] + [{"label": 'Service Category', "value": 'Service Category'}, {"label": 'Sub Category', "value": 'Sub Category', 'disabled' : True}] + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension.keys()) if len(dimension[k]) == 0 or k ==v]
            return dropdown_option, False
    return [], True


@app.callback(
    [Output("drilldown-dropdown-dimension-filter-2", 'options'),
    Output("drilldown-dropdown-dimension-filter-2", 'value'),
    Output("drilldown-dropdown-dimension-filter-2", 'disabled')],
    [Input('drilldown-dropdown-dimension-2', 'value'),
    Input('drilldown-dropdown-dimension-filter-selection', 'value'),
    Input('drilldown-dropdown-dimension-filter', 'value'),
    Input('drilldown-dropdown-dimension-1', 'value'),
    Input('drilldown-dropdown-dimension-filter-1', 'value'),
    Input('drilldown-dropdown-dimension-filter', 'options')]
    )
def update_dimension_filter_2(v1, v2, v3, d1, d1v, op):
    if v1:
        if v2 and v1 == v2:
            return op, v3, False
        else:
            if v1 == 'Service Category':
                return [{'label': k, 'value': k} for k in list(filter_list.keys())], list(filter_list.keys()), False 
            elif v1 == 'Sub Category':
                return [{'label':'All','value':'All'}],["All"],True
            else:
                if v2 and v3:
                    df = df_pt_epi_phy_srv_lv1[(df_pt_epi_phy_srv_lv1[v2].isin(v3)) & (df_pt_epi_phy_srv_lv1[d1].isin(d1v))]
                else:
                    df = df_pt_epi_phy_srv_lv1[df_pt_epi_phy_srv_lv1[d1].isin(d1v)]
                options = list(df[v1].unique())
                return [{'label':k, 'value':k} for k in options], options, False 
    return [],[],True

@app.callback(
    [Output('drilldown-dropdown-dimension-3', 'options'),
    Output('drilldown-dropdown-dimension-3', 'disabled')],
    [Input('drilldown-dropdown-dimension-2', 'value'),
    Input('drilldown-dropdown-dimension-1', 'value')]
    )
def update_dimension_option_3(v1,v2):
    v = [v1, v2]
    if v1:
        if 'Service Category' in v and 'Sub Category' not in v:
            dropdown_option = [{"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys()) if len(dimension[k]) != 0] + [{"label": 'Service Category', "value": 'Service Category', 'disabled' : True}, {"label": 'Sub Category', "value": 'Sub Category'}] + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension.keys()) if len(dimension[k]) == 0]
            return dropdown_option, False
        elif 'Service Category' in v and 'Sub Category' in v:
            dropdown_option =  [{"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys()) if len(dimension[k]) != 0] + [{"label": 'Service Category', "value": 'Service Category', 'disabled' : True}, {"label": 'Sub Category', "value": 'Sub Category', 'disabled' : True}] + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension.keys()) if len(dimension[k]) == 0]
            return dropdown_option, False
        else:
            dropdown_option = [{"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys()) if len(dimension[k]) != 0 and k not in v] + [{"label": 'Service Category', "value": 'Service Category'}, {"label": 'Sub Category', "value": 'Sub Category', 'disabled' : True}] + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension.keys()) if len(dimension[k]) == 0 or k in v]
            return dropdown_option, False
    return [], True


@app.callback(
    [Output("drilldown-dropdown-dimension-filter-3", 'options'),
    Output("drilldown-dropdown-dimension-filter-3", 'value'),
    Output("drilldown-dropdown-dimension-filter-3", 'disabled')],
    [Input('drilldown-dropdown-dimension-3', 'value'),
    Input('drilldown-dropdown-dimension-filter-selection', 'value'),
    Input('drilldown-dropdown-dimension-filter', 'value'),
    Input('drilldown-dropdown-dimension-1', 'value'),
    Input('drilldown-dropdown-dimension-filter-1', 'value'),
    Input('drilldown-dropdown-dimension-2', 'value'),
    Input('drilldown-dropdown-dimension-filter-2', 'value'),
    Input('drilldown-dropdown-dimension-filter', 'options')]
    )
def update_dimension_filter_3(v1, v2, v3, d1, d1v, d2, d2v, op):
    if v3 is None:
        v3 = []
    if d1v is None:
        d1v = []
    if d2v is None:
        d2v = []

    if v1:
        if v2 and v1 == v2:
            return op, v3, False
        else:
            if v1 == 'Service Category':
                return [{'label': k, 'value': k} for k in list(filter_list.keys())], list(filter_list.keys()), False 
            elif v1 == 'Sub Category':
                return [{'label':'All','value':'All'}],["All"],True
            else:
                if v2 and v3:
                    df = df_pt_epi_phy_srv_lv1[(df_pt_epi_phy_srv_lv1[v2].isin(v3)) & (df_pt_epi_phy_srv_lv1[d1].isin(d1v)) & (df_pt_epi_phy_srv_lv1[d2].isin(d2v))]
                elif d2 == 'Sub Category':
                    df = df_pt_epi_phy_srv_lv1[df_pt_epi_phy_srv_lv1[d1].isin(d1v)]
                else:
                    df = df_pt_epi_phy_srv_lv1[(df_pt_epi_phy_srv_lv1[d1].isin(d1v)) & (df_pt_epi_phy_srv_lv1[d2].isin(d2v))]
                options = list(df[v1].unique())
                return [{'label':k, 'value':k} for k in options], options, False 
    return [],[],True

@app.callback(
    Output('drilldown-dropdown-measure-1', 'options'),
    [Input('drilldown-dropdown-dimension-1', 'value'),
    Input('drilldown-dropdown-dimension-2', 'value'),
    Input('drilldown-dropdown-dimension-3', 'value')]
    )
def update_measure_option(d1, d2, d3):
    d = [d1, d2, d3]
    if len(d) == 0:
        return [{"label": k, "value": k} for k in measure]
    else:
        if 'Service Category' in d:
            return [{"label": k, "value": k} for k in measure]
        elif 'Clinical Condition Type' in d or 'Clinical Condition' in d:
            return [{"label": k, "value": k} for k in measure] + [{"label": k, "value": k} for k in clinical_measure] + [{"label": k, "value": k} for k in episode_measure]
        else:
            return [{"label": k, "value": k} for k in measure] + [{"label": k, "value": k} for k in clinical_measure]

@app.callback(
    [Output('drilldown-datatable-tableview', "columns"),
    Output('drilldown-datatable-tableview', "data")],
    [Input('drilldown-dropdown-dimension-1','value'),
    Input('drilldown-dropdown-dimension-2','value'),
    Input('drilldown-dropdown-dimension-3','value'),
    Input('drilldown-dropdown-dimension-filter-1','value'),
    Input('drilldown-dropdown-dimension-filter-2','value'),
    Input('drilldown-dropdown-dimension-filter-3','value'),
    Input('drilldown-dropdown-dimension-filter-selection','value'),
    Input('drilldown-dropdown-dimension-filter', 'value'),
    Input('drilldown-dropdown-measure-1', 'value')]
    )
def datatable_data_selection(d1, d2, d3, d1v, d2v, d3v, f, fv, m):
    if d1v is None:
        d1v = []
    if d2v is None:
        d2v = []
    if d3v is None:
        d3v = []
    if fv is None:
        fv = []

    if f and fv:
        df_pt_lv1_f = df_pt_lv1[df_pt_lv1[f].isin(fv)]
        df_pt_epi_phy_lv1_f = df_pt_epi_phy_lv1[df_pt_epi_phy_lv1[f].isin(fv)]
        df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1[df_pt_epi_phy_srv_lv1[f].isin(fv)]
    else:
        df_pt_lv1_f = df_pt_lv1
        df_pt_epi_phy_lv1_f = df_pt_epi_phy_lv1
        df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1

    d = []
    show_column = []
    if d1 is not None:
        d.append(d1)
    if d2 is not None:
        d.append(d2)
    if d3 is not None:
        d.append(d3)
    show_column = d + ['Patient %'] + m

    


    for i in range(3):
        if eval('d'+str(i+1)) and eval('d'+str(i+1)) not in ['Service Category', 'Sub Category']:
            df_pt_lv1_f = df_pt_lv1_f[(df_pt_lv1_f[eval('d'+str(i+1))].isin(eval('d'+str(i+1)+'v')))]
            df_pt_epi_phy_lv1_f = df_pt_epi_phy_lv1_f[(df_pt_epi_phy_lv1_f[eval('d'+str(i+1))].isin(eval('d'+str(i+1)+'v')))]
            df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1_f[(df_pt_epi_phy_srv_lv1_f[eval('d'+str(i+1))].isin(eval('d'+str(i+1)+'v')))]
        elif eval('d'+str(i+1)) == 'Service Category':
            df_pt_lv1_f = df_pt_lv1_f
            df_pt_epi_phy_lv1_f = df_pt_epi_phy_lv1_f
            df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1_f[(df_pt_epi_phy_srv_lv1_f[eval('d'+str(i+1))].isin(eval('d'+str(i+1)+'v')))]
        else:       
            df_pt_lv1_f = df_pt_lv1_f
            df_pt_epi_phy_lv1_f = df_pt_epi_phy_lv1_f
            df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1_f

    d_set = list(set(d) - set(['Service Category', 'Sub Category']))
    if len(d_set)>0:
        df_agg_pt = df_pt_lv1_f.groupby(by = d_set).agg({'Pt Ct':'nunique', 'Episode Ct':'count'}).reset_index()
        df_agg_clinical = df_pt_epi_phy_lv1_f.groupby(by = d_set).sum().reset_index()
        df_agg_cost = df_pt_epi_phy_srv_lv1_f.groupby(by = d).sum().reset_index()

        df_agg_pre = pd.merge(df_agg_pt, df_agg_clinical, how = 'left', on = d_set )
        df_agg = pd.merge(df_agg_cost, df_agg_pre, how = 'left', on = d_set )


        df_agg['YTD Inpatient Short Stay Utilization'] = 1000*df_agg['YTD Inpatient Short Stay Utilization']/df_agg['Pt Ct']
        df_agg['Annualized Inpatient Short Stay Utilization'] = 1000*df_agg['Annualized Inpatient Short Stay Utilization']/df_agg['Pt Ct']
        df_agg['Benchmark Inpatient Short Stay Utilization'] = 1000*df_agg['Benchmark Inpatient Short Stay Utilization']/df_agg['Pt Ct']
        df_agg['Diff % from Benchmark Inpatient Short Stay Utilization'] = (df_agg['Annualized Inpatient Short Stay Utilization'] - df_agg['Benchmark Inpatient Short Stay Utilization'])/df_agg['Benchmark Inpatient Short Stay Utilization']

        df_agg['YTD Inpatient Short Stay Utilization per Episode'] = 1000*df_agg['YTD Inpatient Short Stay Utilization']/df_agg['Episode Ct']
        df_agg['Annualized Inpatient Short Stay Utilization per Episode'] = 1000*df_agg['Annualized Inpatient Short Stay Utilization']/df_agg['Episode Ct']
        df_agg['Benchmark Inpatient Short Stay Utilization per Episode'] = 1000*df_agg['Benchmark Inpatient Short Stay Utilization']/df_agg['Episode Ct']
        df_agg['Diff % from Benchmark Inpatient Short Stay Utilization per Episode'] = (df_agg['Annualized Inpatient Short Stay Utilization per Episode'] - df_agg['Benchmark Inpatient Short Stay Utilization per Episode'])/df_agg['Benchmark Inpatient Short Stay Utilization per Episode']

        df_agg['YTD 30D Readmission Rate per Episode'] = df_agg['YTD 30D Readmission Rate - N']/df_agg['YTD 30D Readmission Rate - D']
        df_agg['Annualized 30D Readmission Rate per Episode'] = df_agg['Annualized 30D Readmission Rate - N']/df_agg['Annualized 30D Readmission Rate - D']
        df_agg['Benchmark 30D Readmission Rate per Episode'] = df_agg['Benchmark 30D Readm Rate - N']/df_agg['Benchmark 30D Readm Rate - D']
        df_agg['Diff % from Benchmark 30D Readmission Rate per Episode'] = (df_agg['Annualized 30D Readmission Rate per Episode'] - df_agg['Benchmark 30D Readmission Rate per Episode'])/df_agg['Benchmark 30D Readmission Rate per Episode']

        df_agg['YTD 30D Post Discharge ER Rate per Episode'] = df_agg['YTD 30D Post Discharge ER Rate - N']/df_agg['YTD 30D Post Discharge ER Rate - D']
        df_agg['Annualized 30D Post Discharge ER Rate per Episode'] = df_agg['Annualized 30D Post Discharge ER Rate - N']/df_agg['Annualized 30D Post Discharge ER Rate - D']
        df_agg['Benchmark 30D Post Discharge ER Rate per Episode'] = df_agg['Benchmark 30D ER Rate - N']/df_agg['Benchmark 30D ER Rate - D']
        df_agg['Diff % from Benchmark 30D Post Discharge ER Rate per Episode'] = (df_agg['Annualized 30D Post Discharge ER Rate per Episode'] - df_agg['Benchmark 30D Post Discharge ER Rate per Episode'])/df_agg['Benchmark 30D Post Discharge ER Rate per Episode']
        
        
    else:
#           df_agg_pt = df_pt_lv1_f.groupby(by = d_set).agg({'Pt Ct':'nunique', 'Episode Ct':'count'}).reset_index()
#           df_agg_clinical = df_pt_epi_phy_lv1_f.groupby(by = d_set).sum().reset_index()
        df_agg = df_pt_epi_phy_srv_lv1_f.groupby(by = d).sum().reset_index()
        df_agg['Pt Ct'] = 4250
        df_agg['Episode Ct'] = 9867


    df_agg['Patient %'] = df_agg['Pt Ct']/4250
    df_agg['Episode %'] = df_agg['Episode Ct']/9867

    df_agg['YTD Utilization'] = df_agg['YTD Utilization']/df_agg['Pt Ct']
    df_agg['Annualized Utilization'] = df_agg['Annualized Utilization']/df_agg['Pt Ct']
    df_agg['Benchmark Utilization'] = df_agg['Benchmark Utilization']/df_agg['Pt Ct']
    df_agg['Diff % from Benchmark Utilization'] = (df_agg['Annualized Utilization'] - df_agg['Benchmark Utilization'])/df_agg['Benchmark Utilization']

    df_agg['YTD Total Cost'] = df_agg['YTD Total Cost']/df_agg['Pt Ct']
    df_agg['Annualized Total Cost'] = df_agg['Annualized Total Cost']/df_agg['Pt Ct']
    df_agg['Benchmark Total Cost'] = df_agg['Benchmark Total Cost']/df_agg['Pt Ct']
    df_agg['Diff % from Benchmark Total Cost'] = (df_agg['Annualized Total Cost'] - df_agg['Benchmark Total Cost'])/df_agg['Benchmark Total Cost']

    df_agg['YTD Unit Cost'] = df_agg['YTD Total Cost']/df_agg['YTD Utilization']
    df_agg['Annualized Unit Cost'] = df_agg['Annualized Total Cost']/df_agg['Annualized Utilization']
    df_agg['Benchmark Unit Cost'] = df_agg['Benchmark Total Cost']/df_agg['Benchmark Utilization']
    df_agg['Diff % from Benchmark Unit Cost'] = (df_agg['Annualized Unit Cost'] - df_agg['Benchmark Unit Cost'])/df_agg['Benchmark Unit Cost']


    if 'Diff % from Benchmark Total Cost' in m:
        df_agg =  df_agg[show_column].sort_values(by =  'Diff % from Benchmark Total Cost', ascending =False)
    else:
        df_agg = df_agg[show_column]

    pct_list = ['Diff % from Benchmark Utilization', 'Diff % from Benchmark Total Cost', 'Diff % from Benchmark Unit Cost', 'Diff % from Benchmark Inpatient Short Stay Utilization',
    'Episode %', 'Patient %', 'Diff % from Benchmark Inpatient Short Stay Utilization per Episode', 
    'YTD 30D Readmission Rate per Episode', 'Annualized 30D Readmission Rate per Episode','Benchmark 30D Readmission Rate per Episode','Diff % from Benchmark 30D Readmission Rate per Episode',
    'YTD 30D Post Discharge ER Rate per Episode','Annualized 30D Post Discharge ER Rate per Episode','Benchmark 30D Post Discharge ER Rate per Episode', 'Diff % from Benchmark 30D Post Discharge ER Rate per Episode']
    dollar_list = ['YTD Total Cost', 'Annualized Total Cost', 'Benchmark Total Cost',
    'YTD Unit Cost', 'Annualized Unit Cost', 'Benchmark Unit Cost']

    return [{"name": i, "id": i, "selectable":True,"type":"numeric", "format": FormatTemplate.percentage(1)} if i in pct_list else {"name": i, "id": i, "selectable":True, "type":"numeric","format": FormatTemplate.money(0)} if i in dollar_list else {"name": i, "id": i, "selectable":True, "type":"numeric","format": Format(precision=1, scheme = Scheme.fixed)} for i in show_column], df_agg.to_dict('records')



if __name__ == "__main__":
    app.run_server(host="127.0.0.1",port=8049,debug=True)

