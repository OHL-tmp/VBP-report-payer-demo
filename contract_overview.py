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

from dash.dependencies import Input, Output, State, MATCH, ALL

from app import app
from assets.color import *
from modal_simulation_input_newcontract import *

# app = dash.Dash(__name__, url_base_pathname='/vbc-demo/')

# server = app.server


df_contract_overview = pd.read_csv('data/df_contract_overview.csv')

def create_layout(app):
	return html.Div(
			[
				dbc.Card(
					[
						contract_overview_metrics(app),
						contract_list(),     
					],
				)
			],
			style={"padding-top":"1rem","background-color":"#fff"}
		)


def contract_overview_metrics(app):
	return html.Div(
				html.Div(
					[
						html.Div(
							html.H1("Contract Overview", style={"font-size":"2rem","color":"#000"}),
							style={"text-align":"start","padding-bottom":"0rem"},
						),
						html.Div(
							[
								contract_overview_metrics_block("Total Number of Payors", "2", blue2, blue3),
								contract_overview_metrics_block("Total Number of Contracts", "2", blue2, blue3),
								contract_overview_metrics_block("% of Total Revenue", "10%", blue2, blue3),
								
							], 
							style={"display":"flex", "padding-left":"6rem"}
						),
						html.Div(
							[
								html.H3("Contract count by status:", style={"font-size":"1rem"})
							],
							style={"margin-top":"1rem","padding-left":"6rem"}
						),
						html.Div(
							[
								contract_overview_metrics_block("data incomplete", "0", grey2, grey3),
								contract_overview_metrics_block("under Customization", "0", grey2, grey3),
								contract_overview_metrics_block("Ready for Design", "2", yellow1, yellow3),
								contract_overview_metrics_block("In Execution", "2", green1, green2),
								
							], 
							style={"display":"flex", "padding-left":"6rem"}
						),
					],
					style={"padding-top":"3rem", "padding-left":"4rem", "padding-bottom":"2rem", "background":"#f5f5f5"}
				)
				
			)

def contract_list():
	return html.Div(
			[

				dbc.Row(
					[
						dbc.Col(html.H1("Contract List", style={"font-size":"2rem","color":"#000"}), width="auto"),
						dbc.Col(modal_simulation_input_newcontract()),
						dbc.Col(),
						
					],
					style={"text-align":"start","padding-bottom":"20px"},
				),
				html.Div(contract_overview_list_header(), style={"display":"flex"}),
				html.Hr(style={"margin-top":"0.5rem"}),
				html.Div(contract_overview_list_content(df_contract_overview), id = 'contract-overview-list-content'),
			],
			style={"padding-left":"4rem","padding-right":"4rem","padding-top":"2rem","text-align":"center","height":"30rem"}
		)

def contract_overview_metrics_block(title, value, color, shadowcolor):
	return html.Div(
				html.Div(
					[
						html.H6(title.upper(), style={"color":"#fff","width":"10rem"}),
						dbc.Badge(value, style={"font-family":"NotoSans-SemiBold","font-size":"1.2rem","border-radius":"10rem","width":"4.5rem","background":"#fff","color":color}),
					],
					style={"border-radius":"0.8rem", "border":"none","background":color,"padding":"0.5rem","box-shadow":"0 4px 8px 0 "+shadowcolor}
				),
				style={"padding":"1rem"}
			)

			
					

def contract_overview_dropdown(df, metrics, dropdown_id, prior_value='All'):

	return dcc.Dropdown(
						id = dropdown_id,
						options = [{'label':i, 'value':i} for i in ['All'] + list(df[metrics].unique())],
						value = prior_value,
						clearable = False,
						persistence = True,
						persistence_type = 'session',
						style={"font-family":"NotoSans-Regular"}
					)


def contract_overview_list_header():
	
	list_header = list(df_contract_overview.columns[:-1])

	# header_div = []
	# for item in  list_header:
	# 	header_div = header_div + [
	# 					dbc.Col(
	# 						html.Div(
	# 							html.H4(item, style={"font-size":"1rem","color":"#919191"})
	# 						),
	# 						width=1
	# 					)]
	payor = html.Div(
					[
						html.H1("Payor", style={"font-size":"0.8rem"}),
						html.Div([contract_overview_dropdown(df_contract_overview, 'Payor', 'contract-overview-dropdown-payor')], id = 'contract-overview-dropdown-container-payor'),
					],
					style={"width":"8rem","padding":"0.5rem"}
				)

	lob = html.Div(
					[
						html.H1("LOB", style={"font-size":"0.8rem"}),
						html.Div([contract_overview_dropdown(df_contract_overview, 'LOB', 'contract-overview-dropdown-lob')], id = 'contract-overview-dropdown-container-lob'),
],
					style={"width":"8rem","padding":"0.5rem"}
				)

	period = html.Div(
					[
						html.H1("Contract Period", style={"font-size":"0.8rem"}),
						html.Div(),
],
					style={"width":"16rem","padding":"0.5rem"}
				)

	contract_type = html.Div(
					[
						html.H1("VBC Contract Type", style={"font-size":"0.8rem"}),
						html.Div([contract_overview_dropdown(df_contract_overview, 'VBC Contract Type', 'contract-overview-dropdown-contract')], id = 'contract-overview-dropdown-container-contract'),
],
					style={"width":"24rem","padding":"0.5rem"}
				)

	revenue = html.Div(
					[
						html.H1("% of Total Revenue", style={"font-size":"0.8rem"}),
						html.Div(),
					],
					style={"width":"6rem","padding":"0.5rem"}
				)

	status = html.Div(
					[
						html.H1("Status", style={"font-size":"0.8rem"}),
						html.Div([contract_overview_dropdown(df_contract_overview, 'Status', 'contract-overview-dropdown-status')], id = 'contract-overview-dropdown-container-status'),
					],
					style={"width":"12rem","padding":"0.5rem"}
				)

	

	header_div = [payor, lob, period, contract_type, revenue, status]

	return header_div

def contract_overview_list_content(df):

	content_div = []
	num_of_rows = len(df)
	num_of_cols = len(df.columns)
	
	for i in range(num_of_rows):

		# row_div = []
		# for j in  range(num_of_cols-1):
		# 	row_div = row_div + [
		# 					dbc.Col(
		# 						html.Div(
		# 							html.H4(df.iloc[i,j], style={"font-size":"1rem","color":"#919191"})
		# 						),
		# 						width=1
		# 					)]
		


		payor = html.Div(
						html.H5(df.iloc[i,0], style={"font-size":"1rem","color":"#919191","padding-top":"0.3rem"}),
						style={"padding":"1rem","width":"8rem"}
					)

		lob = html.Div(
						html.H5(df.iloc[i,1], style={"font-size":"1rem","color":"#919191","padding-top":"0.3rem"}),
						style={"padding":"1rem","width":"8rem"}
					)

		period = html.Div(
						html.H5(df.iloc[i,2], style={"font-size":"1rem","color":"#919191","padding-top":"0.3rem"}),
						style={"padding":"1rem","width":"16rem"}
					)

		contract = html.Div(
						html.H5(df.iloc[i,3], style={"font-size":"1rem","color":"#919191","padding-top":"0.3rem"}),
						style={"padding":"1rem","width":"24rem"}
					)

		revenue = html.Div(
						html.H5(df.iloc[i,4], style={"font-size":"1rem","color":"#919191","padding-top":"0.3rem"}),
						style={"padding":"1rem","width":"6rem"}
					)

		status_text = df.iloc[i,5]
		if status_text == "In Execution":
			color_set = "success"
		else:
			color_set = "warning"
		status = html.Div(
					dbc.Badge(html.H5(status_text, style={"font-size":"0.8rem","color":"#fff","padding-left":"0.5rem","padding-right":"0.5rem"}), color=color_set, className="mr-1",style={"height":"1.5rem"}),
					style={"padding":"1rem","width":"12rem"}
				)

		# drug_coverage = html.Div(
		# 			html.H4(df.iloc[i,7], style={"font-size":"1rem","color":"#919191","padding-top":"0.3rem"}),
		# 				style={"padding":"1rem","width":"16rem"}
		# 		)

		# other = html.Div(
		# 			dbc.Button(
		# 				"Info \u25BC", 
		# 				# href = df.iloc[i,num_of_cols-1], 
		# 				size="sm", 
		# 				color='light', 
		# 				style={"border-radius":"10rem","border":"1px solid "+grey3}, 
		# 				block=True, 
		# 				id="button-overview-info-{}".format(i+1)
		# 			),
		# 			style={"padding":"1rem","width":"8rem"}
		# 		)

		row_div = [payor, lob, period, contract, revenue, status]

		row_div = row_div \
					+ [
						html.Div(
							dbc.Button(
								"\u1405", 
								href = df.iloc[i,num_of_cols-1], 
								size="sm", 
								color='light', 
								style={"border-radius":"10rem","border":"1px solid "+grey3}, 
								block=True
							),
							style={"padding":"1rem","width":"6rem"}
						)
					]

		# benefit_type = html.Div(
		# 			[
		# 				html.H1("Plan Benefit Type", style={"font-size":"0.8rem"}),
		# 				html.P(df.iloc[i,6], style={"font-size":"1rem","color":"#919191"})
		# 			],
		# 			style={"padding":"1rem","width":"18rem"}
					
		# 		)

		# vbc_method = html.Div(
		# 			[
		# 				html.H1("VBC Adjustment Method", style={"font-size":"0.8rem"}),
		# 				html.P(df.iloc[i,8], style={"font-size":"1rem","color":"#919191"})
		# 			],
		# 			style={"padding":"1rem","width":"18rem"}
		# 		)

		# period = html.Div(
		# 			[
		# 				html.H1("Contract Period", style={"font-size":"0.8rem"}),
		# 				html.P(df.iloc[i,9], style={"font-size":"1rem","color":"#919191"})
		# 			],
		# 			style={"padding":"1rem","width":"18rem"}
		# 		)

		# extra_div = [benefit_type, vbc_method, period]

		content_div = content_div \
						+ [
							html.Div(
								[
									
									html.Div(row_div, style={"display":"flex"}),
									# dbc.Collapse(
									# 	dbc.Card(
									# 		html.Div(
									# 			extra_div, style={"display":"flex", "margin":"0.75rem","padding":"1rem", "background-color":grey3, "border":"none", "border-radius":"0.5rem"}
									# 		)
									# 	), 
									# 	id="overview-info-{}".format(i+1)
									# ),
								], style={"margin-bottom":"1rem","border-radius":"1rem","background-color":"#fff", "box-shadow":"0 4px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 20px 0 rgba(0, 0, 0, 0.05)"}
							)
						]

	return content_div



layout = create_layout(app)

# app.layout = create_layout(app)


# @app.callback(
# 	[Output('overview-info-1', 'is_open'),Output('button-overview-info-1','children')],
# 	[Input('button-overview-info-1', 'n_clicks')]
# 	)
# def toggle_collapse(n):
# 	if n and n%2 == 1:
# 		return True, 'info \u25B2'
# 	return False, 'info \u25BC'

# @app.callback(
# 	[Output('overview-info-2', 'is_open'),Output('button-overview-info-2','children')],
# 	[Input('button-overview-info-2', 'n_clicks')]
# 	)
# def toggle_collapse(n):
# 	if n and n%2 == 1:
# 		return True, 'info \u25B2'
# 	return False, 'info \u25BC'

# @app.callback(
# 	[Output('overview-info-3', 'is_open'),Output('button-overview-info-3','children')],
# 	[Input('button-overview-info-3', 'n_clicks')]
# 	)
# def toggle_collapse(n):
# 	if n and n%2 == 1:
# 		return True, 'info \u25B2'
# 	return False, 'info \u25BC'



## data intake callbacks

@app.callback(
	Output('modal-edit-assumption-newcontract', 'is_open'),
	[Input('button-edit-assumption-newcontract', 'n_clicks'), Input('close-edit-assumption-newcontract', 'n_clicks'), Input('close-edit-assumption-newcontract-3', 'n_clicks')],
	[State("modal-edit-assumption-newcontract","is_open")]
	)
def toggle_collapse(n1, n2, n3, is_open):
	if n1 or n2 or n3:
		return not is_open
	return is_open

@app.callback(
	[Output('data-intake-collapse-age-newcontract', 'is_open'),Output('button-data-intake-collapse-age-newcontract','children')],
	[Input('button-data-intake-collapse-age-newcontract', 'n_clicks')]
	)
def toggle_collapse(n):
	if n and n%2 == 1:
		return True, '\u25B2'
	return False, '\u25BC'

@app.callback(
	[Output('data-intake-collapse-gender-newcontract', 'is_open'),Output('button-data-intake-collapse-gender-newcontract','children')],
	[Input('button-data-intake-collapse-gender-newcontract', 'n_clicks')]
	)
def toggle_collapse(n):
	if n and n%2 == 1:
		return True, '\u25B2'
	return False, '\u25BC'

# @app.callback(
# 	[Output('data-intake-collapse-benefit-newcontract', 'is_open'),Output('button-data-intake-collapse-benefit-newcontract','children')],
# 	[Input('button-data-intake-collapse-benefit-newcontract', 'n_clicks')]
# 	)
# def toggle_collapse(n):
# 	if n and n%2 == 1:
# 		return True, '\u25B2'
# 	return False, '\u25BC'

@app.callback(
	[Output('data-intake-collapse-month-newcontract', 'is_open'),Output('button-data-intake-collapse-month-newcontract','children')],
	[Input('button-data-intake-collapse-month-newcontract', 'n_clicks')]
	)
def toggle_collapse(n):
	if n and n%2 == 1:
		return True, '\u25B2'
	return False, '\u25BC'



@app.callback(
	[
		Output('contract-overview-list-content', 'children'),
		Output('contract-overview-dropdown-container-payor', 'children'),
		Output('contract-overview-dropdown-container-lob', 'children'),
		Output('contract-overview-dropdown-container-contract', 'children'),
		Output('contract-overview-dropdown-container-status', 'children'),
	],
	[
		Input('contract-overview-dropdown-payor', 'value'),
		Input('contract-overview-dropdown-lob','value'),
		Input('contract-overview-dropdown-contract','value'),
		Input('contract-overview-dropdown-status','value'),
	]
	)
def generate_contract_list(payor, lob, contract, status):

	ctx = dash.callback_context

	if not ctx.triggered:		
		return contract_overview_list_content(df_contract_overview),contract_overview_dropdown(df_contract_overview, 'Payor', 'contract-overview-dropdown-payor', prior_value='All'),\
		contract_overview_dropdown(df_contract_overview, 'LOB', 'contract-overview-dropdown-lob', prior_value='All'),\
		contract_overview_dropdown(df_contract_overview, 'VBC Contract Type', 'contract-overview-dropdown-contract', prior_value='All'),\
		contract_overview_dropdown(df_contract_overview, 'Status', 'contract-overview-dropdown-status', prior_value='All')
	else:
		col_value = {'Payor':payor, 'LOB':lob,'VBC Contract Type':contract,'Status':status}
		reset_dropdown_value = {'Payor':payor, 'LOB':lob,'VBC Contract Type':contract,'Status':status}

		button_id = ctx.triggered[0]['prop_id'].split('.')[0]

		df = df_contract_overview.copy()

		if button_id =='contract-overview-dropdown-payor':
			if payor!='All':
				df = df[df['Payor'] == payor]
			current_col = 'Payor'
		
		elif button_id =='contract-overview-dropdown-lob':
			if lob!='All':
				df = df[df['LOB'] == lob]
			current_col = 'LOB'

		elif button_id =='contract-overview-dropdown-contract':
			if contract!='All':
				df = df[df['VBC Contract Type'] == contract]
			current_col = 'VBC Contract Type'

		elif button_id =='contract-overview-dropdown-status':
			if status!='All':
				df = df[df['Status'] == status]
			current_col = 'Status'

		df_filter_current_dropdown = df.copy()
	
		for col, v in col_value.items():
			if col!= current_col:
				if v not in df_filter_current_dropdown[col].tolist():
					reset_dropdown_value[col] = 'All'
				
				if reset_dropdown_value[col] !='All':
					df = df[df[col]==reset_dropdown_value[col]]

		return contract_overview_list_content(df),contract_overview_dropdown(df, 'Payor', 'contract-overview-dropdown-payor', reset_dropdown_value['Payor']),\
		contract_overview_dropdown(df, 'LOB', 'contract-overview-dropdown-lob',reset_dropdown_value['LOB']),\
		contract_overview_dropdown(df, 'VBC Contract Type', 'contract-overview-dropdown-contract', reset_dropdown_value['VBC Contract Type']),\
		contract_overview_dropdown(df, 'Status', 'contract-overview-dropdown-status', reset_dropdown_value['Status'])




if __name__ == "__main__":
	app.run_server(host="0.0.0.0",port=8094, debug = True)


