import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

import os
import pandas as pd
import numpy as np
import datetime

import pathlib
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State

from app import app
from assets.color import *

# app = dash.Dash(__name__, url_base_pathname='/vbc-demo/')

# server = app.server

base_download_url = 'https://provider-valuegen.onehealthlink.com/'

def modal_simulation_input_bundle():
	return html.Div([
		dbc.Button("Data Intake", id = 'button-edit-assumption',outline=True, color="light", className="mr-1", style={"border-radius":"5rem"}),
			dbc.Modal([
				dbc.ModalHeader(html.H1("Data Intake", style={"font-family":"NotoSans-Black","font-size":"1.5rem"})),
				dbc.ModalBody([
					input_session_bundle(app),
					]),
				dbc.ModalFooter(
					dbc.Button("SAVE", id = 'close-edit-assumption')
					)
				], id = 'modal-edit-assumption', size="xl", is_open = False, backdrop = 'static'),
		])

def input_session_bundle(app):
	return dbc.ListGroup([
		dbc.Row(
			[
				dbc.Col(html.H1("Data Input", style={"color":yellow3, "font-size":"1.2rem","padding-top":"0.8rem", "padding-bottom":"1.5rem"})),
				dbc.Col(dbc.Button("update data", id = 'update-edit-assumption-bundle',outline=True, color="dark", className="mr-1", style={"border-radius":"5rem","width":"8rem"}), style={"padding-top":"0.8rem", "padding-bottom":"1.5rem", "padding-left":"1.5rem", "padding-right":"1.5rem"}, width=2),
			],justify="end"
		),
		
		dbc.Row(
			[
				dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
				dbc.Col(html.H2("Basic Information", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
			],
			no_gutters=True,
			style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		),

		dbc.Row(
			[
				dbc.Col(
					[
						html.H3("1. Payor", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "Aetna", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s1-1-bundle",
									style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}
								)
							],
							style={"padding":"1rem"}
						),
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"1rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
					# width=4,
				),
				dbc.Col(
					[
						html.H3("2. LOB", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "MAPD", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s1-2-bundle",
									style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})
							],
							style={"padding":"1rem"}
						),
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"0.8rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
					# width=4,
				),
			],
			style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		),

		dbc.Row(
			[
				dbc.Col(
					[
						html.H3("3. Contract Period", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "1/1/2022-12/31/2022", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s1-3-bundle",
									style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}
								)
							],
							style={"padding":"1rem"}
						),
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"1rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
					# width=4,
				),
				dbc.Col(
					[
						html.H3("4. VBC Contract Type", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "Bundle Payment", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s1-4-bundle",
									style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})
							],
							style={"padding":"1rem"}
						),
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"0.8rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
					# width=4,
				),
			],
			style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		),

		dbc.Row(
			[
				dbc.Col(
					[
						html.H3("5. % of Total Revenue", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "5%", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s1-5-bundle",
									style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}
								)
							],
							style={"padding":"1rem"}
						),
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"1rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
					# width=4,
				),
				dbc.Col(
					[
						
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"1rem", "background-color":yellow_light1, "border":"none", "border-radius":"0.5rem"},
					# width=6,
				),
			],
			style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		),

		html.Hr(),

		dbc.Row(
			[
				dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
				dbc.Col(html.H2("Patient and Claim Data", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
			],
			no_gutters=True,
			style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		),
		dbc.Row(
			[
				dbc.Col(
					[
						html.H3("1. Provider’s historical patient and claim data for the most recent 36 months", style={"font-size":"1rem"}),
						html.Div(
								[
									dbc.Row(
										[
											dbc.Col(
												html.Div(
													[
														html.A('View Attachment', 
															id = 'download-claim-bundle',
															href=base_download_url + 'downloads/Geographic Distribution template.xlsx',
															target = "_blank")
													], style={"font-size":"1rem","padding-left":"0.8rem"}
												),
												width=4
											),
										# dbc.Col(
										# 	dcc.Upload(
										# 		id = 'upload-geo',
										# 		children = html.Div([
										# 			'Select Related Files to Upload'
										# 			],style={"font-family":"NotoSans-Regular","font-size":"0.8rem","text-decoration":"underline","color":"#1357DD"}),
										# 		style={
										# 			'height': '40px',
										# 			'lineHeight': '40px',
										# 			'borderWidth': '1px',
										# 			'borderStyle': 'dashed',
										# 			'borderRadius': '5px',
										# 			'textAlign': 'center'
										# 			}
										# 		), 
										# 	# width = 3
										# 	),
										dbc.Col(
											html.Div(id = 'output-claim-upload-bundle', style={"text-align":"center","padding":"0.5rem","font-family":"NotoSans-Regular","font-size":"0.6rem"}),
											width=1
											)
										]
									)
								],
								style={"padding":"1rem"}
							),
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"0.8rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
					# width=4,
				),
				dbc.Col(
					[
						html.H3("2. Expected annual patient growth % under FFS contract", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "5%", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s2-2-bundle",
									style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}
								)
							],
							style={"padding":"1rem"}
						),
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"1rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
					# width=5,
				),
			],
			style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		),

		dbc.Row(
			[
				dbc.Col(
					[
						html.H3("3. Expected annual patient growth % under VBC contract", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "5%", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s2-3-bundle",
									style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}
								)
							],
							style={"padding":"1rem"}
						),
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"1rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
					# width=4,
				),
				dbc.Col(
					[
						
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"1rem", "background-color":yellow_light1, "border":"none", "border-radius":"0.5rem"},
					# width=6,
				),
			],
			style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		),


		html.Hr(),

		dbc.Row(
			[
				dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
				dbc.Col(html.H2("Care Management", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
			],
			no_gutters=True,
			style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		),
		dbc.Row(
			[
				dbc.Col(
					[
						html.H3("1. Description of current care management program", style={"font-size":"1rem"}),
						dbc.Row(
							[
								dbc.Col(
									html.Div(
										[
											html.A('View Attachment', 
												id = 'download-cmp-bundle',
												href=base_download_url + 'downloads/Geographic Distribution template.xlsx',
												target = "_blank")
										], style={"font-size":"1rem","padding":"0.5rem"}
									),
									# width=3
								),
							],
							style={"padding":"1rem"}
						),
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"0.8rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
					# width=4,
				),
				dbc.Col(
					[
						
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"1rem", "background-color":yellow_light1, "border":"none", "border-radius":"0.5rem"},
					# width=6,
				),
			],
			style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		),


		html.Hr(),

		dbc.Row(
			[
				dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
				dbc.Col(html.H2("Contract Information", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
			],
			no_gutters=True,
			style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		),
		dbc.Row(
			[
				dbc.Col(
					[
						html.H3("1. Payor’s member inclusion/exclusion criteria", style={"font-size":"1rem"}),
						dbc.Row(
							[
								dbc.Col(
									html.Div(
										[
											html.A('View Attachment', 
												id = 'download-excl-bundle',
												href=base_download_url + 'downloads/Geographic Distribution template.xlsx',
												target = "_blank")
										], style={"font-size":"1rem","padding":"0.5rem"}
									),
									# width=3
								),
							],
							style={"padding":"1rem"}
						),
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"0.8rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
					# width=4,
				),
				dbc.Col(
					[
						html.H3("2. Payor’s contract term", style={"font-size":"1rem"}),
						dbc.Row(
							[
								dbc.Col(
									html.Div(
										[
											html.A('View Attachment', 
												id = 'download-term-bundle',
												href=base_download_url + 'downloads/Geographic Distribution template.xlsx',
												target = "_blank")
										], style={"font-size":"1rem","padding":"0.5rem"}
									),
									# width=3
								),
							],
							style={"padding":"1rem"}
						),
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"1rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
					# width=4,
				),
				dbc.Col(
					[
						html.H3("3. Payor’s quality metrics", style={"font-size":"1rem"}),
						dbc.Row(
							[
								dbc.Col(
									html.Div(
										[
											html.A('View Attachment', 
												id = 'download-quality-bundle',
												href=base_download_url + 'downloads/Geographic Distribution template.xlsx',
												target = "_blank")
										], style={"font-size":"1rem","padding":"0.5rem"}
									),
									# width=3
								),
							],
							style={"padding":"1rem"}
						),
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"1rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
					# width=4,
				),
				
				
			],
			style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		),

		html.Hr(),
		dbc.Row(
			[
				dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
				dbc.Col(html.H2("FFS Margin", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
			],
			no_gutters=True,
			style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		),
		dbc.Row(
			[
				dbc.Col(
					[
						html.H3("1. Margin % with FFS arrangement", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "5%", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s5-1-bundle",
									style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}
								)
							],
							style={"padding":"1rem"}
						),
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"1rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
					# width=4,
				),
				dbc.Col(
					[
						
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"1rem", "background-color":yellow_light1, "border":"none", "border-radius":"0.5rem"},
					# width=6,
				),
			],
			style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		),


		

	],
    style={"border-radius":"0.5rem"})

# def card_collapse_age_pharmacy():
# 	return dbc.Card(
# 			[
# 				dbc.Row([
# 					dbc.Col(html.H2("AGE BAND", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
# 					dbc.Col(html.H2("MEMBER %", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
# 					], style={"padding-top":"1rem"}),
# 				html.Hr(),
# 				dbc.Row([
# 					dbc.Col("Newborn (0-1m)", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "0.0%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("1m-2y", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "0.0%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("2-12", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "0.0%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("12-17", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "0.0%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("18-24", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "0.2%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("25-34", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "0.4%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("35-44", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "1.0%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("45-54", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "1.6%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("55-64", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "1.8%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("65-74", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "18%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("75-84", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "44%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col(">=85", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "33%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 			], style={"font-family":"NotoSans-Regular","font-size":"1rem","margin-top":"2rem", "padding":"2rem","border-radius":"0.5rem", "box-shadow":".5rem .5rem 2rem "+grey2}
# 		)

# def card_collapse_gender_pharmacy():
# 	return dbc.Card([
# 				dbc.Row([
# 					dbc.Col(html.H2("GENDER", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
# 					dbc.Col(html.H2("MEMBER %", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
# 					], style={"padding-top":"1rem"}),
# 				html.Hr(),
# 				dbc.Row([
# 					dbc.Col("Female", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "53%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("Male", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "47%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				], style={"font-family":"NotoSans-Regular","font-size":"1rem","margin-top":"2rem", "padding":"2rem","border-radius":"0.5rem", "box-shadow":".5rem .5rem 2rem "+grey2})


# def card_collapse_tier_pharmacy():
# 	return dbc.Card(
# 			[
# 				dbc.Row([
# 					dbc.Col(html.H2("Tier", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
# 					dbc.Col(html.H2("Days of Supply", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
# 					dbc.Col(html.H2("Copay", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
# 					dbc.Col(html.H2("Coinsurance", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
# 					dbc.Col(html.H2("Max Copay", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
# 					], style={"padding-top":"1rem"}),
# 				html.Hr(),
# 				dbc.Row(
# 					[
# 						dbc.Col("Tier 1", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 						dbc.Col("30",style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
# 						dbc.Col(dbc.Input(value = "$5", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 					], style={"padding-top":"1rem"}
# 				),
# 				dbc.Row(
# 					[
# 						dbc.Col("Tier 1", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 						dbc.Col("90", style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
# 						dbc.Col(dbc.Input(value = "$10", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 					], style={"padding-top":"1rem"}
# 				),
# 				dbc.Row(
# 					[
# 						dbc.Col("Tier 2", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 						dbc.Col("30", style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
# 						dbc.Col(dbc.Input(value = "$10", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 					], style={"padding-top":"1rem"}
# 				),
# 				dbc.Row(
# 					[
# 						dbc.Col("Tier 2", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 						dbc.Col("90", style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
# 						dbc.Col(dbc.Input(value = "$20", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 					], style={"padding-top":"1rem"}
# 				),
# 				dbc.Row(
# 					[
# 						dbc.Col("Tier 3", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 						dbc.Col("30", style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
# 						dbc.Col(dbc.Input(value = "$40",bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 					], style={"padding-top":"1rem"}
# 				),
# 				dbc.Row(
# 					[
# 						dbc.Col("Tier 3", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 						dbc.Col("90", style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
# 						dbc.Col(dbc.Input(value = "$100",bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 					], style={"padding-top":"1rem"}
# 				),
# 				dbc.Row(
# 					[
# 						dbc.Col("Tier 4", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 						dbc.Col("30", style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
# 						dbc.Col(dbc.Input(value = "$70",bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 					], style={"padding-top":"1rem"}
# 				),
# 				dbc.Row(
# 					[
# 						dbc.Col("Tier 4", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 						dbc.Col("90", style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
# 						dbc.Col(dbc.Input(value = "$150",bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 					], style={"padding-top":"1rem"}
# 				),
# 				dbc.Row(
# 					[
# 						dbc.Col("Tier 5", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 						dbc.Col("30", style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
# 						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(value = "20%",bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(value = "$200",bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 					], style={"padding-top":"1rem"}
# 				),
# 				dbc.Row(
# 					[
# 						dbc.Col("Tier 5", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 						dbc.Col("90", style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
# 						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(value = "20%",bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 						dbc.Col(dbc.Input(value = "$400",bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 					], style={"padding-top":"1rem"}
# 				),
# 				dbc.Row(
# 					[
# 						dbc.Col("Maximum OOP per Individual", style={"font-family":"NotoSans-Regular","font-size":"1rem"}),
# 						dbc.Col(dbc.Input(value = '$2800', bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
# 					], style={"padding-top":"1rem"}
# 				),
# 			],
# 			style={"font-family":"NotoSans-Regular","font-size":"1rem","margin-top":"2rem", "padding":"2rem","border-radius":"0.5rem", "box-shadow":".5rem .5rem 2rem "+grey2}
# 		)



# def card_collapse_month_pharmacy():
# 	return dbc.Card(
# 			[
# 				dbc.Row([
# 					dbc.Col(html.H2("MONTH", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
# 					dbc.Col(html.H2("RAMP UP", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
# 					], style={"padding-top":"1rem"}),
# 				html.Hr(),
# 				dbc.Row([
# 					dbc.Col("Month 1", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "2%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("Month 2", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "3%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("Month 3", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "4%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("Month 4", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "5%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("Month 5", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "6%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("Month 6", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "7%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("Month 7", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "7%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("Month 8", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "7%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("Month 9", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "7%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("Month 10", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "7%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("Month 11", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "7%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 				dbc.Row([
# 					dbc.Col("Month 12", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
# 					dbc.Col(dbc.Input(value = "7%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
# 					], style={"padding-top":"1rem"}),
# 			], style={"font-family":"NotoSans-Regular","font-size":"1rem","margin-top":"2rem", "padding":"2rem","border-radius":"0.5rem", "box-shadow":".5rem .5rem 2rem "+grey2}
# 		)

# def download_template_pharmacy():
# 	return html.A(
# 				"Download the template file",
# 				id = 'download-link',
# 				href='http://139.224.186.182:8098/downloads/Pharma Value-Based Measures Template.xlsx',
# 				target = "_blank"
# 			)


# def card_data_intake_collapse_rampup_pharmacy():
# 	cardbody = [dbc.Row([
# 					dbc.Col(html.H2("MONTHLY RAMPUP", style={"font-size":"0.8rem", "margin-left":"10px"}), width=6),
# 					# dbc.Col(html.H2("RAMP UP", style={"font-size":"1rem", "margin-left":"10px"})),
# 					], style={"padding":"0.5rem","padding-left":"3rem"}),]
	

# 	for i in range(12):
# 		if i%2 == 1:
# 			extra_style = {"padding":"0.5rem", "padding-left":"3.5rem","background-color":"#f1f1f1", "border":"none", "border-radius":"0rem"}
# 		else:
# 			extra_style = {"padding":"0.5rem","padding-left":"3.5rem"}
# 		cardbody.append(dbc.Row([
# 			dbc.Col("Month {}".format(i+1), style={"font-family":"NotoSans-Regular","font-size":"0.8rem","margin-top":"0.2rem"}, width=2),
# 			dbc.Col(
# 				dbc.InputGroup([
# 				dbc.Input(
# 					value = 2, 
# 					type = 'number',
# 					bs_size="sm", 
# 					persistence = True, 
# 					persistence_type = 'session', 
# 					disabled = True,
# 					style={"color":"#000","font-family":"NotoSans-Regular"}
# 				),
# 				dbc.InputGroupAddon('%', addon_type = 'append')], size="sm"),
# 				width=5
# 				),
# 			dbc.Col(
# 				dbc.InputGroup([
# 				dbc.Input(
# 					value = 10, 
# 					type = 'number',
# 					bs_size="sm", 
# 					persistence = True, 
# 					persistence_type = 'session', 
# 					disabled = True,
# 					style={"color":"#000","font-family":"NotoSans-Regular"}
# 				),
# 				dbc.InputGroupAddon('%', addon_type = 'append')], size="sm"),
# 				width=5,
# 				)
# 			], style=extra_style),)
# 	return dbc.Card(
# 			cardbody
# 			, style={"font-family":"NotoSans-Regular","font-size":"1rem", "padding":"1rem"}
# 		)

#app.layout = modal_simulation_input_bundle(app)

#if __name__ == "__main__":
#	app.run_server(host="0.0.0.0",port=8094, debug = True)


