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

def modal_simulation_input():
	return html.Div([
		dbc.Button("Data Intake", id = 'button-edit-assumption',outline=True, color="light", className="mr-1", style={"border-radius":"5rem"}),
			dbc.Modal([
				dbc.ModalHeader(html.H1("Data Intake", style={"font-family":"NotoSans-Black","font-size":"1.5rem"})),
				dbc.ModalBody([
					input_session(),
					]),
				dbc.ModalFooter(
					dbc.Button("SAVE", id = 'close-edit-assumption')
					)
				], id = 'modal-edit-assumption', size="xl", is_open = False, backdrop = 'static'),
		])

def input_session(app):
	return dbc.ListGroup([
		dbc.Row(
			[
				dbc.Col(html.H1("Client Data Input", style={"color":yellow3, "font-size":"1.2rem","padding-top":"0.8rem", "padding-bottom":"1.5rem"})),
				dbc.Col(dbc.Button("update data", id = 'update-edit-assumption-pharmacy',outline=True, color="dark", className="mr-1", style={"border-radius":"5rem","width":"8rem"}), style={"padding-top":"0.8rem", "padding-bottom":"1.5rem", "padding-left":"1.5rem", "padding-right":"1.5rem"}, width=2),
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
						html.H3("1. Company", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "Pfizer", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s1-1-pharmacy",
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
						html.H3("2. Drug", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "Drug B", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s1-2-pharmacy",
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
						html.H3("3. Indication", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "Heart Failure", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s1-3-pharmacy",
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
						html.H3("4. LOB", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "Medicare", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s1-4-pharmacy",
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
						html.H3("5. Payor", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "Aetna", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s1-5-pharmacy",
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
						html.H3("6. Plan Name", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "Plan B", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s1-6-pharmacy",
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
						html.H3("7. Contract Period", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "1/1/2022-12/31/2022", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s1-7-pharmacy",
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
						html.H3("8. Plan Benefit Type", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "Medical and Pharmacy", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s1-8-pharmacy",
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
						html.H3("9. Drug Coverage Type", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "Under Medical Benefit", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s1-9-pharmacy",
									style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}
									)
							],
							style={"padding":"1rem"}
						),
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"1rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
					# width=6,
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
				dbc.Col(html.H2("Plan Membership Information", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
			],
			no_gutters=True,
			style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		),
		dbc.Row(
			[
				dbc.Col(
					[
						html.H3("1. Total Members", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "150,000", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s2-1-pharmacy",
									style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})
							],
							style={"padding":"1rem"}
						),
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"0.8rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
					# width=4,
				),
				dbc.Col(
					[
						html.H3("2. Gender Distribution", style={"font-size":"1rem"}),
						dbc.Row(
							[
								dbc.Col(html.P("Expand"), width="auto"),
								dbc.Col(dbc.Button("\u25BC", size="sm", color='primary', style={"border-radius":"10rem"}, block=True, id = 'button-data-intake-collapse-gender-pharmacy'), width=4)
								
							],
							style={"padding":"1rem"}
						),
						html.Div(
							dbc.Collapse(
								[
									card_collapse_gender_pharmacy()
									
								],id = 'data-intake-collapse-gender-pharmacy', is_open = False,
							), style={"padding-right":"0rem"}
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
						html.H3("3. Age Distribution", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Row(
									[
										dbc.Col(
											[
												# html.H1("OPTION 1:", style={"font-size":"0.8rem"}),
												dbc.Row(
													[
														dbc.Col(html.P("Expand"), width="auto"),
														dbc.Col(dbc.Button("\u25BC", id = 'button-data-intake-collapse-age-pharmacy', size="sm", color='primary', style={"border-radius":"10rem"}, block=True), width=5),
													]
												),
												
											], 
											style={"margin-left":"1rem","margin-right":"1rem","padding":"0.8rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
											width=5
											),
										# dbc.Col(
										# 	[
										# 		html.H1("OPTION 2:", style={"font-size":"0.8rem"}),
										# 		dbc.Row(
										# 			[
										# 				dbc.Col(
										# 					html.Div(
										# 						[
										# 							html.A('Download Template', 
										# 								
										# 								href='http://139.224.186.182:8098/downloads/Age Distribution template.xlsx',
										# 								target = "_blank")
										# 						], style={"font-size":"0.8rem","padding-left":"0.8rem"}),
										# 					width=3
										# 					),
										# 				dbc.Col(html.P("then"),width="auto"),
										# 				dbc.Col(
										# 					dcc.Upload(
										# 						id = 'upload-age',
										# 						children = html.Div([
										# 							'Select Related Files to Upload'
										# 							],style={"font-family":"NotoSans-Regular","font-size":"0.8rem","text-decoration":"underline","color":"#1357DD"}),
										# 						style={
										# 							'height': '40px',
										# 							'lineHeight': '40px',
										# 							'borderWidth': '1px',
										# 							'borderStyle': 'dashed',
										# 							'borderRadius': '5px',
										# 							'textAlign': 'center'
										# 							}
										# 						), 
										# 					# width=3
										# 					),
										# 				dbc.Col(
										# 					html.Div(id = 'output-age-upload', style={"text-align":"center","padding":"0.5rem","font-family":"NotoSans-Regular","font-size":"0.6rem"}),
										# 					width=1,
										# 					)
										# 			]
										# 		), 
										# 	],
										# 	style={"margin-left":"1rem","margin-right":"1rem","padding":"0.8rem", "background-color":yellow2, "border":"none", "border-radius":"0.5rem"},
										# ),
									]
								),
								html.Div(
									dbc.Collapse(
										[
											card_collapse_age_pharmacy()
										],
										id = 'data-intake-collapse-age-pharmacy', is_open = False,
									), style={"padding-right":"30rem"}
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


		dbc.Row(
			[
				dbc.Col(
					html.Div(
						[
							html.H3("4. Geography Distribution", style={"font-size":"1rem"}),
							html.Div(
								[
									dbc.Row(
										[
											dbc.Col(
												html.Div(
													[
														html.A('View Attachment', 
															id = 'download-geo',
															href='http://139.224.186.182:8098/downloads/Geographic Distribution template.xlsx',
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
											html.Div(id = 'output-geo-upload', style={"text-align":"center","padding":"0.5rem","font-family":"NotoSans-Regular","font-size":"0.6rem"}),
											width=1
											)
										]
									)
								],
								style={"padding":"1rem"}
							),
						],
						style={"padding":"0.8rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"}
					),
					# width=4,
				),
				dbc.Col(
					[
						html.H3("5. Prevalence Rate of Target Indication", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "13%", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s2-5-pharmacy",
									style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})
							],
							style={"padding":"1rem"}
						),
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"1rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
					# width=6,
				),
			],
			style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		),


		dbc.Row(
			[
				dbc.Col(
					[
						html.H3("6.Benefit Design", style={"font-size":"1rem"}),
						# dbc.Row(
						# 	[
						# 		dbc.Col(html.P("click to open"), width="auto"),
						# 		dbc.Col(dbc.Button("\u25BC", size="sm", color='primary', style={"border-radius":"10rem"}, id = 'button-data-intake-collapse-benefit-pharmacy', block=True), width=2),
						# 		dbc.Col()
						# 	],
						# 	style={"padding":"1rem"}
						# ),
						dbc.Col(
							html.Div(
								[
									html.A('View Attachment', 
										
										href='http://139.224.186.182:8098/downloads/Age Distribution template.xlsx',
										target = "_blank")
								], style={"font-size":"1rem","padding-left":"0.8rem"}
							),
							width=3,
							style={"padding":"1rem"}
						),
						# html.Div(
						# 	dbc.Collapse(
						# 		[
						# 			card_collapse_tier_pharmacy()
						# 		],
						# 		id = 'data-intake-collapse-benefit-pharmacy', 
						# 		is_open = False,
						# 		# style={"padding":"1rem","border-radius":"0.5rem","background-color":"#f5f5f5"}
						# 	), style={"padding":"0.5rem"}
						# ),
					], 
					style={"margin-left":"1rem","margin-right":"1rem","padding":"1rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
					# width=6,
				),
				# dbc.Col(
				# ),
			],
			style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		),


		html.Hr(),

		dbc.Row(
			[
				dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
				dbc.Col(html.H2("PLan Cost and Utilization", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
			],
			no_gutters=True,
			style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		),
		dbc.Row(
			[
				dbc.Col(
					[
						html.H3("1. Historical Cost and Utilization for Patients with Target Indications", style={"font-size":"1rem"}),
						dbc.Row(
							[
								dbc.Col(
									html.Div(
										[
											html.A('View Attachment', 
												
												href='http://139.224.186.182:8098/downloads/Age Distribution template.xlsx',
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
						html.H3("2. Historical Trend Rates for Patients with Target Indications", style={"font-size":"1rem"}),
						dbc.Row(
							[
								dbc.Col(
									html.Div(
										[
											html.A('View Attachment', 
												
												href='http://139.224.186.182:8098/downloads/Age Distribution template.xlsx',
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
				dbc.Col(html.H2("Drug Information", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
			],
			no_gutters=True,
			style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		),
		dbc.Row(
			[
				dbc.Col(
					[
						html.H3("1. Pricing Info (WAC)", style={"font-size":"1rem"}),
						dbc.Row(
							[
								dbc.Col(
									dbc.Input(
										value = "$9.6 / unit (tablet)", 
										bs_size="sm", 
										persistence = True, 
										persistence_type = 'session', 
										disabled=True,
										id="input-intake-s4-1-pharmacy",
										style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}
									)
								),
								# dbc.Col(
								# 		dcc.Upload(
								# 			id = 'upload-price',
								# 			children = html.Div([
								# 				'Select Related Files to Upload'
								# 				],style={"font-family":"NotoSans-Regular","font-size":"0.8rem","text-decoration":"underline","color":"#1357DD"}),
								# 			style={
								# 				'height': '40px',
								# 				'lineHeight': '40px',
								# 				'borderWidth': '1px',
								# 				'borderStyle': 'dashed',
								# 				'borderRadius': '5px',
								# 				'textAlign': 'center'
								# 				}
								# 			), 
								# 		# width = 3
								# 		),
								dbc.Col(
									html.Div(id = 'output-price-upload', style={"text-align":"center","padding":"0.5rem","font-family":"NotoSans-Regular","font-size":"0.6rem"}),
									width=1
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
						html.H3("2. Market Basket Definition", style={"font-size":"1rem"}),
						html.Div(
							[
								dbc.Input(
									value = "ACE, ARB", 
									bs_size="sm", 
									persistence = True, 
									persistence_type = 'session', 
									disabled=True,
									id="input-intake-s4-2-pharmacy",
									style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}
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
		# dbc.Row(
		# 	[
		# 		dbc.Col(
		# 			[
		# 				html.H3("3. Market Basket Definition", style={"font-size":"1rem"}),
		# 				html.Div(
		# 					[
		# 						dbc.Input(
		# 							value = "ACE, ARB", 
		# 							bs_size="sm", 
		# 							persistence = True, 
		# 							persistence_type = 'session', 
		# 							style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})
		# 					],
		# 					style={"padding":"1rem"}
		# 				),
		# 			], 
		# 			style={"margin-left":"1rem","margin-right":"1rem","padding":"1rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
		# 			# width=4,
		# 		),
		# 		dbc.Col(
		# 			[
						
		# 			], 
		# 			style={"margin-left":"1rem","margin-right":"1rem","padding":"1rem", "background-color":yellow_light1, "border":"none", "border-radius":"0.5rem"},
		# 			# width=6,
		# 		),
		# 	],
		# 	style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		# ),



		html.Hr(),
		dbc.Row(
			[
				dbc.Col(html.Img(src=app.get_asset_url("bullet-round-blue.png"), width="10px"), width="auto", align="start", style={"margin-top":"-4px"}),
				dbc.Col(html.H2("Contract Information", style={"font-size":"1rem", "margin-left":"10px"}), width=8),
			],
			no_gutters=True,
			style={"padding-left":"1.5rem", "padding-right":"1.5rem", "padding-bottom":"1.5rem"}
		),
		html.Div(
			[
				html.Div([
					dbc.Row([
						dbc.Col(width=6),
						dbc.Col("Contract without VBC:", style={"font-style":"italic"}, width=3),
						dbc.Col("Contract with VBC:", style={"font-style":"italic"}, width=3),
						], style={"padding-top":"0.5rem"}),
					], style={"padding-left":"1rem", "padding-right":"1rem", "padding-top":"1rem"}),
				html.Div([
					dbc.Row(
						[
							dbc.Col('Expected Formulary Tier', style={"font-size":"0.8rem", "margin-top":"0.3rem"}, width=6),
							dbc.Col(
								[
									dbc.InputGroup(
										[
											dbc.Input( 
												value = "Non-Preferred",
												persistence = True,
												persistence_type = 'session',
												disabled = True,
												id="input-intake-s5-1wo-pharmacy",
												style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}
											)
										], size="sm"
									)
								], width=3
							),
							dbc.Col(
								[
									dbc.InputGroup(
										[
											dbc.Input( 
												value = "Preferred",
												persistence = True,
												persistence_type = 'session',
												disabled = True,
												id="input-intake-s5-1w-pharmacy",
												style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}
											)
										], size="sm"
									)
								], width=3
							),
						], style={"padding-top":"0.5rem"}
					),
					dbc.Row(
						[
							dbc.Col('Rebate', style={"font-size":"0.8rem", "margin-top":"0.3rem"}, width=6),
							dbc.Col(
								[
									dbc.InputGroup(
										[
											dbc.Input( 
												value = "10%",
												persistence = True,
												persistence_type = 'session',
												disabled = True,
												id="input-intake-s5-2wo-pharmacy",
												style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}
											)
										], size="sm"
									)
								], width=3
							),
							dbc.Col(
								[
									dbc.InputGroup(
										[
											dbc.Input( 
												value = "10%",
												persistence = True,
												persistence_type = 'session',
												disabled = True,
												id="input-intake-s5-2w-pharmacy",
												style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}
											)
										], size="sm"
									)
								], width=3
							),
						], style={"padding-top":"0.5rem"}
					),

					dbc.Row(
						[
							dbc.Col('Clinical Trial Results', style={"font-size":"0.8rem", "margin-top":"0.3rem"}, width=6),
							dbc.Col(
								width=3
							),
							dbc.Col(
								html.Div(
									[
										html.A('View Attachment', 
											
											href='http://139.224.186.182:8098/downloads/Age Distribution template.xlsx',
											target = "_blank")
									], style={"font-size":"0.8rem","padding":"0.5rem"}
								),
								width=3
							),
							# dbc.Col(
							# 	[
							# 		dbc.InputGroup(
							# 			[
							# 				dbc.Input( 
							# 					value = "40%",
							# 					persistence = True,
							# 					persistence_type = 'session',
							# 					disabled = True,
							# 					style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}
							# 				)
							# 			], size="sm"
							# 		)
							# 	], width=3
							# ),
						], style={"padding-top":"0.5rem"}
					),
					
					dbc.Row(
						[
							dbc.Col('Projected Drug B Market Share', style={"font-size":"0.8rem", "margin-top":"0.3rem"}, width=6),
							dbc.Col(
								[
									dbc.InputGroup(
										[
											dbc.Input( 
												value = "2%",
												persistence = True,
												persistence_type = 'session',
												disabled = True,
												id="input-intake-s5-4wo-pharmacy",
												style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}
											)
										], size="sm"
									)
								], width=3
							),
							dbc.Col(
								[
									dbc.InputGroup(
										[
											dbc.Input( 
												value = "10%",
												persistence = True,
												persistence_type = 'session',
												disabled = True,
												id="input-intake-s5-4w-pharmacy",
												style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}
											)
										], size="sm"
									)
								], width=3
							),
						], style={"padding-top":"0.5rem"}
					),

					

					dbc.Row([
						dbc.Col('Drug B Market Share Monthly Ramp Up Rate (M1-M12)', style={"font-size":"0.8rem", "margin-top":"0.3rem"}, width=6),
						dbc.Col(
							dbc.Button("\u25BC", size="sm", color='primary', style={"border-radius":"10rem"}, id = 'button-data-intake-collapse-month-pharmacy', block=True),
							)
						], style={"padding-top":"0.5rem"}),
					
					html.Div(
						dbc.Row(
							[
								dbc.Col(width=4),
								dbc.Col(
									dbc.Collapse(
										[
											card_data_intake_collapse_rampup_pharmacy()
										],
										id = 'data-intake-collapse-month-pharmacy', 
										is_open = False,
										style={"padding":"0rem","border-radius":"0.5rem","background-color":"#f5f5f5", "box-shadow":".5rem .5rem 2rem #A9A9A9"}
									),
								),
							]
						),
						style={"padding-top":"1rem","padding-bottom":"1rem", "margin-right":"-1rem"}
					),

				], style={"padding-left":"1rem", "padding-right":"1rem", "padding-top":"1rem"}),
			], 
			style={"margin-left":"1rem","margin-right":"1rem", "padding":"1rem", "background-color":"#fff", "border":"none", "border-radius":"0.5rem"},
		),



		],
		style={"border-radius":"0.5rem"})

def card_collapse_age_pharmacy():
	return dbc.Card(
			[
				dbc.Row([
					dbc.Col(html.H2("AGE BAND", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
					dbc.Col(html.H2("MEMBER %", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
					], style={"padding-top":"1rem"}),
				html.Hr(),
				dbc.Row([
					dbc.Col("Newborn (0-1m)", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "0.0%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("1m-2y", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "0.0%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("2-12", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "0.0%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("12-17", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "0.0%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("18-24", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "0.2%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("25-34", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "0.4%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("35-44", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "1.0%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("45-54", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "1.6%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("55-64", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "1.8%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("65-74", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "18%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("75-84", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "44%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col(">=85", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "33%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
			], style={"font-family":"NotoSans-Regular","font-size":"1rem","margin-top":"2rem", "padding":"2rem","border-radius":"0.5rem", "box-shadow":".5rem .5rem 2rem "+grey2}
		)

def card_collapse_gender_pharmacy():
	return dbc.Card([
				dbc.Row([
					dbc.Col(html.H2("GENDER", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
					dbc.Col(html.H2("MEMBER %", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
					], style={"padding-top":"1rem"}),
				html.Hr(),
				dbc.Row([
					dbc.Col("Female", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "53%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("Male", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "47%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				], style={"font-family":"NotoSans-Regular","font-size":"1rem","margin-top":"2rem", "padding":"2rem","border-radius":"0.5rem", "box-shadow":".5rem .5rem 2rem "+grey2})


def card_collapse_tier_pharmacy():
	return dbc.Card(
			[
				dbc.Row([
					dbc.Col(html.H2("Tier", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
					dbc.Col(html.H2("Days of Supply", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
					dbc.Col(html.H2("Copay", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
					dbc.Col(html.H2("Coinsurance", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
					dbc.Col(html.H2("Max Copay", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
					], style={"padding-top":"1rem"}),
				html.Hr(),
				dbc.Row(
					[
						dbc.Col("Tier 1", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
						dbc.Col("30",style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
						dbc.Col(dbc.Input(value = "$5", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
					], style={"padding-top":"1rem"}
				),
				dbc.Row(
					[
						dbc.Col("Tier 1", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
						dbc.Col("90", style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
						dbc.Col(dbc.Input(value = "$10", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
					], style={"padding-top":"1rem"}
				),
				dbc.Row(
					[
						dbc.Col("Tier 2", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
						dbc.Col("30", style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
						dbc.Col(dbc.Input(value = "$10", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
					], style={"padding-top":"1rem"}
				),
				dbc.Row(
					[
						dbc.Col("Tier 2", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
						dbc.Col("90", style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
						dbc.Col(dbc.Input(value = "$20", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
					], style={"padding-top":"1rem"}
				),
				dbc.Row(
					[
						dbc.Col("Tier 3", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
						dbc.Col("30", style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
						dbc.Col(dbc.Input(value = "$40",bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
					], style={"padding-top":"1rem"}
				),
				dbc.Row(
					[
						dbc.Col("Tier 3", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
						dbc.Col("90", style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
						dbc.Col(dbc.Input(value = "$100",bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
					], style={"padding-top":"1rem"}
				),
				dbc.Row(
					[
						dbc.Col("Tier 4", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
						dbc.Col("30", style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
						dbc.Col(dbc.Input(value = "$70",bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
					], style={"padding-top":"1rem"}
				),
				dbc.Row(
					[
						dbc.Col("Tier 4", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
						dbc.Col("90", style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
						dbc.Col(dbc.Input(value = "$150",bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
					], style={"padding-top":"1rem"}
				),
				dbc.Row(
					[
						dbc.Col("Tier 5", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
						dbc.Col("30", style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(value = "20%",bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(value = "$200",bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
					], style={"padding-top":"1rem"}
				),
				dbc.Row(
					[
						dbc.Col("Tier 5", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
						dbc.Col("90", style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}),
						dbc.Col(dbc.Input(bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(value = "20%",bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
						dbc.Col(dbc.Input(value = "$400",bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
					], style={"padding-top":"1rem"}
				),
				dbc.Row(
					[
						dbc.Col("Maximum OOP per Individual", style={"font-family":"NotoSans-Regular","font-size":"1rem"}),
						dbc.Col(dbc.Input(value = '$2800', bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"})),
					], style={"padding-top":"1rem"}
				),
			],
			style={"font-family":"NotoSans-Regular","font-size":"1rem","margin-top":"2rem", "padding":"2rem","border-radius":"0.5rem", "box-shadow":".5rem .5rem 2rem "+grey2}
		)



def card_collapse_month_pharmacy():
	return dbc.Card(
			[
				dbc.Row([
					dbc.Col(html.H2("MONTH", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
					dbc.Col(html.H2("RAMP UP", style={"font-size":"1.2rem", "margin-left":"10px", "color":yellow3})),
					], style={"padding-top":"1rem"}),
				html.Hr(),
				dbc.Row([
					dbc.Col("Month 1", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "2%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("Month 2", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "3%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("Month 3", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "4%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("Month 4", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "5%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("Month 5", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "6%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("Month 6", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "7%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("Month 7", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "7%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("Month 8", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "7%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("Month 9", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "7%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("Month 10", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "7%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("Month 11", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "7%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
				dbc.Row([
					dbc.Col("Month 12", style={"font-family":"NotoSans-Regular","font-size":"0.8rem"}),
					dbc.Col(dbc.Input(value = "7%", bs_size="sm", persistence = True, persistence_type = 'session', style={"border-radius":"5rem","padding-left":"1rem","padding-right":"1rem","color":"#000","font-family":"NotoSans-Regular"}))
					], style={"padding-top":"1rem"}),
			], style={"font-family":"NotoSans-Regular","font-size":"1rem","margin-top":"2rem", "padding":"2rem","border-radius":"0.5rem", "box-shadow":".5rem .5rem 2rem "+grey2}
		)

def download_template_pharmacy():
	return html.A(
				"Download the template file",
				id = 'download-link',
				href='http://139.224.186.182:8098/downloads/Pharma Value-Based Measures Template.xlsx',
				target = "_blank"
			)


def card_data_intake_collapse_rampup_pharmacy():
	cardbody = [dbc.Row([
					dbc.Col(html.H2("MONTHLY RAMPUP", style={"font-size":"0.8rem", "margin-left":"10px"}), width=6),
					# dbc.Col(html.H2("RAMP UP", style={"font-size":"1rem", "margin-left":"10px"})),
					], style={"padding":"0.5rem","padding-left":"3rem"}),]
	

	for i in range(12):
		if i%2 == 1:
			extra_style = {"padding":"0.5rem", "padding-left":"3.5rem","background-color":"#f1f1f1", "border":"none", "border-radius":"0rem"}
		else:
			extra_style = {"padding":"0.5rem","padding-left":"3.5rem"}
		cardbody.append(dbc.Row([
			dbc.Col("Month {}".format(i+1), style={"font-family":"NotoSans-Regular","font-size":"0.8rem","margin-top":"0.2rem"}, width=2),
			dbc.Col(
				dbc.InputGroup([
				dbc.Input(
					value = 2, 
					type = 'number',
					bs_size="sm", 
					persistence = True, 
					persistence_type = 'session', 
					disabled = True,
					style={"color":"#000","font-family":"NotoSans-Regular"}
				),
				dbc.InputGroupAddon('%', addon_type = 'append')], size="sm"),
				width=5
				),
			dbc.Col(
				dbc.InputGroup([
				dbc.Input(
					value = 10, 
					type = 'number',
					bs_size="sm", 
					persistence = True, 
					persistence_type = 'session', 
					disabled = True,
					style={"color":"#000","font-family":"NotoSans-Regular"}
				),
				dbc.InputGroupAddon('%', addon_type = 'append')], size="sm"),
				width=5,
				)
			], style=extra_style),)
	return dbc.Card(
			cardbody
			, style={"font-family":"NotoSans-Regular","font-size":"1rem", "padding":"1rem"}
		)
