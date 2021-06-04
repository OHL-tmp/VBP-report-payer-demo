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

# base_download_url = 'http://localhost:8099'
base_download_url = 'https://provider-valuegen.onehealthlink.com/'

def modal_simulation_input_newcontract():
	return html.Div([
		dbc.Button("\u002B Add New Contract", id = 'button-edit-assumption-newcontract',outline=True, color="dark", className="mr-1", style={"border-radius":"5rem"}),
			dbc.Modal([
				dbc.ModalHeader(html.H1("Edit New Contract Data", style={"font-family":"NotoSans-Black","font-size":"1.5rem"})),
				dbc.ModalBody(
					[
						html.Div(
							[
								input_session_newcontract(app)
							]
						)
						
					],
					style={"background-color":yellow_light1, "border":"none"}
				),
				dbc.ModalFooter(
					[
						html.Div(dbc.Button("save", id = 'close-edit-assumption-newcontract',outline=True, color="primary", className="mr-1", style={"border-radius":"5rem","width":"10rem"}), style={"margin-right":"16rem"}),
						dbc.Button("reset", id = 'close-edit-assumption-newcontract-2',outline=True, color="dark", className="mr-1", style={"border-radius":"5rem","width":"6rem"}),
						dbc.Button("close", id = 'close-edit-assumption-newcontract-3',outline=True, color="dark", className="mr-1", style={"border-radius":"5rem","width":"6rem"})
					]
				)
				], id = 'modal-edit-assumption-newcontract', size="xl", is_open = False, backdrop = 'static'),
		])


def input_session_newcontract(app):
	return dbc.ListGroup([
		dbc.Row(
			[
				dbc.Col(html.H1("Data Input", style={"color":yellow3, "font-size":"1.2rem","padding-top":"0.8rem", "padding-bottom":"1.5rem"})),
				# dbc.Col(dbc.Button("update data", id = 'update-edit-assumption-newcontract',outline=True, color="dark", className="mr-1", style={"border-radius":"5rem","width":"8rem"}), style={"padding-top":"0.8rem", "padding-bottom":"1.5rem", "padding-left":"1.5rem", "padding-right":"1.5rem"}, width=2),
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
									#value = "Aetna", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									#disabled=True,
									id="input-intake-s1-1-newcontract",
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
									#value = "Medicare", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									#disabled=True,
									id="input-intake-s1-2-newcontract",
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
									#value = "1/1/2022-12/31/2022", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									#disabled=True,
									id="input-intake-s1-3-newcontract",
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
									#value = "Shared Savings and Downside Risk", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									#disabled=True,
									id="input-intake-s1-4-newcontract",
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
									#value = "5%", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									#disabled=True,
									id="input-intake-s1-5-newcontract",
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
						dbc.Row(
									[
										dbc.Col(
											html.Div(
												[
													html.A('Download Template', 
														id = 'download-claim-newcontact',
														href=base_download_url +'downloads/Member and Claim Data Template.xlsx',
														target = "_blank")
												], style={"font-size":"0.8rem","padding-left":"0.8rem"}),
											width=3
											),
										dbc.Col(html.P("then"),width="auto"),
										dbc.Col(
											dcc.Upload(
												id = 'upload-claim-newcontact',
												children = html.Div([
													'Select Related Files to Upload'
													],style={"font-family":"NotoSans-Regular","font-size":"0.8rem","text-decoration":"underline","color":"#1357DD"}),
												style={
													'height': '40px',
													'lineHeight': '40px',
													'borderWidth': '1px',
													'borderStyle': 'dashed',
													'borderRadius': '5px',
													'textAlign': 'center'
													}
												), 
											# width=3
											),
										dbc.Col(
											html.Div(id = 'output-age-upload', style={"text-align":"center","padding":"0.5rem","font-family":"NotoSans-Regular","font-size":"0.6rem"}),
											width=1,
											)
									]
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
									#value = "5%", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									#disabled=True,
									id="input-intake-s2-2-newcontract",
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
									#value = "5%", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									#disabled=True,
									id="input-intake-s2-3-newcontract",
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
						html.Div(
								[
									dbc.Row(
										[
											# dbc.Col(
											# 	html.Div(
											# 		[
											# 			html.A('View Attachment', 
											# 				id = 'download-geo',
											# 				href='http://139.224.186.182:8098/downloads/Geographic Distribution template.xlsx',
											# 				target = "_blank")
											# 		], style={"font-size":"1rem","padding-left":"0.8rem"}
											# 	),
											# 	width=4
											# ),
										dbc.Col(
											dcc.Upload(
												id = 'upload-cmp-newcontract',
												children = html.Div([
													'Select Related Files to Upload'
													],style={"font-family":"NotoSans-Regular","font-size":"0.8rem","text-decoration":"underline","color":"#1357DD"}),
												style={
													'height': '40px',
													'lineHeight': '40px',
													'borderWidth': '1px',
													'borderStyle': 'dashed',
													'borderRadius': '5px',
													'textAlign': 'center'
													}
												), 
											# width = 3
											),
										dbc.Col(
											html.Div(id = 'output-cmp-newcontract', style={"text-align":"center","padding":"0.5rem","font-family":"NotoSans-Regular","font-size":"0.6rem"}),
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
						html.Div(
								[
									dbc.Row(
										[
											# dbc.Col(
											# 	html.Div(
											# 		[
											# 			html.A('View Attachment', 
											# 				id = 'download-geo',
											# 				href='http://139.224.186.182:8098/downloads/Geographic Distribution template.xlsx',
											# 				target = "_blank")
											# 		], style={"font-size":"1rem","padding-left":"0.8rem"}
											# 	),
											# 	width=4
											# ),
										dbc.Col(
											dcc.Upload(
												id = 'upload-excl-newcontract',
												children = html.Div([
													'Select Related Files to Upload'
													],style={"font-family":"NotoSans-Regular","font-size":"0.8rem","text-decoration":"underline","color":"#1357DD"}),
												style={
													'height': '40px',
													'lineHeight': '40px',
													'borderWidth': '1px',
													'borderStyle': 'dashed',
													'borderRadius': '5px',
													'textAlign': 'center'
													}
												), 
											# width = 3
											),
										dbc.Col(
											html.Div(id = 'output-excl-newcontract', style={"text-align":"center","padding":"0.5rem","font-family":"NotoSans-Regular","font-size":"0.6rem"}),
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
						html.H3("2. Payor’s contract term", style={"font-size":"1rem"}),
						html.Div(
								[
									dbc.Row(
										[
											# dbc.Col(
											# 	html.Div(
											# 		[
											# 			html.A('View Attachment', 
											# 				id = 'download-geo',
											# 				href='http://139.224.186.182:8098/downloads/Geographic Distribution template.xlsx',
											# 				target = "_blank")
											# 		], style={"font-size":"1rem","padding-left":"0.8rem"}
											# 	),
											# 	width=4
											# ),
										dbc.Col(
											dcc.Upload(
												id = 'upload-term-newcontract',
												children = html.Div([
													'Select Related Files to Upload'
													],style={"font-family":"NotoSans-Regular","font-size":"0.8rem","text-decoration":"underline","color":"#1357DD"}),
												style={
													'height': '40px',
													'lineHeight': '40px',
													'borderWidth': '1px',
													'borderStyle': 'dashed',
													'borderRadius': '5px',
													'textAlign': 'center'
													}
												), 
											# width = 3
											),
										dbc.Col(
											html.Div(id = 'output-term-newcontract', style={"text-align":"center","padding":"0.5rem","font-family":"NotoSans-Regular","font-size":"0.6rem"}),
											width=1
											)
										]
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
						html.H3("3. Payor’s quality metrics", style={"font-size":"1rem"}),
						html.Div(
								[
									dbc.Row(
										[
											# dbc.Col(
											# 	html.Div(
											# 		[
											# 			html.A('View Attachment', 
											# 				id = 'download-geo',
											# 				href='http://139.224.186.182:8098/downloads/Geographic Distribution template.xlsx',
											# 				target = "_blank")
											# 		], style={"font-size":"1rem","padding-left":"0.8rem"}
											# 	),
											# 	width=4
											# ),
										dbc.Col(
											dcc.Upload(
												id = 'upload-quality-newcontract',
												children = html.Div([
													'Select Related Files to Upload'
													],style={"font-family":"NotoSans-Regular","font-size":"0.8rem","text-decoration":"underline","color":"#1357DD"}),
												style={
													'height': '40px',
													'lineHeight': '40px',
													'borderWidth': '1px',
													'borderStyle': 'dashed',
													'borderRadius': '5px',
													'textAlign': 'center'
													}
												), 
											# width = 3
											),
										dbc.Col(
											html.Div(id = 'output-quality-newcontract', style={"text-align":"center","padding":"0.5rem","font-family":"NotoSans-Regular","font-size":"0.6rem"}),
											width=1
											)
										]
									)
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
									#value = "5%", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									#disabled=True,
									id="input-intake-s3-1-newcontract",
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
