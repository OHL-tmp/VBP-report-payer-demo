import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash_table.FormatTemplate as FormatTemplate

import pandas as pd
import numpy as np

import pathlib
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from dash_table.Format import Format, Scheme



app = dash.Dash(__name__, url_base_pathname='/vbc-payer-demo/tableview/')

server = app.server

#df_drilldown = pd.read_csv("data/drilldown_sample_5.csv")
#df_drilldown["Diff % from Target Utilization"] = df_drilldown.apply(lambda x: format( x['Annualized Utilization'] - x['Target Utilization']/x['Target Utilization'], '.2%'), axis = 1)
#df_drilldown['Diff % from Target Total Cost'] = df_drilldown.apply(lambda x: format( x['Annualized Total Cost'] - x['Target Total Cost']/x['Target Total Cost'], '.2%'), axis = 1)
#df_drilldown['YTD Unit Cost'] = df_drilldown.apply(lambda x: round( x['YTD Total Cost']/x['YTD Utilization'], 2), axis = 1)
#df_drilldown['Annualized Unit Cost'] = df_drilldown.apply(lambda x: round( x['Annualized Total Cost']/x['Annualized Utilization'], 2), axis = 1)
#df_drilldown['Target Unit Cost'] = df_drilldown.apply(lambda x: round( x['Target Total Cost']/x['Target Utilization'], 2), axis = 1)
#df_drilldown['Diff % from Target Unit Cost'] = df_drilldown.apply(lambda x: format( x['Annualized Unit Cost'] - x['Target Unit Cost']/x['Target Unit Cost'], '.2%'), axis = 1)

df_drilldown=pd.read_csv("data/drilldown_data_table_header.csv")










dimension = {'Age Band' : ['<65', '65-74', '75-85', '>=85'], 'Gender' : ['F', 'M'], 
'Patient Health Risk Level' : ['Low', 'Mid', 'High'], 'Clinical Condition Type' : [], 
       'Clinical Condition' : [], 'Managing Physician Specialty': [], 
       'Managing Physician' : []}
measure = ['YTD Utilization', 'Annualized Utilization', 'Benchmark Utilization', 'Diff % from Benchmark Utilization',
		'YTD Total Cost', 'Annualized Total Cost', 'Benchmark Total Cost', 'Diff % from Benchmark Total Cost',
		'YTD Unit Cost', 'Annualized Unit Cost', 'Benchmark Unit Cost', 'Diff % from Benchmark Unit Cost']
measure_ori = ['YTD Utilization',
       'Annualized Utilization', 'Benchmark Utilization', 'YTD Total Cost',
       'Annualized Total Cost', 'Benchmark Total Cost', 'YTD Inpatient Short Stay Utilization', 'Annualized Inpatient Short Stay Utilization',
       'Benchmark Inpatient Short Stay Utilizatio', 'YTD 30D Readmission Rate', 'Annualized 30D Readmission Rate', 
       'Benchmark 30D Readmission Rate', 'YTD 30D Post Discharge ER Rate', 'Annualized 30D Post Discharge ER Rate',
       'Benchmark 30D Post Discharge ER Rate', 'YTD ASC Surgery %', 'Annualized ASC Surgery %', 'Benchmark ASC Surgery %',
       'YTD Generic Dispensing Rate', 'Annualized Generic Dispensing Rate', 'Benchmark Generic Dispensing Rate']
filter_list = {
       'Inpatient' : ['Acute myocardial infarction', 'CABG', 'Cardiac Arrhythmia', 'Cardiac arrest and ventricular fibrillation', 'Heart Failure', 'Hypertension', 'ICD', 'Others', 'PCI', 'Pacemaker Implant', 'Pleural effusion', 'Renal Failure'],
 		'Outpatient ER' : ['AMI', 'Aftercare following surgery', 'COPD', 'Cardiac dysrhythmias', 'Diabetes', 'Heart Failure', 'Hypertension', 'Others', 'Respiratory system and chest symptoms'], 
 		'Outpatient Others (Non ER)' : ['Ambulance', 'Durable Medical Equipment (DME)', 'Lab/Pathology', 'Observation', 'Others', 'Outpatient Surgery', 'Radiology'], 
 		'Professional Services' : [ 'Administered Drugs', 'Anesthesia', 'Lab/Pathology', 'Office Visits', 'Others', 'Radiology', 'Surgical'], 
 		'Drug Others (Excl. Entrestro)' : ['ACE /ARB', 'Aldosterone receptor antagonists', 'Beta Blocker', 'Diuretics', 'Others', 'Vasodilators'], 
 		'Drug Entresto': ['Entresto'], 'Home Health' : ['Home Health'], 'Skilled Nursing Facility' : ['Skilled Nursing Facility'], 'Hospice' : ['Hospice']}




cate_mix_cnt = 0
for k in list(filter_list.keys()):
	cate_mix_cnt = cate_mix_cnt + len(filter_list[k])


def tableview():
	return html.Div(
		[
			dbc.Row(
				[
					dbc.Col(
						[
							html.Div(
								[
									html.H4("Filter", style={"font-size":"1rem","padding-left":"0.5rem", "padding-top":"0.5rem"}),
#									html.H5("Filter 1", style={"font-size":"0.8rem","color":"#919191","padding-left":"0.5rem", "padding-top":"0.5rem"}),
									dcc.Dropdown(
										id = "drilldown-dropdown-dimension-filter-selection",
										options = [{"label": 'Service Category', "value": 'Service Category'}] 
										+ [{"label": k, "value": k, 'disabled' : True} if len(dimension[k]) == 0 else {"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys())],
										placeholder = "Add a Filter",
										style = {"font-family":"NotoSans-Condensed"}
										),
									html.H5("", style={"font-size":"0.8rem"}),
									dcc.Dropdown(
										id = "drilldown-dropdown-dimension-filter",
										placeholder = "Select Filter Value",
										multi = True,
										style = {"font-family":"NotoSans-Condensed"},
										),
									html.H4("Select Dimension", style={"font-size":"1rem","padding-left":"0.5rem", "padding-top":"0.5rem"}),
									html.H5("First Dimension", style={"font-size":"0.8rem","color":"#919191","padding-left":"0.5rem", "padding-top":"0.5rem"}),
									dcc.Dropdown(
										id = "drilldown-dropdown-dimension-1",
										placeholder ="...",
										options = [{"label": 'Service Category', "value": 'Service Category'}, {"label": 'Sub Category', "value": 'Sub Category', 'disabled': True}] 
										+ [{"label": k, "value": k, 'disabled' : True} if len(dimension[k]) == 0 else {"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys())],
										value = 'Patient Health Risk Level',
										clearable = False,
										style = {"font-family":"NotoSans-Condensed"}
										),
									html.H5("", style={"font-size":"0.8rem"}),
									dcc.Dropdown(
										id = "drilldown-dropdown-dimension-filter-1",
										placeholder = "Select Filter Value",
										multi = True,
										style = {"font-family":"NotoSans-Condensed"},
										),
									html.H5("Second Dimension", style={"font-size":"0.8rem","color":"#919191","padding-left":"0.5rem", "padding-top":"0.5rem"}),
									dcc.Dropdown(
										id = "drilldown-dropdown-dimension-2",
										disabled=True,
										placeholder ="...",
										style = {"font-family":"NotoSans-Condensed"}
										),
									html.H5("", style={"font-size":"0.8rem"}),
									dcc.Dropdown(
										id = "drilldown-dropdown-dimension-filter-2",
										placeholder = "Select Filter Value",
										multi = True,
										style = {"font-family":"NotoSans-Condensed"},
										),
									html.H5("Third Dimension", style={"font-size":"0.8rem","color":"#919191","padding-left":"0.5rem", "padding-top":"0.5rem"}),
									dcc.Dropdown(
										id = "drilldown-dropdown-dimension-3",
										disabled=True,
										placeholder ="...",
										style = {"font-family":"NotoSans-Condensed"}
										),
									html.H5("", style={"font-size":"0.8rem"}),
									dcc.Dropdown(
										id = "drilldown-dropdown-dimension-filter-3",
										placeholder = "Select Filter Value",
										multi = True,
										style = {"font-family":"NotoSans-Condensed"},
										),
									html.H4("Select Measures", style={"font-size":"1rem","padding-left":"0.5rem", "padding-top":"1rem"}),
									dcc.Dropdown(
										id = "drilldown-dropdown-measure-1",
										options = [{"label": k, "value": k} for k in measure],
										value = ['Diff % from Benchmark Total Cost', 'YTD Total Cost', 'Annualized Total Cost', 'Benchmark Total Cost'],
										placeholder ="Select measures",
										multi = True,
										style = {"font-family":"NotoSans-Condensed"}
										),
								]
							),
							
						],
						width=3,
						style={"overflow-y":"scroll"}
					),
						
					dbc.Col(
						[
							html.Div(
								[
									html.P("*Default sorted by Diff % from Benchmark Total Cost", style={"font-size":"0.6rem"}),
									dash_table.DataTable(
										id = 'drilldown-datatable-tableview',
										style_header = {'height': 'auto', 'width':'auto','whiteSpace':'normal','font-family':'NotoSans-Condensed','font-size':'auto','backgroundColor': '#dce7fc','color':'#1357DD'},
										style_cell = {'font-family':'NotoSans-Regular','font-size':'0.8rem','textAlign': 'center'},
										#fixed_rows={ 'headers': True, 'data': 0 },
										style_table = {'textAlign': 'center'},
										sort_action='native',
										page_size=200,
										style_data_conditional=[
									        {
									            'if': {'row_index': 'odd'},
									            'backgroundColor': 'rgb(248, 248, 248)'
									        }],
										)
								],
								style={"padding-left":"1rem","padding-right":"1rem","padding-bottom":"1rem","overflow":"scroll",'max-height':'60rem'}
							)
							
						],
						width = 9,
						
					),
				]
			)
		]
	)

app.layout = tableview()

@app.callback(
	[Output('drilldown-dropdown-dimension-filter', 'options'),
	Output('drilldown-dropdown-dimension-filter', 'value'),
	Output('drilldown-dropdown-dimension-filter', 'disabled')],
	[Input('drilldown-dropdown-dimension-filter-selection', 'value')]
	)
def update_filter(v):
	if v:
		if v=='Service Category':
			return [{'label': k, 'value': k} for k in list(filter_list.keys())], list(filter_list.keys()), False 
		else:
			return [{'label':k, 'value':k} for k in dimension[v]], dimension[v], False
	return [],[],True

@app.callback(
	[Output("drilldown-dropdown-dimension-filter-1", 'options'),
	Output("drilldown-dropdown-dimension-filter-1", 'value'),
	Output("drilldown-dropdown-dimension-filter-1", 'disabled')],
	[Input('drilldown-dropdown-dimension-1', 'value'),
	Input('drilldown-dropdown-dimension-filter-selection', 'value')],
	[State('drilldown-dropdown-dimension-filter', 'options'),
	State('drilldown-dropdown-dimension-filter', 'value')]
	)
def update_dimension_filter_1(v1, v2, op, v3):
	if v1:
		if v2 and v1 == v2:
			return op, v3, False
		else:
			if v1 == 'Service Category':
				return [{'label': k, 'value': k} for k in list(filter_list.keys())], list(filter_list.keys()), False 
			else:
				return [{'label':k, 'value':k} for k in dimension[v1]], dimension[v1], False 
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
	Input('drilldown-dropdown-dimension-filter-selection', 'value')],
	[State('drilldown-dropdown-dimension-filter', 'options'),
	State('drilldown-dropdown-dimension-filter', 'value')]
	)
def update_dimension_filter_2(v1, v2, op, v3):
	if v1:
		if v2 and v1 == v2:
			return op, v3, False
		else:
			if v1 == 'Service Category':
				return [{'label': k, 'value': k} for k in list(filter_list.keys())], list(filter_list.keys()), False 
			elif v1 == 'Sub Category':
				return [{'label':'All','value':'All'}],["All"],True
			else:
				return [{'label':k, 'value':k} for k in dimension[v1]], dimension[v1], False 
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
	Input('drilldown-dropdown-dimension-filter-selection', 'value')],
	[State('drilldown-dropdown-dimension-filter', 'options'),
	State('drilldown-dropdown-dimension-filter', 'value')]
	)
def update_dimension_filter_3(v1, v2, op, v3):
	if v1:
		if v2 and v1 == v2:
			return op, v3, False
		else:
			if v1 == 'Service Category':
				return [{'label': k, 'value': k} for k in list(filter_list.keys())], list(filter_list.keys()), False 
			elif v1 == 'Sub Category':
				return [{'label':'All','value':'All'}],["All"],True
			else:
				return [{'label':k, 'value':k} for k in dimension[v1]], dimension[v1], False 
	return [],[],True


if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True, port=8051)