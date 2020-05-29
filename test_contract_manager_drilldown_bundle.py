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

from modal_drilldown_tableview_bundle import *

from app import app
#app = dash.Dash(__name__)
#server = app.server

#df_drilldown=pd.read_csv("data/drilldown_sample_6.csv")

df_bundle_performance=pd.read_csv("data/df_bundle_performance.csv")
df_bundle_performance_pmpm=pd.read_csv("data/df_bundle_performance_pmpm.csv")

df_overall_driver_bundle=pd.read_csv("data/BP_Drivers_Odometer.csv")
df_driver_dtl_bundle=pd.read_csv("data/BP_Drivers_All.csv")
df_driver_default=df_overall_driver_bundle[df_overall_driver_bundle['Bundle Name']=='Major joint replacement of the lower extremity (MJRLE)'].reset_index(drop=True)
df_detail_default=df_driver_dtl_bundle[df_driver_dtl_bundle['Bundle Name']=='Major joint replacement of the lower extremity (MJRLE)'].iloc[:,[1,2]]

data_lv2_bundle=drilldata_process_bundle('Service Category','Bundle Name','Major joint replacement of the lower extremity (MJRLE)')

#modebar display
button_to_rm=['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'hoverClosestCartesian','hoverCompareCartesian','hoverClosestGl2d', 'hoverClosestPie', 'toggleHover','toggleSpikelines']



def create_layout(app):
#    load_data()
    return html.Div(
                [ 
                    html.Div([Header_mgmt_bp(app, False, True, False, False)], style={"height":"6rem"}, className = "sticky-top navbar-expand-lg"),
                       
                    html.Div(
                        [

                            html.Div(col_content_drilldown_bundle(app), id='drilldown-div-bundle-container', hidden=False),
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
                    dbc.DropdownMenuItem("Volume Based Measures", header=True),
                    dbc.DropdownMenuItem("YTD Market Share %"),
                    dbc.DropdownMenuItem("Utilizer Count"),
                    dbc.DropdownMenuItem("Avg Script(30-day adj) per Utilizer"),
                    dbc.DropdownMenuItem("Total Script Count (30-day-adj) by Dosage (in thousand)"),
                    dbc.DropdownMenuItem("Total Units by Dosage (in thousand)"),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Value Based Measures", header=True),
                    dbc.DropdownMenuItem("CHF Related Average Cost per Patient", id="avg_cost"),
                    dbc.DropdownMenuItem("CHF Related Hospitalization Rate", id="bundle"),
                    dbc.DropdownMenuItem("NT - proBNP Change %"),
                    dbc.DropdownMenuItem("LVEF LS Mean Change %"),
                    dbc.DropdownMenuItem(divider=True),
                    html.P(
                        "Select measure to drill.",
                    style={"padding-left":"1rem", "font-size":"0.6rem"}),
                ],
                id="drilldown-dropdownmenu",
                label="CHF Related Average Cost per Patient",
                toggle_style={"font-family":"NotoSans-SemiBold","font-size":"1.2rem","border-radius":"5rem","background-color":"#1357DD"},
            )

def card_selected_measures():
	return html.Div(
			[
				html.H2("Current measure : Value Based Measures - CHF Related Average Cost per Patient", style={"font-size":"1.5rem"})
			],
		)




def col_content_drilldown_bundle(app):
    return html.Div(
            [
                html.Div(
                    [
                        html.Div(card_overview_drilldown_bundle(0.03), style={"max-height":"100rem","padding":"1rem"}),
                        html.Div(card_key_driver_drilldown_bundle(app)),
                    ]
                ),
                
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Div(
                                        [
                                            html.H2("Performance Drilldown", style={"font-size":"2rem"}),
                                            html.H3("check table view for more details...", style={"font-size":"1rem"}),
                                        ],
                                        style={"padding-left":"2rem"}
                                    ), width=8),
                                dbc.Col(modal_drilldown_tableview_bundle(), width=4)
                            ]
                        )
                    ],
                    style={"padding-bottom":"1rem", "padding-top":"2rem"}
                ),
                html.Div(
                    dbc.Tabs(
                        [
                            dbc.Tab(tab_patient_analysis_bundle(app), label="Patient Analysis", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
                            dbc.Tab(tab_physician_analysis_bundle(app), label="Physician Analysis", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
                        ], 
                        # id = 'tab_container'
                    ),
                )
                
            ]
        )


def card_overview_drilldown_bundle(percentage):
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
                            dbc.Col(html.H1("Bundle Payment", style={"font-size":"3rem"}), width="auto"),
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H3("worse than target", style={"font-size":"0.8rem", "color":"#fff"}),
                                        html.H2(str(percentage*100)+"%", style={"font-size":"1.2rem", "margin-top":"-9px", "color":"#fff"}),
                                    ],
                                    style={"margin-top":"-20px"}
                                ),
                                style={"height":"2.5rem", "border":"none", "background-color":color, "text-align":"center", "margin-top":"6px"},
                            ),
                        ],
                        style={"padding-left":"1rem"}
                    ),
                html.P("As of June 30th.", style={"color":"#000", "font-size":"0.8rem","padding-left":"1rem"}),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        table_perform_bundle_drill(df_bundle_performance,df_bundle_performance_pmpm),
                                    ],
                                    style={"padding":"1rem"}
                                )
                            ],
                        ),
#                        dbc.Col(
#                            [
#                                html.Div(
#                                    [
#                                        html.H3("Risk Adjustment Details", style={"font-size":"0.8rem","margin-top":"-1.8rem","color":"#919191","background-color":"#f5f5f5","width":"9rem","padding-left":"1rem","padding-right":"1rem","text-align":"center"}),
#                                        html.Div([dcc.Graph(figure=drill_waterfall(df_drill_waterfall_bundle),style={"height":"24rem","padding-bottom":"1rem"},config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,})]),
#                                    ],
#                                    style={"border-radius":"0.5rem","border":"2px solid #d2d2d2","padding":"1rem","height":"25.5rem"}
#                                )
#                            ],
#                            width=4,
#                            
#                        )
                    ],
                ),
            ],
        )


def card_key_driver_drilldown_bundle(app):
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Key Drivers", style={"font-size":"1rem", "margin-left":"10px"}), width=2),
                                dbc.Col([dbc.Button("See All Drivers", id = 'button-all-driver-bundle',
                                                        style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem"},
                                                    ),
                                        dbc.Modal([
                                                dbc.ModalHeader("All Drivers"),
                                                dbc.ModalBody(children = html.Div([table_driver_all(df_detail_default)],id='table-all-driver-bundle', style={"padding":"1rem"})),
                                                dbc.ModalFooter(
                                                        dbc.Button("Close", id = 'close-all-driver-bundle',
                                                                        style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.8rem"},
                                                                    )
                                                        )
                                                ], id = 'modal-all-driver-bundle', size="lg")],
                                        width=3,
                                        ),
                            ],
                            no_gutters=True,
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(html.Div([gaugegraph(df_driver_default,0)],id='figure-driver-bundle-1', style={"padding-top":"1.5rem"})),
                                                dbc.Col(html.Div(html.H4("{:.1f} %".format(abs(df_driver_default['%'][0]*100)),style={"color":"#ff4d17"}),id='value-driver-bundle-1', style={"font-size":"1rem","color":"#ffeb78","margin-top":"6rem","margin-left":"-1rem"})),
                                            ]
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(html.Div([gaugegraph(df_driver_default,1)],id='figure-driver-bundle-2', style={"padding-top":"1.5rem"})),
                                                dbc.Col(html.Div(html.H4("{:.1f} %".format(abs(df_driver_default['%'][1]*100)),style={"color":"#ff4d17"}),id='value-driver-bundle-2', style={"font-size":"1rem","color":"#aeff78","margin-top":"6rem","margin-left":"-1rem"}))
                                            ]
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(html.Div([gaugegraph(df_driver_default,2)],id='figure-driver-bundle-3', style={"padding-top":"1.5rem"})),
                                                dbc.Col(html.Div(html.H4("{:.1f} %".format(abs(df_driver_default['%'][2]*100)),style={"color":"#ff4d17"}),id='value-driver-bundle-3', style={"font-size":"1rem","color":"#39db44","margin-top":"6rem","margin-left":"-1rem"}),)
                                            ]
                                        )
                                    ]
                                ),
                                
                                
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )



def card_confounding_factors_bundle(app):
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
                               
                                dbc.Col(element_confounding_factors_bundle(0.003, "Benefit Change")),
                                dbc.Col(element_confounding_factors_bundle(-0.002, "Outlier Impact")),
                            ],
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )


def element_confounding_factors_bundle(percentage, factor):
    if percentage > 0:
        color = "success"
    elif percentage == 0:
        color = "secondary"
    else:
        color = "danger"

    return dbc.Row(
            [
                dbc.Col(dbc.Badge(str(abs(percentage*100))+"%", color=color, className="mr-1"), width=3, style={"font-family":"NotoSans-SemiBold"}),
                dbc.Col(html.H6(factor, style = {"font-size":"1rem", "padding-top":"0.1rem"}), width=9),
            ],
            style={"padding":"1rem"}
        )


def tab_patient_analysis_bundle(app):
    return html.Div(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                card_graph1_patient_performance_drilldown_bundle(app),
                                
                                

                    html.Hr(),

                                card_table1_patient_performance_drilldown_bundle(app),

                                
                            ]
                        ),
                        className="mb-3",
                        style={"border":"none", "border-radius":"0.5rem"}
                    ),

                    
                ]
            )


def tab_physician_analysis_bundle(app):
    return html.Div(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                card_graph2_physician_performance_drilldown_bundle(app),
                                
                                

                    html.Hr(),

                                card_table1_physician_performance_drilldown_bundle(app),

                                
                            ]
                        ),
                        className="mb-3",
                        style={"border":"none", "border-radius":"0.5rem"}
                    ),

                    
                ]
            )



def card_graph1_patient_performance_drilldown_bundle(app):
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Performance Drilldown by Bundle Risk", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),
                        
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(html.H1("Major joint replacement of the lower extremity (MJRLE)",id='dimname_on_patient_lv1_bundle', style={"color":"#f0a800", "font-size":"1.5rem","padding-top":"0.8rem"}), width=9),
                                                
                                            ]
                                        )
                                    ],
                                    style={"padding-left":"2rem","padding-right":"1rem","border-radius":"5rem","background-color":"#f7f7f7","margin-top":"2rem"}
                                ), 
                                html.H4("* Default sorting: by Contribution to Overall Performance Difference", style={"font-size":"0.8rem","color":"#919191","padding-top":"1rem","margin-bottom":"-1rem"}),

                                html.Div(drilltable_lv1(drilldata_process_bundle('Bundle Risk','Bundle Name','Major joint replacement of the lower extremity (MJRLE)'),'dashtable_patient_lv1_bundle'),id="drill_patient_lv1_bundle",style={"padding-top":"2rem","padding-bottom":"2rem"}), 
                            ], 
                            style={"max-height":"80rem"}
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )



def card_table1_patient_performance_drilldown_bundle(app):
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Cost by Service Category", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),

                        html.Div(
                            [
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(html.H1("Major joint replacement of the lower extremity (MJRLE)",id='dimname_on_patient_lv2_bundle', style={"color":"#f0a800", "font-size":"1.5rem","padding-top":"1.2rem"}), width=9),
                                                
                                                                                    
                                            ]
                                        )
                                    ],
                                    style={"padding-left":"2rem","padding-right":"1rem","border-radius":"5rem","background-color":"#f7f7f7","margin-top":"2rem"}
                                ), 
                                 
                                html.Div([drilltable_lv3(data_lv2_bundle,'Service Category','dashtable_patient_lv2_bundle',0)],id="drill_patient_lv2_bundle",style={"padding":"1rem"})
                            ], 
                            style={"max-height":"120rem"}
                        ),
                        

                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )

def card_graph2_physician_performance_drilldown_bundle(app):
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Performance Drilldown by Managing Physician", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),

                        html.Div(
                            [
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(html.H1("Major joint replacement of the lower extremity (MJRLE)",id='dimname_on_physician_lv1_bundle', style={"color":"#f0a800", "font-size":"1.5rem","padding-top":"1.2rem"}), width=9),
                                                
                                            ]
                                        )
                                    ],
                                    style={"padding-left":"2rem","padding-right":"1rem","border-radius":"5rem","background-color":"#f7f7f7","margin-top":"2rem"}
                                ), 
                                html.H4("* Default sorting: by Contribution to Overall Performance Difference", style={"font-size":"0.8rem","color":"#919191","padding-top":"1rem","margin-bottom":"-1rem"}),
                                html.Div(drilltable_physician(drilldata_process_bundle('Physician ID','Bundle Name','Major joint replacement of the lower extremity (MJRLE)'),'dashtable_physician_lv1_bundle',1),id="drill_physician_lv1_bundle",style={"padding-top":"2rem","padding-bottom":"2rem"}), 
                            ], 
                            style={"max-height":"80rem"}
                        ),
                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )


def card_table1_physician_performance_drilldown_bundle(app):
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Cost by Service Category", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
                            ],
                            no_gutters=True,
                        ),

                        html.Div(
                            [
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(html.H1("Major joint replacement of the lower extremity (MJRLE)", id='dimname_on_physician_lv2_bundle',style={"color":"#f0a800", "font-size":"1.5rem","padding-top":"1.2rem"}), width=9),
                                                
                                                    
                                            ]
                                        )
                                    ],
                                    style={"padding-left":"2rem","padding-right":"1rem","border-radius":"5rem","background-color":"#f7f7f7","margin-top":"2rem"}
                                ), 
                                
                                html.Div([drilltable_lv3(data_lv2_bundle,'Service Category','dashtable_physician_lv2_bundle',0)],id="drill_physician_lv2_bundle",style={"padding":"1rem"})
                            ], 
                            style={"max-height":"120rem"}
                        ),
                        

                    ]
                ),
                className="mb-3",
                style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)", "border":"none", "border-radius":"0.5rem"}
            )



layout = create_layout(app)
#app.layout = create_layout(app)

##### select drilldown #####
'''
@app.callback(
    [
    Output('drilldown-dropdownmenu-bundle','label'),
    Output('drilldown-div-avgcost-container-bundle', 'hidden'),
    Output('drilldown-div-bundle-container-bundle', 'hidden')],
    [
        Input("avg_cost", "n_clicks"),
        Input("bundle", "n_clicks"),
        
    ],
)
def select_drilldown(*args):
    state_avg_cost = True
    state_bundle = True

    ctx = dash.callback_context

    if not ctx.triggered:
        state_avg_cost = False
        button_id = "avg_cost"
        label = "CHF Related Average Cost per Patient"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == "bundle":
            state_bundle = False
            label = "CHF Related Hospitalization Rate"
        elif button_id == "avg_cost":
            state_avg_cost = False
            label = "CHF Related Average Cost per Patient"


    return label, state_avg_cost, state_bundle

'''
##### bundle drilldown callbacks #####

@app.callback(
    Output("modal-all-driver-bundle","is_open"),
    [Input("button-all-driver-bundle","n_clicks"),
     Input("close-all-driver-bundle","n_clicks")],
    [State("modal-all-driver-bundle","is_open")]        
)
def open_all_driver(n1,n2,is_open):
    if n1 or n2:
        return not is_open
    return is_open



#update patient lv1 table on selected bundle
@app.callback(
   [ Output("drill_patient_lv1_bundle","children"),
     Output("dimname_on_patient_lv1_bundle","children"),
#     Output("dimname_on_patient_lv2_bundle","children"),
     Output("dimname_on_physician_lv1_bundle","children"),
#     Output("dimname_on_physician_lv2_bundle","children"),
     Output("table-all-driver-bundle","children"),
     Output("figure-driver-bundle-1","children"),
     Output("figure-driver-bundle-2","children"),
     Output("figure-driver-bundle-3","children"),
     Output("value-driver-bundle-1","children"),
     Output("value-driver-bundle-2","children"),
     Output("value-driver-bundle-3","children"),
   ],
   [Input("table_perform_drill_bundle","selected_row_ids"),] 
)
def update_data_lv1(row):

    if row is None or row==[]:
        row_1='Major joint replacement of the lower extremity (MJRLE)'
    else:row_1=row[0]

    data_pat=drilldata_process_bundle('Bundle Risk','Bundle Name',row_1)

    df_detail=df_driver_dtl_bundle[df_driver_dtl_bundle['Bundle Name']==row_1].iloc[:,[1,2]]

    df_driver=df_overall_driver_bundle[df_overall_driver_bundle['Bundle Name']==row_1].reset_index(drop=True)

    val1="{:.1f} %".format(abs(df_driver['%'][0]*100))
    val2="{:.1f} %".format(abs(df_driver['%'][1]*100))

    if df_driver['%'][0]>0:
        val1=html.H4("{:.1f} %".format(abs(df_driver['%'][0]*100)),style={"color":"#ff4d17"})
    else:
        val1=html.H4("{:.1f} %".format(abs(df_driver['%'][0]*100)),style={"color":"#18cc75"})

    if df_driver['%'][1]>0:
        val2=html.H4("{:.1f} %".format(abs(df_driver['%'][1]*100)),style={"color":"#ff4d17"})
    else:
        val2=html.H4("{:.1f} %".format(abs(df_driver['%'][1]*100)),style={"color":"#18cc75"})
    
    if len(df_driver)>2:
        figure3=gaugegraph(df_driver,2)
        if df_driver['%'][2]>0:
            val3=html.H4("{:.1f} %".format(abs(df_driver['%'][2]*100)),style={"color":"#ff4d17"})
        else:
            val3=html.H4("{:.1f} %".format(abs(df_driver['%'][2]*100)),style={"color":"#18cc75"})
    else:
        val3=html.H4("")
        figure3=[]

    return drilltable_lv1(data_pat,"dashtable_patient_lv1_bundle"),row_1,row_1,table_driver_all(df_detail),gaugegraph(df_driver,0),gaugegraph(df_driver,1),figure3,val1,val2,val3


#sort patient lv1 
@app.callback(
    Output("dashtable_patient_lv1_bundle","data"),
   [Input('dashtable_patient_lv1_bundle', 'sort_by'),],
   [State('dashtable_patient_lv1_bundle', 'data'),] 
)
def update_data_lv1(sort_dim,data):

    data_pat=pd.DataFrame(data)

    if sort_dim==[]:
        sort_dim=[{"column_id":"Contribution to Overall Performance Difference","direction":"desc"}]
  
    df1=data_pat[0:len(data_pat)-1].sort_values(by=sort_dim[0]['column_id'],ascending= sort_dim[0]['direction']=='asc')
    df1=pd.concat([df1,data_pat.tail(1)])

    return df1.to_dict('records')

#update patient lv2 on patient lv1 select row

@app.callback(
   [Output("dashtable_patient_lv2_bundle","data"), 
    Output("dimname_on_patient_lv2_bundle","children")],
   [ Input("table_perform_drill_bundle","selected_row_ids"),
     Input("dashtable_patient_lv1_bundle","selected_row_ids"),
    ] 
)
def update_table3(row_lv1,row_lv2):

    if row_lv1 is None or row_lv1==[]:
        val1='Major joint replacement of the lower extremity (MJRLE)'
    else:val1=row_lv1[0]

    if row_lv2 is None or row_lv2==[]:
        val2='All'
    else:val2=row_lv2[0]

    
    data_lv3=drilldata_process_bundle('Service Category','Bundle Name',val1,'Bundle Risk',val2) 
    
    return data_lv3.to_dict('records'),'Bundle Risk: '+ val2

#update physician lv1 table on selected bundle
@app.callback(
    Output("drill_physician_lv1_bundle","children"),
   [Input("table_perform_drill_bundle","selected_row_ids"),
   ] 
)
def update_data_lv1(row):

    if row is None or row==[]:
        row_1='Major joint replacement of the lower extremity (MJRLE)'
    else:row_1=row[0]

    data_doc=drilldata_process_bundle('Physician ID','Bundle Name',row_1)
    
    return drilltable_physician(data_doc,"dashtable_physician_lv1_bundle",1)

#sort physician lv1 
@app.callback(
    Output("dashtable_physician_lv1_bundle","data"),
   [Input('dashtable_physician_lv1_bundle', 'sort_by'),],
   [State("dashtable_physician_lv1_bundle","data")] 
)
def update_data_lv1(sort_dim,data):

    data_doc=pd.DataFrame(data)
    
    if sort_dim==[]:
        sort_dim=[{"column_id":"Contribution to Overall Performance Difference","direction":"desc"}]
  
    df1=data_doc[0:len(data_doc)-1].sort_values(by=sort_dim[0]['column_id'],ascending= sort_dim[0]['direction']=='asc')
    df1=pd.concat([df1,data_doc.tail(1)])
    
    return df1.to_dict('records')


#update physician lv2 on physician lv1 select row

@app.callback(
   [Output("dashtable_physician_lv2_bundle","data"), 
   Output("dimname_on_physician_lv2_bundle","children")],
   [ Input("table_perform_drill_bundle","selected_row_ids"),
     Input("dashtable_physician_lv1_bundle","selected_row_ids"),
   ] 
)
def update_table3(row_lv1,row_lv2):

    if row_lv1 is None or row_lv1==[]:
        val1='Major joint replacement of the lower extremity (MJRLE)'
    else:val1=row_lv1[0]

    if row_lv2 is None or row_lv2==[]:
        val2='All'
    else:val2=row_lv2[0]

    
    data_lv3=drilldata_process_bundle('Service Category','Bundle Name',val1,'Physician ID',val2)
    

    return data_lv3.to_dict('records'),'Physician ID: '+val2


##### table view #####
@app.callback(
    Output("drilldown-modal-centered-bundle", "is_open"),
    [Input("drilldown-open-centered-bundle", "n_clicks"), Input("drilldown-close-centered-bundle", "n_clicks")],
    [State("drilldown-modal-centered-bundle", "is_open")],
)
def toggle_modal_dashboard_domain_selection(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    [Output('drilldown-dropdown-dimension-filter-bundle', 'options'),
    Output('drilldown-dropdown-dimension-filter-bundle', 'value'),
    Output('drilldown-dropdown-dimension-filter-bundle', 'disabled')],
    [Input('drilldown-dropdown-dimension-filter-selection-bundle', 'value')]
    )
def update_filter(v):
    if v:
#       if v=='Service Category':
#           return [{'label': k, 'value': k} for k in list(filter_list.keys())], list(filter_list.keys()), False 
#       else:
        return [{'label':k, 'value':k} for k in dimension_bundle[v]], dimension_bundle[v], False
    return [],[],True

@app.callback(
    [Output("drilldown-dropdown-dimension-filter-1-bundle", 'options'),
    Output("drilldown-dropdown-dimension-filter-1-bundle", 'value'),
    Output("drilldown-dropdown-dimension-filter-1-bundle", 'disabled')],
    [Input('drilldown-dropdown-dimension-1-bundle', 'value'),
    Input('drilldown-dropdown-dimension-filter-selection-bundle', 'value'),
    Input('drilldown-dropdown-dimension-filter-bundle', 'value'),
    Input('drilldown-dropdown-dimension-filter-bundle', 'options')]
    )
def update_dimension_filter_1(v1, v2, v3, op):
    if v1:
        if v2 and v1 == v2:
            return op, v3, False
        else:
            
            if v2 and v3:
                df = df_pt_epi_phy_srv_lv1_bundle[df_pt_epi_phy_srv_lv1_bundle[v2].isin(v3)]
            else:
                df = df_pt_epi_phy_srv_lv1_bundle
            options = list(df[v1].unique())
            return [{'label':k, 'value':k} for k in options], options, False 
    return [],[],True

@app.callback(
    [Output('drilldown-dropdown-dimension-2-bundle', 'options'),
    Output('drilldown-dropdown-dimension-2-bundle', 'disabled')],
    [Input('drilldown-dropdown-dimension-1-bundle', 'value')]
    )
def update_dimension_option_2(v):
    if v:
        dropdown_option = [{"label": k, "value": k, 'disabled' : False} for k in list(dimension_bundle.keys()) if len(dimension_bundle[k]) != 0 and k != v]  + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension_bundle.keys()) if len(dimension_bundle[k]) == 0 or k ==v]
        return dropdown_option, False
    return [], True


@app.callback(
    [Output("drilldown-dropdown-dimension-filter-2-bundle", 'options'),
    Output("drilldown-dropdown-dimension-filter-2-bundle", 'value'),
    Output("drilldown-dropdown-dimension-filter-2-bundle", 'disabled')],
    [Input('drilldown-dropdown-dimension-2-bundle', 'value'),
    Input('drilldown-dropdown-dimension-filter-selection-bundle', 'value'),
    Input('drilldown-dropdown-dimension-filter-bundle', 'value'),
    Input('drilldown-dropdown-dimension-1-bundle', 'value'),
    Input('drilldown-dropdown-dimension-filter-1-bundle', 'value'),
    Input('drilldown-dropdown-dimension-filter-bundle', 'options')]
    )
def update_dimension_filter_2(v1, v2, v3, d1, d1v, op):
    if v1:
        if v2 and v1 == v2:
            return op, v3, False
        else:
            
            if v2 and v3:
                df = df_pt_epi_phy_srv_lv1_bundle[(df_pt_epi_phy_srv_lv1_bundle[v2].isin(v3)) & (df_pt_epi_phy_srv_lv1_bundle[d1].isin(d1v))]
            else:
                df = df_pt_epi_phy_srv_lv1_bundle[df_pt_epi_phy_srv_lv1_bundle[d1].isin(d1v)]
            options = list(df[v1].unique())
            return [{'label':k, 'value':k} for k in options], options, False 
    return [],[],True

@app.callback(
    [Output('drilldown-dropdown-dimension-3-bundle', 'options'),
    Output('drilldown-dropdown-dimension-3-bundle', 'disabled')],
    [Input('drilldown-dropdown-dimension-2-bundle', 'value'),
    Input('drilldown-dropdown-dimension-1-bundle', 'value')]
    )
def update_dimension_option_3(v1,v2):
    v = [v1, v2]
    if v1:
        
        dropdown_option = [{"label": k, "value": k, 'disabled' : False} for k in list(dimension_bundle.keys()) if len(dimension_bundle[k]) != 0 and k not in v] + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension_bundle.keys()) if len(dimension_bundle[k]) == 0 or k in v]
        return dropdown_option, False
    return [], True


@app.callback(
    [Output("drilldown-dropdown-dimension-filter-3-bundle", 'options'),
    Output("drilldown-dropdown-dimension-filter-3-bundle", 'value'),
    Output("drilldown-dropdown-dimension-filter-3-bundle", 'disabled')],
    [Input('drilldown-dropdown-dimension-3-bundle', 'value'),
    Input('drilldown-dropdown-dimension-filter-selection-bundle', 'value'),
    Input('drilldown-dropdown-dimension-filter-bundle', 'value'),
    Input('drilldown-dropdown-dimension-1-bundle', 'value'),
    Input('drilldown-dropdown-dimension-filter-1-bundle', 'value'),
    Input('drilldown-dropdown-dimension-2-bundle', 'value'),
    Input('drilldown-dropdown-dimension-filter-2-bundle', 'value'),
    Input('drilldown-dropdown-dimension-filter-bundle', 'options')]
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
            
            if v2 and v3:
                df = df_pt_epi_phy_srv_lv1_bundle[(df_pt_epi_phy_srv_lv1_bundle[v2].isin(v3)) & (df_pt_epi_phy_srv_lv1_bundle[d1].isin(d1v)) & (df_pt_epi_phy_srv_lv1_bundle[d2].isin(d2v))]
            
            else:
                df = df_pt_epi_phy_srv_lv1_bundle[(df_pt_epi_phy_srv_lv1_bundle[d1].isin(d1v)) & (df_pt_epi_phy_srv_lv1_bundle[d2].isin(d2v))]
            options = list(df[v1].unique())
            return [{'label':k, 'value':k} for k in options], options, False 
    return [],[],True

@app.callback(
    Output('drilldown-dropdown-measure-1-bundle', 'options'),
    [Input('drilldown-dropdown-dimension-1-bundle', 'value'),
    Input('drilldown-dropdown-dimension-2-bundle', 'value'),
    Input('drilldown-dropdown-dimension-3-bundle', 'value')]
    )
def update_measure_option(d1, d2, d3):
    d = [d1, d2, d3]
    if len(d) == 0:
        return [{"label": k, "value": k} for k in measure_bundle]
    else:   
        return [{"label": k, "value": k} for k in measure_bundle]

@app.callback(
    [Output('drilldown-datatable-tableview-bundle', "columns"),
    Output('drilldown-datatable-tableview-bundle', "data")],
    [Input('drilldown-dropdown-dimension-1-bundle','value'),
    Input('drilldown-dropdown-dimension-2-bundle','value'),
    Input('drilldown-dropdown-dimension-3-bundle','value'),
    Input('drilldown-dropdown-dimension-filter-1-bundle','value'),
    Input('drilldown-dropdown-dimension-filter-2-bundle','value'),
    Input('drilldown-dropdown-dimension-filter-3-bundle','value'),
    Input('drilldown-dropdown-dimension-filter-selection-bundle','value'),
    Input('drilldown-dropdown-dimension-filter-bundle', 'value'),
    Input('drilldown-dropdown-measure-1-bundle', 'value')]
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
        df_pt_lv1_f = df_pt_lv1_bundle[df_pt_lv1_bundle[f].isin(fv)]
        df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1_bundle[df_pt_epi_phy_srv_lv1_bundle[f].isin(fv)]
    else:
        df_pt_lv1_f = df_pt_lv1_bundle
        df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1_bundle

    d = []
    show_column = []
    if d1 is not None:
        d.append(d1)
    if d2 is not None:
        d.append(d2)
    if d3 is not None:
        d.append(d3)
    show_column = d  + m



    for i in range(3):
        if eval('d'+str(i+1)) and eval('d'+str(i+1)) not in ['Service Category', 'Sub Category']:
            df_pt_lv1_f = df_pt_lv1_f[(df_pt_lv1_f[eval('d'+str(i+1))].isin(eval('d'+str(i+1)+'v')))]
            df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1_f[(df_pt_epi_phy_srv_lv1_f[eval('d'+str(i+1))].isin(eval('d'+str(i+1)+'v')))]
        elif eval('d'+str(i+1)) == 'Service Category':
            df_pt_lv1_f = df_pt_lv1_f
            df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1_f[(df_pt_epi_phy_srv_lv1_f[eval('d'+str(i+1))].isin(eval('d'+str(i+1)+'v')))]
        else:       
            df_pt_lv1_f = df_pt_lv1_f
            df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1_f

    d_set = list(set(d) - set(['Service Category']))
    if len(d_set)>0:
        df_agg_pt = df_pt_lv1_f.groupby(by = d_set).agg({'Episode Count':'sum'}).reset_index()
        df_agg_pt=df_agg_pt.rename(columns={'Episode Count':'Episode Ct'})
        df_agg_cost = df_pt_epi_phy_srv_lv1_f.groupby(by = d).sum().reset_index()

        df_agg = pd.merge(df_agg_cost, df_agg_pt, how = 'left', on = d_set )
               
    else:

        df_agg = df_pt_epi_phy_srv_lv1_f.groupby(by = d).sum().reset_index()
        df_agg['Episode Ct'] = df_pt_lv1_f['Episode Count'].agg('sum')

    cost_all=df_agg['YTD Total Cost'].sum()

   
    epi_all=df_pt_lv1_f['Episode Count'].sum()


    df_agg['Bundle %'] = df_agg['Episode Ct']/epi_all

    df_agg['Cost %'] = df_agg['YTD Total Cost']/cost_all

    df_agg['YTD Utilization/Bundle per 1000'] = df_agg['YTD Utilization']/df_agg['Episode Ct']*1000
    df_agg['Annualized Utilization/Bundle per 1000'] = df_agg['Annualized Utilization']/df_agg['Episode Ct']*1000
    df_agg['Benchmark Utilization/Bundle per 1000'] = df_agg['Benchmark Utilization']/df_agg['Episode Ct']*1000
    df_agg['Diff % from Benchmark Utilization/Bundle'] = (df_agg['Annualized Utilization/Bundle per 1000'] - df_agg['Benchmark Utilization/Bundle per 1000'])/df_agg['Benchmark Utilization/Bundle per 1000']

    df_agg['YTD Total Cost/Bundle'] = df_agg['YTD Total Cost']/df_agg['Episode Ct']
    df_agg['Annualized Total Cost/Bundle'] = df_agg['Annualized Total Cost']/df_agg['Episode Ct']
    df_agg['Benchmark Total Cost/Bundle'] = df_agg['Benchmark Total Cost']/df_agg['Episode Ct']
    df_agg['Diff % from Benchmark Total Cost/Bundle'] = (df_agg['Annualized Total Cost/Bundle'] - df_agg['Benchmark Total Cost/Bundle'])/df_agg['Benchmark Total Cost/Bundle']

    df_agg['YTD Unit Cost'] = df_agg['YTD Total Cost']/df_agg['YTD Utilization']
    df_agg['Annualized Unit Cost'] = df_agg['Annualized Total Cost']/df_agg['Annualized Utilization']
    df_agg['Benchmark Unit Cost'] = df_agg['Benchmark Total Cost']/df_agg['Benchmark Utilization']
    df_agg['Diff % from Benchmark Unit Cost'] = (df_agg['Annualized Unit Cost'] - df_agg['Benchmark Unit Cost'])/df_agg['Benchmark Unit Cost']


    if 'Diff % from Benchmark Total Cost/Bundle' in m:
        df_agg =  df_agg[show_column].sort_values(by =  'Diff % from Benchmark Total Cost/Bundle', ascending =False)
    else:
        df_agg = df_agg[show_column]

    pct_list = ['Cost %','Bundle %','Diff % from Benchmark Utilization/Bundle', 'Diff % from Benchmark Total Cost/Bundle', 'Diff % from Benchmark Unit Cost']
    dollar_list = ['YTD Total Cost/Bundle', 'Annualized Total Cost/Bundle', 'Benchmark Total Cost/Bundle',
    'YTD Unit Cost', 'Annualized Unit Cost', 'Benchmark Unit Cost']

    return [{"name": i, "id": i, "selectable":True,"type":"numeric", "format": FormatTemplate.percentage(1)} if i in pct_list else {"name": i, "id": i, "selectable":True, "type":"numeric","format": FormatTemplate.money(0)} if i in dollar_list else {"name": i, "id": i, "selectable":True, "type":"numeric","format": Format(precision=0,group=',', scheme = Scheme.fixed)} for i in show_column], df_agg.to_dict('records')


if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True,port=8050)









