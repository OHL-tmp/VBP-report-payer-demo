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

from dash.dependencies import Input, Output, State

from utils import *
from app import app


# app = dash.Dash(__name__, url_base_pathname='/vbc-payer-demo/contract-generator/')

# server = app.server


df_quality = pd.read_csv("data/quality_setup.csv")
df_bundle_measure=pd.read_csv("data/bundle_measure_setup2.csv")
df_bundle=pd.read_csv("data/df_bundles_90.csv")

def create_layout(app):
	
	return html.Div(
                [ 
                    html.Div([Header_contract(app, False, False, True, False)], style={"height":"6rem"}, className = "sticky-top navbar-expand-lg"),
                    html.Div(dbc.Button('Back to Simulation',href = "/vbc-demo/contract-optimizer-bundle/", style={"text-align":"center", "font-size":"0.8rem", "border":"1px dashed #919191"}, color="light"), style={"text-align":"start", "width":"850px", "margin":"auto","padding-bottom":"2rem"}),
	                
                    html.Div(
                    	html.Div(
	                        [
	                        	html.H1("Contract Generator", style={"padding-left":"20px","padding-bottom":"30px"}),
		                        contract_gen_basic(app),
		                        html.Div(style={"height":"20px"}),
		                        contract_gen_parameter(app),
		                        html.Div(style={"height":"40px"}),
		                        contract_gen_measure(app),
		                        html.Div(style={"height":"20px"}),
								html.Div(
									[
										html.H1("Upload Contract Template", style={"font-size":"1.25rem"}),
										html.Hr(),
										dcc.Upload(
											id = 'upload-data',
											children = html.Div([
												'Select Contract Template to Upload'
												],style={"font-family":"NotoSans-Regular","font-size":"1rem","text-decoration":"underline","color":"#1357DD"}),
											style={
												'height': '60px',
												'lineHeight': '60px',
												'borderWidth': '1px',
												'borderStyle': 'dashed',
												'borderRadius': '5px',
												'textAlign': 'center',
												'margin': '10px'
												}
										)
									],
									style={"padding":"20px","background-color":"#f2f7ff"}
								),
								html.Div(style={"height":"20px"}),
								html.Div(dbc.Button('Generate Contract', style={"text-align":"center", "background-color":"#381610", "border-radius":"10rem"}), style={"padding-bottom":"40px", "text-align":"center"}),
								
							]      
	                        
	                    ),
                        className="mb-3",
                    	style={"box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)","background-color":"#fff","padding":"20px","padding-bottom":"0rem", "width":"850px", "margin":"auto"},
                    )
                    
                ])



def contract_gen_basic(app):
	df = df_bundle[(df_bundle['Bundle'].isin(['Major joint replacement of the lower extremity (MJRLE)', 'Stroke', 'Acute myocardial infarction', 'Congestive heart failure'])) & (df_bundle['IP/OP'] == 'Inpatient')]
	return html.Div([
		html.Div(
			[
				html.H1("Bundle Selection & Target Price", style={"font-size":"1.25rem"}),
				html.Hr(),
				dbc.Row([
					dbc.Col('BS1. Bundle Length', width=7),
					dbc.Col([
						dcc.Dropdown(options = [{'label':'90D', 'value':'90D'},{'label':'60D', 'value':'60D'},{'label':'30D', 'value':'30D'}],
							value = '90D',
							style={"font-size":"0.8rem"}
							)
						], width=5)
					],
					style={"padding-bottom":"10px"}),
				dbc.Row([
					dbc.Col("BS2. ", width=7),
					]),
				html.Div([
					dash_table.DataTable(
						data = df.to_dict('records'),
						columns = [{'name':'IP/OP', 'id':'IP/OP'},{'name':'Bundle', 'id':'Bundle'},{'name':'Recommended Target', 'id':'Recommended Target'} ],
						style_data = {'textAlign' : 'center','font-family': 'NotoSans-CondensedLight',"font-size":"0.85rem"},
						style_header = {'backgroundColor': '#f1f6ff',
						'fontWeight': 'bold',
						'font-family':'NotoSans-CondensedLight',
						'fontSize':14,
						'color': '#1357DD',
						'text-align':'center',
						'border':'1px solid grey'},
						style_as_list_view=True,
									),
					])
			]
		),
		
		],
		style={"padding":"20px"})




def contract_gen_parameter(app):
	return html.Div([
		html.Div(
			[
			html.H1("Quality Adjustment", style={"font-size":"1.25rem"}),
			html.Hr(),
			dbc.Row([
				dbc.Col(html.H6('QA1. Maximum Adjustment on Positive Reconciliation Amount', style={"font-size":"1rem"}), width=7),
				dbc.Col([
					dbc.InputGroup([
						dbc.Input(value = 10), 
						dbc.InputGroupAddon('%', addon_type = 'append'),
						], size="sm"),
					], width=2)
				],
				style={"padding-bottom":"10px"}),
			dbc.Row([
				dbc.Col(html.H6('QA2. Maximum Adjustment on Negative Reconciliation Amount', style={"font-size":"1rem"}), width=7),
				dbc.Col([
					dbc.InputGroup([
						dbc.Input(value = 10), 
						dbc.InputGroupAddon('%', addon_type = 'append'),
						], size="sm"),
					], width=2)
				],
				style={"padding-bottom":"10px"}),
			],
			style={"padding":"20px","background-color":"#f2f7ff"}
		),
		
		html.Div(style={"height":"20px"}),

		html.Div(
			[
				dbc.Row([
					dbc.Col('QA3. Quality Measures', width=7),
					],
					style={"padding-bottom":"10px"}),
				html.Div([
					dash_table.DataTable(
						data = df_bundle_measure.to_dict('records'),
						columns = [{'name':'Measure', 'id':'Measure'},{'name':'Applicable Episodes', 'id':'Applicable Episodes'},{'name':'Recommended Target', 'id':'recommended'}],
						style_data = {'textAlign' : 'center','font-family': 'NotoSans-CondensedLight',"font-size":"0.85rem",'height':'auto','width':'4rem','whiteSpace':'normal'},
						style_header = {'backgroundColor': '#f1f6ff',
						'fontWeight': 'bold',
						'font-family':'NotoSans-CondensedLight',
						'fontSize':14,
						'color': '#1357DD',
						'text-align':'center',
						'border':'1px solid grey'},
						style_cell_conditional = [{'if': {'column_id': 'Measure'}, 'width': '50%'}],
						style_as_list_view=True,
						),
					],
					style={"padding-bottom":"10px"}),
			],
			style={"padding":"20px"}
		),

		],
		style={"font-family":"NotoSans-Regular"}
	)


def contract_gen_measure(app):
	return html.Div([
		html.H1("Stop-Loss/Stop-Gain", style={"font-size":"1.25rem"}),
		html.Hr(),
		dbc.Row([
			dbc.Col('SS1. Stop Loss'),
			dbc.Col(
			dbc.InputGroup([
				dbc.Input(value= 20),
				dbc.InputGroupAddon('%', addon_type = 'append')
				], size="sm"),
				width=2
			),
			],
			style={"padding-bottom":"10px"}),
		dbc.Row([
			dbc.Col('SS2. Stop Gain'),
			dbc.Col(
			dbc.InputGroup([
				dbc.Input(value= 20),
				dbc.InputGroupAddon('%', addon_type = 'append')
				], size="sm"),
				width=2
			)
			],
			style={"padding-bottom":"10px"}),
		
		],
		style={"padding":"20px","background-color":"#f2f7ff"})
	

layout = create_layout(app)

if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True,port=8052)