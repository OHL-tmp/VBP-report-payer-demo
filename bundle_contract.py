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
from modal_test import *
from bp_contract_calculation import *
from assets.color import *
from test_contract_opportunities import *
from modal_simulation_input_bundle import *

from app import app
# app = dash.Dash(__name__)
# server = app.server


df_quality = pd.read_csv("data/quality_setup.csv")
df_bundle_measure=pd.read_csv("data/bundle_measure_setup.csv")

update_measure=df_bundle_measure.iloc[[0,1,3,6]].reset_index()
update_measure['Applicable Episodes']=['All Episodes','All Episodes','All Inpatient Episodes','Major joint replacement of the lower extremity (MJRLE)']

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
					html.Div([Header_contract(app,True, False, False)], style={"height":"6rem"}, className = "sticky-top navbar-expand-lg"),
					
					html.A(id="top"),
					html.Div(
						[
							dbc.Row(
								[
									dbc.Col(
										dbc.Button(
											"Data Intake", 
											className="mr-1", 
											style={"color":blue2, "background-color":blue4, "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"1rem","padding":"0.5rem","padding-left":"2rem","padding-right":"2rem"},
											id = "navigation-data-intake-bundle"
										),
										style={"padding":"1rem"}, 
										align="center",
										width="auto"
									),
									dbc.Col(
										dbc.Button(
											"Opportunity Analysis", 
											className="mr-1", 
											style={"background-color":blue1, "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"1rem","padding":"0.5rem","padding-left":"2rem","padding-right":"2rem", "box-shadow":".5rem .5rem 1.5rem "+blue2},
											id = "navigation-analysis-bundle"
										),
										style={"padding":"1rem"}, 
										align="center",
										width="auto"
									),
									dbc.Col(
										dbc.Button(
											"Simulation Setup", 
											className="mr-1", 
											style={"color":blue2, "background-color":blue4, "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"1rem","padding":"0.5rem","padding-left":"2rem","padding-right":"2rem"},
											id = "navigation-simulation-setup-bundle"
										),
										style={"padding":"1rem"}, 
										align="center",
										width="auto"
									),
									dbc.Col(
										dbc.Button(
											"Result", 
											className="mr-1", 
											style={"color":blue2, "background-color":blue4, "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"1rem","padding":"0.5rem","padding-left":"2rem","padding-right":"2rem"},
											id = "navigation-result-bundle"
										),
										style={"padding":"1rem"}, 
										align="center",
										width="auto"
									)
								],
								justify="around",
								style={"width":"56rem","margin-left":"14rem","margin-right":"18rem","background-color":"#fff", "border":"none", "border-radius":"10rem","padding":"0.5rem", "box-shadow":".7rem .7rem 2rem "+grey2}
							),
							dbc.Row(
								[
									dbc.Col(
										html.Div(
											[
												tab_setup_bundle(app)
											],
											style={"padding-left":"1rem", "padding-right":"1rem"}
										)
									),
								]
							),
							# html.Div(default_temp_data(),id = 'temp-data',  style = {'display':'none'}),
							# html.Div(default_temp_data_medical(),id = 'temp-data-medical',  style = {'display':'none'}),
							# html.Div(assumption_default_data(),id = 'assumption-default-data',  style = {'display':'none'})
						],
						className="mb-3",
						style={"padding-left":"1rem", "padding-right":"1rem"},
					),
					# html.Div(
					# 	[
					# 		dbc.Tabs(
					# 			[
					# 				dbc.Tab(tab_setup(app), label="Contract Simulation Setup", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
					# 				dbc.Tab(tab_result(app), label="Result", style={"background-color":"#fff"}, tab_style={"font-family":"NotoSans-Condensed"}),
									
					# 			], id = 'bundle-tab-container'
					# 		)
					# 	],
					# 	className="mb-3",
					# 	style={"padding-left":"3rem", "padding-right":"3rem"},
					# ),

					# hidden div inside the app to store the temp data
					html.Div(id = 'bundle-temp-data', style = {'display':'none'}),
					html.Div(id = 'bundle-temp-result', style = {'display':'none'}),
					dcc.Store(
						id='bundle-store',
						storage_type= 'session'

					)

					
				],
				style={"background-color":"#f5f5f5"},
			)


def tab_setup_bundle(app):
	return html.Div(
				[
					dbc.Row(
						[
							dbc.Col(html.H1("Contract Simulation", style={"padding-left":"2rem","margin-bottom":"-1rem","font-size":"5rem","color":blue3})),
							
						],
						justify="between",
						style={"padding-top":"2rem","padding-right":"2rem"}
					),

					html.Div(
						[
							card_data_intake_bundle(app),
						],
						hidden=True,
						id="card-data-intake-bundle"
					),

					html.Div(
						[
							card_contract_infomation_bundle(app),
							card_analysis_bundle(app),
						],
						hidden=False,
						id="card-analysis-bundle"
					),
					
					html.Div(
						[
							html.Div(
								[
									card_contract_infomation_bundle(app),
									card_performance_measure_setup(app),
								]
							),
							

							# html.Div(
							# 	[
							# 		dbc.Button(
							# 			"Submit for Simulation", 
							# 			color="primary",
							# 			id = 'button-simulation-submit-bundle', 
							# 			# href='#top',
							# 			style={"border-radius":"10rem","box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)"}
							# 		)
							# 	],
							# 	style={"text-align":"center", "padding-bottom":"2rem"}
							# ),
						],
						hidden=True,
						id="card-simulation-setup-bundle",
						style={}
					),
					
					html.Div(
						[
							tab_result(app)
						],
						hidden=True,
						id="card-result-bundle"
					),
				]
			)


def card_data_intake_bundle(app):
	return dbc.Card(
				dbc.CardBody(
					[
						input_session_bundle(app),
					]
				),
				className="mb-3",
				style={"background-color":yellow_light1, "border":"none", "border-radius":"0.5rem"}
			)



def card_analysis_bundle(app):
	return dbc.Card(
				dbc.CardBody(
					[
						tab_bundle(app),
					]
				),
				className="mb-3",
				style={"background-color":"#fff", "border":"none", "border-radius":"0.5rem"}
			)




def card_contract_infomation_bundle(app):
	return dbc.Card(
				dbc.CardBody(
					[
						dbc.Row(
							[
								dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
								dbc.Col(
									[
										html.H4(
											[
												"Basic Contract Information",
											],
											style={"font-size":"1rem", "margin-left":"10px"}
										),
									],
									
									width="auto"
								),
							],
							no_gutters=True,
						),
						html.Div(
							[
								html.Div(
									[
										html.Div(html.H1("Payor", style={"font-size":"0.8rem"})),
										html.Div(html.P("Humana", style={"font-size":"0.8rem"}), style={"background-color":"#fff", "border":"none", "border-radius":"0.5rem", "width":"10rem","height":"2rem", "padding":"0.5rem","text-align":"start"})
									],
									style={"padding":"1rem"}
								),
								html.Div(
									[
										html.Div(html.H1("LOB", style={"font-size":"0.8rem"})),
										html.Div(html.P("MAPD", style={"font-size":"0.8rem"}), style={"background-color":"#fff", "border":"none", "border-radius":"0.5rem", "width":"8rem","height":"2rem", "padding":"0.5rem","text-align":"start"})
									],
									style={"padding":"1rem"}
								),
								
								html.Div(
									[
										html.Div(html.H1("Contract Period", style={"font-size":"0.8rem"})),
										html.Div(html.P("1/1/2022-12/31/2022", style={"font-size":"0.8rem"}), style={"background-color":"#fff", "border":"none", "border-radius":"0.5rem", "width":"16rem","height":"2rem", "padding":"0.5rem","text-align":"start"})
									],
									style={"padding":"1rem"}
								),
								html.Div(
									[
										html.Div(html.H1("VBC Contract Type", style={"font-size":"0.8rem"})),
										html.Div(html.P("Bundle Payment", style={"font-size":"0.8rem"}), style={"background-color":"#fff", "border":"none", "border-radius":"0.5rem", "width":"20rem","height":"2rem", "padding":"0.5rem","text-align":"start"})
									],
									style={"padding":"1rem"}
								),
								html.Div(
									[
										html.Div(html.H1("% of Total Revenue", style={"font-size":"0.8rem"})),
										html.Div(html.P("2%", style={"font-size":"0.8rem"}), style={"background-color":"#fff", "border":"none", "border-radius":"0.5rem", "width":"8rem","height":"2rem", "padding":"0.5rem","text-align":"start"})
									],
									style={"padding":"1rem"}
								),
							],
							style={"display":"flex"}
						),
					]
				),
				className="mb-3",
				style={"background-color":grey3, "border":"none", "border-radius":"0.5rem", "box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)"}
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
								id = 'button-submit-simulation-bundle',
								href='#top'
							),
							style={"text-align":"center","padding-top":"1rem"}
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
							],
							no_gutters=True,
						),
						dbc.Row(
							[
								dbc.Col(
									dcc.Dropdown(
										options = [{'label':'30D', 'value':'30D'},{'label':'60D', 'value':'60D'},{'label':'90D', 'value':'90D'}],
										value = '90D',
										id = 'bundle-dropdown-duration',
										clearable = False,
										persistence = True, 
										persistence_type = 'memory',
									),
									width = 2
								),
								dbc.Col(
									
									width = 2
								),
								dbc.Col(
									[
										html.Div(
											[
												html.H4("Baseline", style={"font-size":"1rem"}),
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
																"Target",
															],
															style={"font-size":"1rem"}
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
												html.H4("Likelihood to achieve", style={"font-size":"0.8rem"}),
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
		persistence = True, 
		persistence_type = 'memory',
		persisted_props = ['columns.name', 'data', 'filter_query', 'hidden_columns', 'selected_columns', 'selected_rows', 'sort_by'],
#        persisted_props = ['data'],
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
	return html.Div(
				table_setup(df_bundles_default.iloc[[5,13,18]]), 
				id = 'bundle-card-bundleselection',
				style={"width":"100%","padding-left":"1rem","padding-right":"1rem"}
			)



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
								dbc.Col(
									[
										html.H6(
											[
												"Maximum Quality Adjustment on Savings",
												html.Span(
													"\u24D8",
													style={"font-size":"0.8rem"}
												)
											],
											id="tooltip-mqa-saving",
											style={"font-size":"0.8rem"}
										),
										dbc.Tooltip(
											"Maximum reduction in savings as a result of quality adjustment (i.e., when quality score = 0)",
											target="tooltip-mqa-saving",
											style={"text-align":"start"}
										),
									],
									width="auto"
								),
								dbc.Col(dbc.InputGroup([
									dbc.Input(id = 'bundle-input-adj-pos', type = 'number', debounce = True, value = 10,
										persistence = True, 
										persistence_type = 'memory',),
									dbc.InputGroupAddon('%', addon_type = 'append'),
									], size="sm"), width=2),
								dbc.Col(html.Div(), width=2),
								dbc.Col(
									[
										html.H6(
											[
												"Maximum Quality Adjustment on Losses",
												html.Span(
													"\u24D8",
													style={"font-size":"0.8rem"}
												)
											],
											id="tooltip-mqa-loss",
											style={"font-size":"0.8rem"}
										),
										dbc.Tooltip(
											"Maximum reduction in losses/repayment as a result of quality adjustment (i.e., when quality score = 100)",
											target="tooltip-mqa-loss",
											style={"text-align":"start"}
										),
									],
									width="auto"
								),
								dbc.Col(dbc.InputGroup([
									dbc.Input(id = 'bundle-input-adj-neg', type = 'number', debounce = True, value = 10,
										persistence = True, 
										persistence_type = 'memory',),
									dbc.InputGroupAddon('%', addon_type = 'append'),
									], size="sm"), width=2),
							], style={"padding":"1rem"}
						),
						html.Div(children=bundle_measure_setup(update_measure),
							id='bundle-card-measselection', style={"padding-left":"1rem", "padding-right":"1rem"})
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
								dbc.Col(html.H6("Stop Loss", style={"padding-top":"0.5rem"}), width="auto"),
								dbc.Col(dbc.InputGroup([
									dbc.Input(id = 'bundle-input-stop-loss', type = 'number', debounce = True, value = 20,
										persistence = True, 
										persistence_type = 'memory',),
									dbc.InputGroupAddon('%', addon_type = 'append'),
									],size="sm"), width=2),
								dbc.Col(html.H6("of total target payment", style={"padding-top":"0.5rem"}), width="auto"),
								dbc.Col(html.Div(), width=3),
								dbc.Col(html.H6("Stop Gain", style={"padding-top":"0.5rem"}), width="auto"),
								dbc.Col(dbc.InputGroup([
									dbc.Input(id = 'bundle-input-stop-gain', type = 'number', debounce = True, value = 20,
										persistence = True, 
										persistence_type = 'memory',),
									dbc.InputGroupAddon('%', addon_type = 'append'),
									],size="sm"), width=2),
								dbc.Col(html.H6("of total target payment", style={"padding-top":"0.5rem"}), width="auto"),

							], style={"padding":"1rem"}
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
							dbc.Col(html.H1("VBC Contract Simulation Result", style={"padding-left":"2rem","padding-bottom":"3rem","font-size":"1.8rem"})),
							html.Hr(),
							dbc.Col([
								# dbc.Button("View Scenario Assumptions",
								# 	className="mb-3",
								# 	style={"background-color":"#38160f", "border":"none", "border-radius":"0.25rem", "font-family":"NotoSans-Regular", "font-size":"1rem"},
								# 	id = 'button-open-assump-modal'
								# ),
								dbc.Modal([
									dbc.ModalHeader(html.H1("Key Simulation Assumptions", style={"font-family":"NotoSans-Black","font-size":"1.5rem"})),
									dbc.ModalBody([bundle_assumption(),]),
									dbc.ModalFooter(
										dbc.Button('Close', id = 'button-close-assump-modal'))
									], id = 'modal-assump', size = 'xl', backdrop = 'static'),
								],
								width="auto"
							),
							# dbc.Col(
							# 	[
							# 		dbc.DropdownMenu(
							# 		label = 'Choose Version to Generate Contract',
							# 		children = [
							# 					dbc.DropdownMenuItem('User Defined Setting', 
							# 					),
							# 					dbc.DropdownMenuItem('Recommended Setting',
							# 					href = '/vbc-demo/contract-generator-bundle/')
							# 					],
							# 		style={"font-family":"NotoSans-Regular", "font-size":"1rem"},
							# 		color="warning"
							# 		)
							# 	]
							# )
						]
					),
					dbc.Row(
						[
							dbc.Col(html.Div(html.H2("Bundle", style={"padding":"0.5rem","color":"#fff", "background-color":"#1357DD", "font-size":"0.8rem", "border-radius":"0.5rem"}), style={"padding-right":"1rem"}), width="auto"),
							dbc.Col(dcc.Dropdown(
								id = 'dropdown-bundle',
								clearable=False,
								style={"font-size":"0.8rem"},                                      
								),
								width=3
							),
							dbc.Col(width=1),
							dbc.Col(html.Div(html.H2("Metric", style={"padding":"0.5rem","color":"#fff", "background-color":"#1357DD", "font-size":"0.8rem", "border-radius":"0.5rem"}), style={"padding-right":"1rem"}), width="auto"),
							dbc.Col(dcc.Dropdown(
								id = 'dropdown-metric',
								options = [
								{'label' : "Episode Total", 'value' : "Episode Total" },
								{'label' : "Episode Average", 'value' : "Episode Average" },],
								value = "Episode Average",
								clearable=False,
								style={"font-size":"0.8rem"}
								),
								width=3
							),
						]
					),
					dbc.Card(
						dbc.CardBody(
							[
								dbc.Row(
									[
										dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
										dbc.Col(html.H4("Plan's Financial Projection", style={"font-size":"1rem", "margin-left":"10px"}), width=3),
										
									],
									no_gutters=True,
								),
								html.Div(
									dbc.Row(
										[
											dbc.Col(dcc.Graph(id = 'bundle-figure-plan',config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},style={"height":"24rem", "width":"60vh"}), width=5),
											dbc.Col(html.Div(id = 'bundle-table-plan'), width=7),
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
										dbc.Col(html.H4("Provider’s Margin Projection", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
									   
										
									],
									no_gutters=True,
								),
								html.Div(
									dbc.Row(
										[
											dbc.Col(dcc.Graph(id = 'bundle-figure-provider',config={'modeBarButtonsToRemove': button_to_rm,'displaylogo': False,},style={"height":"24rem", "width":"60vh"}), width=5),
											dbc.Col(html.Div(id = 'bundle-table-provider'), width=7),
										],
										no_gutters=True,
									),
									style={"padding":"1rem"}
								)
								
							],
							className="mb-3",
							style={"background-color":"#f7f7f7", "border":"none", "border-radius":"0.5rem", "padding-top":"1rem"}
						)
					),
					html.Hr(),
					html.H1(
						"\u25c9 Best case scenario means more cost reduction is achieved in performance year than expected",
						style={"font-size":"0.8rem"}
					),
					html.H1(
						"\u25c9 Worst case scenario means less cost reduction is achieved in performance year than expected",
						style={"font-size":"0.8rem"}
					)
				],
				style={"padding-top":"2rem","padding-bottom":"2rem","padding-left":"1rem","padding-right":"1rem"}

		)




layout = create_layout(app)
# app.layout = create_layout(app)


## navigation
@app.callback(
	[
	Output('navigation-data-intake-bundle','style'),
	Output('card-data-intake-bundle','hidden'),
	Output('navigation-analysis-bundle','style'),
	Output('card-analysis-bundle','hidden'),
	Output('navigation-simulation-setup-bundle','style'),
	Output('card-simulation-setup-bundle','hidden'),
	Output('navigation-result-bundle','style'),
	Output('card-result-bundle','hidden'),
	],
	[
	Input('navigation-data-intake-bundle','n_clicks'),
	Input('navigation-analysis-bundle','n_clicks'),
	Input('navigation-simulation-setup-bundle','n_clicks'),
	Input('navigation-result-bundle','n_clicks'),
	Input('button-submit-simulation-bundle', 'n_clicks')
	]
	)
def open_modal(n1,n2,n3,n4,submit):
	style_open = {"background-color":blue1, "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"1rem","padding":"0.5rem","padding-left":"2rem","padding-right":"2rem", "box-shadow":".5rem .5rem 1.5rem "+blue2}
	style_close = {"color":blue2, "background-color":blue4, "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"1rem","padding":"0.5rem","padding-left":"2rem","padding-right":"2rem"}
	
	ctx = dash.callback_context

	if not ctx.triggered:
		button_id = 'No clicks yet'
	else:
		button_id = ctx.triggered[0]['prop_id'].split('.')[0]


	if button_id == "navigation-data-intake-bundle":
		return style_open, False, style_close, True, style_close, True, style_close, True
	elif button_id == "navigation-analysis-bundle":
		return style_close, True, style_open, False, style_close, True, style_close, True
	elif button_id == "navigation-simulation-setup-bundle":
		return style_close, True, style_close, True, style_open, False, style_close, True
	elif button_id == "navigation-result-bundle":
		return style_close, True, style_close, True, style_close, True, style_open, False
	elif button_id == "button-submit-simulation-bundle":
		print(button_id)
		return style_close, True, style_close, True, style_close, True, style_open, False
	else:
		return style_close, True, style_open, False, style_close, True, style_close, True


## data intake
@app.callback(
	[
	Output('update-edit-assumption-bundle', 'children'),
	Output('input-intake-s1-1-bundle', 'disabled'),
	Output('input-intake-s1-2-bundle', 'disabled'),
	Output('input-intake-s1-3-bundle', 'disabled'),
	Output('input-intake-s1-4-bundle', 'disabled'),
	Output('input-intake-s1-5-bundle', 'disabled'),
	Output('input-intake-s2-2-bundle', 'disabled'),
	Output('input-intake-s2-3-bundle', 'disabled'),
	Output('input-intake-s5-1-bundle', 'disabled'),
	],
	[Input('update-edit-assumption-bundle', 'n_clicks')],
	[
	State('input-intake-s1-1-bundle', 'disabled')
	]
	)
def toggle_collapse(u, disabled):
	text = "update data"
	if u:
		if disabled:
			text = "save"
		return text, not disabled, not disabled, not disabled, not disabled, not disabled, not disabled, not disabled, not disabled
	return text, disabled, disabled, disabled, disabled, disabled, disabled, disabled, disabled



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


### bundle selection ###
@app.callback(
#	Output('bundle-temp-data', 'children'),
	Output('bundle-store', 'data'),
	[Input('bundle-dropdown-duration', 'value')]
	)
def update_basetable(v):
	if v == '30D':
		df_bundles = pd.read_csv("data/df_bundles_30.csv")
	elif v == '60D':
		df_bundles = pd.read_csv("data/df_bundles_60.csv")
	else:
		df_bundles = pd.read_csv("data/df_bundles_90.csv")

#	return df_bundles.to_json(orient = 'split')
	return df_bundles.to_dict()



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
	[Input('bundle-store', 'data'),
#	Input('bundle-temp-data', 'children'),
	]
	)
def read_basetable(data):
	if data is None:
		raise PreventUpdate

	df_bundles = pd.DataFrame(data)
#	df_bundles = pd.read_json(data, orient = 'split')
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
#	Input('bundle-temp-data', 'children'),
	Input('bundle-store', 'data'),],
	[State('bundle-table-modal-spine', 'selected_rows'),
	State('bundle-table-modal-kidney', 'selected_rows'),
	State('bundle-table-modal-infect', 'selected_rows'),
	State('bundle-table-modal-neuro', 'selected_rows'),
	State('bundle-table-modal-cardi', 'selected_rows'),
	State('bundle-table-modal-pul', 'selected_rows'),
	State('bundle-table-modal-gastro', 'selected_rows'),
	State('bundle-table-modal-op', 'selected_rows'),]
	)
def update_selected_bundles(n,data, r1,r2,r3,r4,r5,r6,r7,r8):
	if data is None:
		raise PreventUpdate

	df_bundles = pd.DataFrame(data)
#	df_bundles = pd.read_json(data, orient = 'split')

#    if n:

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

			if i==2:
				episode.append('All Inpatient Episodes')
			else:
				epi_for_each_meas=','.join(epi_list_intersection)
				episode.append(epi_for_each_meas)
			
			measure_list.append(i)

	update_measure=df_bundle_measure.iloc[measure_list].reset_index() 
	update_measure['Applicable Episodes']=episode

#    else:
#        update_data=df_bundles.iloc[[5,13,18]]
#        update_measure=df_bundle_measure.iloc[[0,1,3,6]].reset_index()
#        update_measure['Applicable Episodes']=['All Episodes','All Episodes','All Inpatient Episodes','Major joint replacement of the lower extremity (MJRLE)']

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
		elif defined_val/recom_val<=0.98 :
			row['User Defined']='Low'
		else:
			row['User Defined']='Mid'

		row['User Defined Target']='${:,.0f}'.format(defined_val)

	return data

@app.callback(
	[
	# Output('bundle-tab-container', 'active_tab'),
	Output('bundle-temp-result', 'children'),
	Output('dropdown-bundle', 'options'),
	Output('dropdown-bundle', 'value'),],
	[Input('button-submit-simulation-bundle','n_clicks')],
	[State('bundle-table-selectedbundles', 'data'),
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
		dff['Average Bundle Cost'] = dff['Average Bundle Cost'].apply(lambda x: int(x.replace('$','').replace(',','')))
		dff['Recommended'] = dff['Recommended'].apply(lambda x: int(x.replace('$','').replace(',','')))
		dff['User Defined'] = dff['User Defined'].apply(lambda x: int(x.replace('$','').replace(',','')))
		
		adj_pos = adj_pos/100
		adj_neg = adj_neg/100
		stop_loss = stop_loss/100
		stop_gain = stop_gain/100
		result = BP_Contract_Calculation(dff,stop_gain,stop_loss,adj_pos,adj_neg)
 
		drop_opt=[{'label':c,'value':c} for c in result['Bundle'].unique().tolist()]
		drop_default=result['Bundle'].unique().tolist()[0]
		return result.to_json(orient = 'split'),drop_opt,drop_default
	return "",[],''

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
		if metric=='Episode Average':
			df_plan = dff[(dff['Bundle'] == bundle) & (dff['Category'] == 'Plan')].iloc[:,[2,3,4,5,6]]
			df_provider = dff[(dff['Bundle'] == bundle) & (dff['Category'] == 'Provider')].iloc[:,[2,3,4,5,6]]
		else:
			df_plan = dff[(dff['Bundle'] == bundle) & (dff['Category'] == 'Plan')].iloc[:,[2,3,7,8,9]]
			df_provider = dff[(dff['Bundle'] == bundle) & (dff['Category'] == 'Provider')].iloc[:,[2,3,7,8,9]]

		return sim_bundle_result_box(df_plan), table_bundle_sim_result(df_plan),sim_bundle_result_box(df_provider), table_bundle_sim_result(df_provider)
	return {},"",{},""

if __name__ == "__main__":
	app.run_server(host="127.0.0.1",debug=True,port=8049)


