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
from modal_bundle import *
from bp_contract_calculation import *


app = dash.Dash(__name__, url_base_pathname='/vbc-payer-demo/contract-optimizer/')

server = app.server

file = open('configure/default_ds.json', encoding = 'utf-8')
default_input = json.load(file)
df_quality = pd.read_csv("data/quality_setup.csv")
df_bundle_measure=pd.read_csv("data/bundle_measure_setup.csv")
#df_bundles_default=pd.read_csv("data/df_bundles_30.csv")

# measure_list for episode
measure_epo_list2=df_bundles_default[df_bundles_default['IP/OP'] == "Inpatient"]
measure_epo_list3=['Double joint replacement of the lower extremity','Major joint replacement of the lower extremity (MJRLE)']
measure_epo_list4=['Coronary artery bypass graft']
measure_epo_list5=['Acute myocardial infarction']
measure_epo_list6=['Back and neck except spinal fusion','Back & neck except spinal fusion','Bariatric Surgery','Coronary artery bypass graft','Cardiac valve','Double joint replacement of the lower extremity','Hip and femur procedures except major joint','Lower extremity/humerus procedure except hip, foot, femur','Major bowel procedure','Major joint replacement of the lower extremity (MJRLE)','Major joint replacement of the upper extremity','Spinal fusion']

#modebar display
button_to_rm=['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'hoverClosestCartesian','hoverCompareCartesian','hoverClosestGl2d', 'hoverClosestPie', 'toggleHover','toggleSpikelines']


def create_layout(app):
#    load_data()
    return html.Div(
                [ 
                    html.Div([Header_contract(app, False,True, False, False)], style={"height":"6rem"}, className = "sticky-top navbar-expand-lg"),
                    
                    html.Div(
                        [
                            dbc.Tabs(
							    [
							        dbc.Tab(tab_setup(app), label="Contract Simulation Setup", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
							        dbc.Tab(tab_result(app), label="Result", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
							        
							    ], id = 'bundle-tab-container'
							)
                        ],
                        className="mb-3",
                        style={"padding-left":"3rem", "padding-right":"3rem"},
                    ),

                    # hidden div inside the app to store the temp data
                    html.Div(id = 'bundle-temp-data', style = {'display':'none'}),
                    html.Div(id = 'bundle-temp-result', style = {'display':'none'}),

                    
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
                        	card_performance_measure_setup(app),
                        ]
                    ),                  
				]
			)


def card_performance_measure_setup(app):
	return dbc.Card(
                dbc.CardBody(
                    [
                        card_bundle_selection(app),
                        card_quality_adjustment(app),
                        card_stop_loss_gain(app),
                        html.Div(
                            dbc.Button("SUBMIT",
                                className="mb-3",
                                style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Black", "font-size":"1rem", "width":"8rem"},
                                id = 'bundle-button-submit-simulation'
                            ),
                            style={"text-align":"center"}
                        )
                    ]
                ),
                className="mb-3",
                style={"background-color":"#fff", "border":"none", "border-radius":"0.5rem"}
            )


def card_bundle_selection(app):
	return dbc.Card(
                dbc.CardBody(
                    [
                    	dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Bundle Selection & Target Price", style={"font-size":"1rem", "margin-left":"10px"}), width=4),
                                dbc.Col(html.H6("PLACEHOLDER"), width = 1),
                                dbc.Col(dcc.Dropdown(
                                options = [{'label':'30D', 'value':'30D'},{'label':'60D', 'value':'60D'},{'label':'90D', 'value':'90D'}],
                                value = '90D',
                                id = 'bundle-dropdown-duration',
                                clearable = False,
                                ),width = 1)
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                	html.Div(
                                		dcc.Dropdown(
                                        	options = [
	                                        	{'label' : "Plan's Total Cost", 'value' : "Plan's Total Cost" },
	                                        	{'label' : "ACO's Total Cost", 'value' : "ACO's Total Cost" },
	                                        	{'label' : "ACO's PMPM", 'value' : "ACO's PMPM" },
                                        	],#{'label' : "Plan's Total Revenue", 'value' : "Plan's Total Revenue" }
                                            value = "ACO's PMPM"
                                        ),
                                        style={"padding-left":"0rem","padding-right":"1rem", "height":"0.6rem","font-size":"0.8rem"}
                                    ),
                                    width=4,
                                ),
                                dbc.Col(
                                	[
                                		html.Div(
                                			[
                                				html.H4("Baseline", style={"font-size":"0.6rem"}),
                                                html.Hr(className="ml-1"),
                                				
                                			]
                                		)
                                	],
                                    style={"text-align":"center"},
                                    width=4,
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
                                                            style={"font-size":"0.6rem"}
                                                        ),
                                                    ],
                                                ),
                                                html.Hr(className="ml-1"),
                                				
                                			]
                                		)
                                	],
                                    style={"text-align":"center","padding-left":"4rem"},
                                    width=2,
                                ),
                                dbc.Col(
                                	[
                                		html.Div(
                                			[
                                				html.H4("Likelihood to achieve", style={"font-size":"0.6rem"}),
                                                html.Hr(className="ml-1"),
                                				
                                			]
                                		)
                                	],
                                    style={"text-align":"center","padding-left":"2rem"},
                                    width=2,
                                ),
                            ],
                            style={"padding-right":"1rem", "padding-left":"1rem"}
                        ),
                        
                        card_bundle_table(),
                        bundle_modal_bundles(),
                        
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
            )

def table_setup(df):
    table=dash_table.DataTable(
                    id = 'bundle-table-selectedbundles',
                    columns = [{"name":i,"id":i} for i in df_bundles_default.columns[:8]] +[{"name":'Recommended',"id":'Recommended Target'}]+[{"name":'User Defined',"id":'User Defined Target','editable':True}]+ [{"name":i,"id":i} for i in df_bundles_default.columns[11:13]],
                    
                    data = df.to_dict('records'),
                    # style_cell = {'textAlign': 'center', 'padding': '5px', "font-size":"0.7rem", 'height' : 'auto', 'whiteSpace':'normal'},
                    style_data_conditional=[
                            {
                                'if': {'column_id': 'Bundle'},
                                'textAlign': 'left'
                            },
                            {
                                'if': {'column_id': 'Category'},
                                'textAlign': 'left',
                                'width':'8%'
                            },
                            {
                                'if': {'column_id': 'IP/OP'},
                                'textAlign': 'left',
                                'width':'7%'
                            },
                            {
                                'if': {'column_id': 'User Defined Target'},
                                'border':'1px solid blue',
                                'backgroundColor':'white',

                            },
                            {
                                'if': {
                                'column_id': 'User Defined',
                                'filter_query': '{User Defined} eq "High"'
                                },
                                'backgroundColor':'green',
                                'color':'white'
                            },
                            {
                                'if': {
                                'column_id': 'User Defined',
                                'filter_query': '{User Defined} eq "Mid"'
                                },
                                'backgroundColor':'#f5b111',
                                'color':'black'
                            },
                            {
                                'if': {
                                'column_id': 'User Defined',
                                'filter_query': '{User Defined} eq "Low"'
                                },
                                'backgroundColor':'red',
                                'color':'white'
                            },

                            ] + [
                            {
                                'if':{'column_id':i},
                                'width':'7.5%',
                                
                            } for i in df_bundles_default.columns[3:8]
                            ] + [
                            {
                                'if':{'column_id':i},
                                'width':'7.5%'
                            } for i in df_bundles_default.columns[9:13]
                            ],
                    style_header_conditional = [
                                {'if': {'column_id': 'Bundle'},
                                    'textAlign': 'left'},
                                {'if': {'column_id': 'IP/OP'},
                                    'textAlign': 'left'},
                                {'if': {'column_id': 'Category'},
                                    'textAlign': 'left'}
                                ],
                    style_header={
                        'backgroundColor': '#bfd4ff',
                        'fontWeight': 'bold',
                        'font-family':'NotoSans-Condensed',
                    },
                    style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'backgroundColor':'rgba(0,0,0,0)',
                        'border-left':'0px',
                        'border-right':'0px',
                    },
                   
                    style_cell={
                        'textAlign': 'center',
                        'font-family':'NotoSans-Regular',
                        'fontSize':10,
                        'height' : 'auto', 
                        'whiteSpace':'normal',
                        'max-width':'3rem',
                        'padding':'10px',
                    },
                    #style_as_list_view = True,
                    )
    return table

def card_bundle_table():
    return html.Div(children=table_setup(df_bundles_default.iloc[[0,1,2]]), id = 'bundle-card-bundleselection',style={"width":"100%","padding-left":"1rem","padding-right":"1rem"})



def card_quality_adjustment(app):
	return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Quality Adjustment", style={"font-size":"1rem", "margin-left":"10px"}), width=2),
                                
                                
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.H6("Maximum Adjustment on Positive Reconciliation Amount"), width="auto"),
                                dbc.Col(dbc.InputGroup([
                                    dbc.Input(id = 'bundle-input-adj-pos', type = 'number', debounce = True, value = 10),
                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                    ]), width=1),
                                dbc.Col(html.Div(), width=1),
                                dbc.Col(html.H6("Maximum Adjustment on Negative Reconciliation Amount"), width="auto"),
                                dbc.Col(dbc.InputGroup([
                                    dbc.Input(id = 'bundle-input-adj-neg', type = 'number', debounce = True, value = 10),
                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                    ]), width=1),
                            ]
                        ),
                        html.Div(id='bundle-card-measselection', style={"padding-left":"4rem", "padding-right":"1rem"}
                        ),
                    ]
                ),
                className="mb-3",
                style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem"}
            )


def card_stop_loss_gain(app):
    return dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
                                dbc.Col(html.H4("Stop-Loss/Stop-Gain", style={"font-size":"1rem", "margin-left":"10px"}), width=2),
                                
                                
                            ],
                            no_gutters=True,
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.H6("Stop Loss"), width=2),
                                dbc.Col(dbc.InputGroup([
                                    dbc.Input(id = 'bundle-input-stop-loss', type = 'number', debounce = True, value = 20),
                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                    ]), width=1),
                                dbc.Col(html.Div(), width=2),
                                dbc.Col(html.H6("Stop Gain"), width=2),
                                dbc.Col(dbc.InputGroup([
                                    dbc.Input(id = 'bundle-input-stop-gain', type = 'number', debounce = True, value = 20),
                                    dbc.InputGroupAddon('%', addon_type = 'append'),
                                    ]), width=1),
                            ]
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
                                        dbc.Col(html.Div(html.H2("Bundle", style={"padding":"0.5rem","color":"#fff", "background-color":"#1357DD", "font-size":"1rem", "border-radius":"0.5rem"}), style={"padding-right":"1rem"}), width="auto"),
                                        dbc.Col(dcc.Dropdown(
                                        	id = 'dropdown-bundle',
                                            clearable=False,                                       	
                                        	)),
                                        dbc.Col(html.Div(html.H2("Metric", style={"padding":"0.5rem","color":"#fff", "background-color":"#1357DD", "font-size":"1rem", "border-radius":"0.5rem"}), style={"padding-right":"1rem"}), width="auto"),
                                        dbc.Col(dcc.Dropdown(
                                            id = 'dropdown-metric',
                                            options = [
                                            {'label' : "Cost per Episode", 'value' : "Cost per Episode" },
                                            {'label' : "Total cost", 'value' : "Total cost" },],
                                            value = "Cost per Episode",
                                            clearable=False,
                                            ))
                                    ],
                                    no_gutters=True,
                                ),
                                html.Div(
                                    dbc.Row(
                                        [
                                            dbc.Col(html.Div("1"), width=1),
                                            dbc.Col(dcc.Graph(id = 'bundle-figure-plan',config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},style={"height":"45vh", "width":"60vh"}), width=5),
                                            dbc.Col(html.Div(id = 'bundle-table-plan'), width=6),
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
                                       
                                        
                                    ],
                                    no_gutters=True,
                                ),
                                html.Div(
                                    dbc.Row(
                                        [
                                            dbc.Col(html.Div("1"), width=1),
                                            dbc.Col(dcc.Graph(id = 'bundle-figure-provider',config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},style={"height":"45vh", "width":"60vh"}), width=5),
                                            dbc.Col(html.Div(id = 'bundle-table-provider'), width=6),
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



### bundle selection ###
@app.callback(
    Output('bundle-temp-data', 'children'),
    [Input('bundle-dropdown-duration', 'value')]
    )
def update_basetable(v):
    if v == '30D':
        df_bundles = pd.read_csv("data/df_bundles_30.csv")
    elif v == '60D':
        df_bundles = pd.read_csv("data/df_bundles_60.csv")
    else:
        df_bundles = pd.read_csv("data/df_bundles_90.csv")

    return df_bundles.to_json(orient = 'split')



@app.callback(
    Output('bundle-modal-bundles', 'is_open'),
    [Input('bundle-button-openmodal', 'n_clicks'),
    Input('bundle-button-closemodal', 'n_clicks')],
    [State('bundle-modal-bundles', 'is_open')]
    )
def open_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    [Output('bundle-table-modal-spine', 'data'),
    Output('bundle-table-modal-kidney', 'data'),
    Output('bundle-table-modal-infect', 'data'),
    Output('bundle-table-modal-neuro', 'data'),
    Output('bundle-table-modal-cardi', 'data'),
    Output('bundle-table-modal-pul', 'data'),
    Output('bundle-table-modal-gastro', 'data'),
    Output('bundle-table-modal-op', 'data')],
    [Input('bundle-temp-data', 'children')]
    )
def read_basetable(data):
    df_bundles = pd.read_json(data, orient = 'split')
    data_spine = df_bundles[df_bundles['Category'] == "Spine, Bone, and Joint"].to_dict('records')
    data_kindey = df_bundles[df_bundles['Category'] == "Kidney"].to_dict('records')
    data_infect = df_bundles[df_bundles['Category'] == "Infectious Disease"].to_dict('records')
    data_neuro = df_bundles[df_bundles['Category'] == "Neurological"].to_dict('records')
    data_cardi = df_bundles[df_bundles['Category'] == "Cardiac"].to_dict('records')
    data_pul = df_bundles[df_bundles['Category'] == "Pulmonary"].to_dict('records')
    data_gastro = df_bundles[df_bundles['Category'] == "Gastrointestinal"].to_dict('records')
    data_op = df_bundles[df_bundles['Category'] == "Outpatient"].to_dict('records')
    return data_spine,data_kindey,data_infect,data_neuro,data_cardi,data_pul,data_gastro,data_op


@app.callback(
    [Output('bundle-card-bundleselection', 'children'),
     Output('bundle-card-measselection', 'children'),],
    [Input('bundle-button-closemodal', 'n_clicks'),
    Input('bundle-temp-data', 'children')],
    [State('bundle-table-modal-spine', 'selected_rows'),
    State('bundle-table-modal-kidney', 'selected_rows'),
    State('bundle-table-modal-infect', 'selected_rows'),
    State('bundle-table-modal-neuro', 'selected_rows'),
    State('bundle-table-modal-cardi', 'selected_rows'),
    State('bundle-table-modal-pul', 'selected_rows'),
    State('bundle-table-modal-gastro', 'selected_rows'),
    State('bundle-table-modal-op', 'selected_rows'),]
    )
def update_selected_bundles(n,data,r1,r2,r3,r4,r5,r6,r7,r8):
    df_bundles = pd.read_json(data, orient = 'split')

    if n:

        df1 = df_bundles[df_bundles['Category'] == "Spine, Bone, and Joint"]
        df2 = df_bundles[df_bundles['Category'] == "Kidney"]
        df3 = df_bundles[df_bundles['Category'] == "Infectious Disease"]
        df4 = df_bundles[df_bundles['Category'] == "Neurological"]
        df5 = df_bundles[df_bundles['Category'] == "Cardiac"]
        df6 = df_bundles[df_bundles['Category'] == "Pulmonary"]
        df7 = df_bundles[df_bundles['Category'] == "Gastrointestinal"]
        df8 = df_bundles[df_bundles['Category'] == "Outpatient"]

        update_data = pd.concat([df1.iloc[r1],df2.iloc[r2],df3.iloc[r3],df4.iloc[r4],
            df5.iloc[r5],df6.iloc[r6],df7.iloc[r7],df8.iloc[r8]])


        measure_list=[0,1]
        episode_list=update_data['Bundle']
        episode=['All Episodes','All Episodes']

        for i in range(2,7):
            epi_list_intersection=set(episode_list).intersection( set(eval('measure_epo_list'+str(i)) ))
            if len(epi_list_intersection)>0:

                if i==6:
                    episode.append('All Inpatient Episodes')
                else:
                    epi_for_each_meas=','.join(epi_list_intersection)
                    episode.append(epi_for_each_meas)
                
                measure_list.append(i)

        update_measure=df_bundle_measure.iloc[measure_list].reset_index() 
        update_measure['Applicable Episodes']=episode

    else:
        update_data=df_bundles.iloc[[0,1,2]]
        update_measure=df_bundle_measure.iloc[[0,1,3,6]].reset_index()
        update_measure['Applicable Episodes']=['All Episodes','All Episodes','Major joint replacement of the lower extremity (MJRLE)','All Inpatient Episodes']

    return table_setup(update_data),bundle_measure_setup(update_measure)

# set up table selfupdate
@app.callback(
    Output('bundle-table-selectedbundles', 'data'),
    [Input('bundle-table-selectedbundles', 'data_timestamp'),],
    [State('bundle-table-selectedbundles', 'data'),])
def update_bundlerows(timestamp, data):

    for i in range(0,len(data)):
        row=data[i]
        defined_val=int(str(row['User Defined Target']).replace('$','').replace('%','').replace(',',''))
        recom_val=int(str(row['Recommended Target']).replace('$','').replace('%','').replace(',',''))
        if defined_val/recom_val>=1 :
            row['User Defined']='High'
        elif defined_val/recom_val<=0.9 :
            row['User Defined']='Low'
        else:
            row['User Defined']='Mid'

        row['User Defined Target']='${:,.0f}'.format(defined_val)

    return data

@app.callback(
    [Output('bundle-tab-container', 'active_tab'),
    Output('bundle-temp-result', 'children'),
    Output('dropdown-bundle', 'options'),
    Output('dropdown-bundle', 'value'),],
    [Input('bundle-button-submit-simulation','n_clicks')],
    [State('bundle-table-selectedbundles', 'data'),
#    State('bundle-table-selectedbundles', 'columns'),
    State('bundle-input-adj-pos', 'value'),
    State('bundle-input-adj-neg', 'value'),
    State('bundle-input-stop-loss', 'value'),
    State('bundle-input-stop-gain', 'value')]
    )
def store_inter_results(n, data, adj_pos, adj_neg, stop_loss, stop_gain):
    if n:
        df = pd.DataFrame(data)
        dff = df[['Bundle', 'Bundle Count', 'Average Bundle Cost', 'Recommended Target', 'User Defined Target']]
        dff.columns = ['Bundle', 'Bundle Count', 'Average Bundle Cost', 'Recommended', 'User Defined']
        dff['User Defined'] = dff['User Defined'].apply(lambda x: int(x.replace('$','').replace(',','')))
        dff['Average Bundle Cost'] = dff['Average Bundle Cost'].apply(lambda x: int(x.replace('$','').replace(',','')))
        dff['Recommended'] = dff['Recommended'].apply(lambda x: int(x.replace('$','').replace(',','')))
        adj_pos = adj_pos/100
        adj_neg = adj_neg/100
        stop_loss = stop_loss/100
        stop_gain = stop_gain/100
        result = BP_Contract_Calculation(dff,stop_gain,stop_loss,adj_pos,adj_neg)
 
        drop_opt=[{'label':c,'value':c} for c in result['Bundle'].unique().tolist()]
        drop_default=result['Bundle'].unique().tolist()[0]
        return 'tab-1', result.to_json(orient = 'split'),drop_opt,drop_default
    return 'tab-0',"",[],''

@app.callback(
    [Output('bundle-figure-plan', 'figure'),
    Output('bundle-table-plan', 'children'),
    Output('bundle-figure-provider', 'figure'),
    Output('bundle-table-provider', 'children'),],
    [Input('dropdown-bundle', 'value'),
    Input('dropdown-metric', 'value'),
    Input('bundle-temp-result', 'children')]
    )
def update_grapg_cost(bundle,metric, data):
    ['Category', 'Bundle', 'Contract_type', 'Item', 'Best Estimate',
       'Worst Case', 'Best Case', 'Best Estimate Total', 'Worst Case Total',
       'Best Case Total']
    if data:
        dff = pd.read_json(data, orient = 'split')
        if metric=='Cost per Episode':
            df_plan = dff[(dff['Bundle'] == bundle) & (dff['Category'] == 'Plan')].iloc[:,[2,3,4,5,6]]
            df_provider = dff[(dff['Bundle'] == bundle) & (dff['Category'] == 'Provider')].iloc[:,[2,3,4,5,6]]
        else:
            df_plan = dff[(dff['Bundle'] == bundle) & (dff['Category'] == 'Plan')].iloc[:,[2,3,7,8,9]]
            df_provider = dff[(dff['Bundle'] == bundle) & (dff['Category'] == 'Provider')].iloc[:,[2,3,7,8,9]]

        return sim_bundle_result_box(df_plan), table_bundle_sim_result(df_plan),sim_bundle_result_box(df_provider), table_bundle_sim_result(df_provider)
    return {},"",{},""


if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True,port=8049)


