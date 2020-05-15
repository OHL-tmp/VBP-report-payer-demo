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



# app = dash.Dash(__name__, url_base_pathname='/vbc-payer-demo/tableview/')

# server = app.server

#df_drilldown = pd.read_csv("data/drilldown_sample_5.csv")
#df_drilldown["Diff % from Target Utilization"] = df_drilldown.apply(lambda x: format( x['Annualized Utilization'] - x['Target Utilization']/x['Target Utilization'], '.2%'), axis = 1)
#df_drilldown['Diff % from Target Total Cost'] = df_drilldown.apply(lambda x: format( x['Annualized Total Cost'] - x['Target Total Cost']/x['Target Total Cost'], '.2%'), axis = 1)
#df_drilldown['YTD Unit Cost'] = df_drilldown.apply(lambda x: round( x['YTD Total Cost']/x['YTD Utilization'], 2), axis = 1)
#df_drilldown['Annualized Unit Cost'] = df_drilldown.apply(lambda x: round( x['Annualized Total Cost']/x['Annualized Utilization'], 2), axis = 1)
#df_drilldown['Target Unit Cost'] = df_drilldown.apply(lambda x: round( x['Target Total Cost']/x['Target Utilization'], 2), axis = 1)
#df_drilldown['Diff % from Target Unit Cost'] = df_drilldown.apply(lambda x: format( x['Annualized Unit Cost'] - x['Target Unit Cost']/x['Target Unit Cost'], '.2%'), axis = 1)

df_pt_lv1=pd.read_csv("data/Pt Level V1.csv")
df_pt_epi_phy_lv1=pd.read_csv("data/Pt Episode Phy Level V1.csv")
df_pt_epi_phy_srv_lv1=pd.read_csv("data/Pt Episode Phy Srv Level V1.csv")



dimension = {'Age Band' : list(df_pt_epi_phy_srv_lv1['Age Band'].unique()), 'Gender' : list(df_pt_epi_phy_srv_lv1['Gender'].unique()), 
'Patient Health Risk Level' : list(df_pt_epi_phy_srv_lv1['Patient Health Risk Level'].unique()), 'Clinical Condition Type' : list(df_pt_epi_phy_srv_lv1['Clinical Condition Type'].unique()), 
	   'Clinical Condition' : list(df_pt_epi_phy_srv_lv1['Clinical Condition'].unique()), 'Managing Physician Specialty': list(df_pt_epi_phy_srv_lv1['Managing Physician Specialty'].unique()), 
	   'Managing Physician' : list(df_pt_epi_phy_srv_lv1['Managing Physician'].unique())}
measure = ['YTD Utilization', 'Annualized Utilization', 'Benchmark Utilization', 'Diff % from Benchmark Utilization',
		'YTD Total Cost', 'Annualized Total Cost', 'Benchmark Total Cost', 'Diff % from Benchmark Total Cost',
		'YTD Unit Cost', 'Annualized Unit Cost', 'Benchmark Unit Cost', 'Diff % from Benchmark Unit Cost']
clinical_measure = ['YTD Inpatient Short Stay Utilization', 'Annualized Inpatient Short Stay Utilization', 'Benchmark Inpatient Short Stay Utilization','Diff % from Benchmark Inpatient Short Stay Utilization',
#'YTD 30D Readmission Rate', 'Annualized 30D Readmission Rate','Benchmark 30D Readmission Rate','Diff % from Benchmark 30D Readmission Rate',
#'YTD 30D Post Discharge ER Rate','Annualized 30D Post Discharge ER Rate','Benchmark 30D Post Discharge ER Rate', 'Diff % from Benchmark 30D Post Discharge ER Rate'
]
episode_measure = ['Episode %','YTD Inpatient Short Stay Utilization per Episode', 'Annualized Inpatient Short Stay Utilization per Episode', 'Benchmark Inpatient Short Stay Utilization per Episode','Diff % from Benchmark Inpatient Short Stay Utilization per Episode',
'YTD 30D Readmission Rate per Episode', 'Annualized 30D Readmission Rate per Episode','Benchmark 30D Readmission Rate per Episode','Diff % from Benchmark 30D Readmission Rate per Episode',
'YTD 30D Post Discharge ER Rate per Episode','Annualized 30D Post Discharge ER Rate per Episode','Benchmark 30D Post Discharge ER Rate per Episode', 'Diff % from Benchmark 30D Post Discharge ER Rate per Episode']
measure_ori = [ 'YTD Utilization', 'Annualized Utilization', 'Benchmark Utilization',
	   'YTD Total Cost', 'Annualized Total Cost', 'Benchmark Total Cost', 'YTD Inpatient Short Stay Utilization',
	   'Annualized Inpatient Short Stay Utilization',
	   'Benchmark Inpatient Short Stay Utilization',
	   'YTD 30D Readmission Rate', 'YTD 30D Readmission Rate - D',
	   'YTD 30D Readmission Rate - N', 'Annualized 30D Readmission Rate',
	   'Annualized 30D Readmission Rate - D',
	   'Annualized 30D Readmission Rate - N', 'Benchmark 30D Readmission Rate',
	   'Benchmark 30D Readm Rate - D', 'Benchmark 30D Readm Rate - N',
	   'YTD 30D Post Discharge ER Rate', 'YTD 30D Post Discharge ER Rate - D',
	   'YTD 30D Post Discharge ER Rate - N',
	   'Annualized 30D Post Discharge ER Rate',
	   'Annualized 30D Post Discharge ER Rate - D',
	   'Annualized 30D Post Discharge ER Rate - N',
	   'Benchmark 30D Post Discharge ER Rate', 'Benchmark 30D ER Rate - D',
	   'Benchmark 30D ER Rate - N']
filter_list = {
	   'Inpatient' : list(df_pt_epi_phy_srv_lv1[df_pt_epi_phy_srv_lv1['Service Category'] == 'Inpatient']['Sub Category'].unique()),
		'Outpatient' : list(df_pt_epi_phy_srv_lv1[df_pt_epi_phy_srv_lv1['Service Category'] == 'Outpatient']['Sub Category'].unique()), 
		'Professional' : list(df_pt_epi_phy_srv_lv1[df_pt_epi_phy_srv_lv1['Service Category'] == 'Professional']['Sub Category'].unique()), 
		'Rx' : list(df_pt_epi_phy_srv_lv1[df_pt_epi_phy_srv_lv1['Service Category'] == 'Rx']['Sub Category'].unique()), 
		'Home Health' : list(df_pt_epi_phy_srv_lv1[df_pt_epi_phy_srv_lv1['Service Category'] == 'Home Health']['Sub Category'].unique()), 
		'Skilled Nursing Facility': list(df_pt_epi_phy_srv_lv1[df_pt_epi_phy_srv_lv1['Service Category'] == 'Skilled Nursing Facility']['Sub Category'].unique()), 
		'Hospice' : list(df_pt_epi_phy_srv_lv1[df_pt_epi_phy_srv_lv1['Service Category'] == 'Hospice']['Sub Category'].unique())}




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
										options = 
#										[{"label": 'Service Category', "value": 'Service Category'}] + 
										[{"label": k, "value": k, 'disabled' : True} if len(dimension[k]) == 0 else {"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys())],
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

# app.layout = tableview()

# @app.callback(
# 	[Output('drilldown-dropdown-dimension-filter', 'options'),
# 	Output('drilldown-dropdown-dimension-filter', 'value'),
# 	Output('drilldown-dropdown-dimension-filter', 'disabled')],
# 	[Input('drilldown-dropdown-dimension-filter-selection', 'value')]
# 	)
# def update_filter(v):
# 	if v:
# #		if v=='Service Category':
# #			return [{'label': k, 'value': k} for k in list(filter_list.keys())], list(filter_list.keys()), False 
# #		else:
# 		return [{'label':k, 'value':k} for k in dimension[v]], dimension[v], False
# 	return [],[],True

# @app.callback(
# 	[Output("drilldown-dropdown-dimension-filter-1", 'options'),
# 	Output("drilldown-dropdown-dimension-filter-1", 'value'),
# 	Output("drilldown-dropdown-dimension-filter-1", 'disabled')],
# 	[Input('drilldown-dropdown-dimension-1', 'value'),
# 	Input('drilldown-dropdown-dimension-filter-selection', 'value'),
# 	Input('drilldown-dropdown-dimension-filter', 'value')],
# 	[State('drilldown-dropdown-dimension-filter', 'options')]
# 	)
# def update_dimension_filter_1(v1, v2, v3, op):
# 	if v1:
# 		if v2 and v1 == v2:
# 			return op, v3, False
# 		else:
# 			if v1 == 'Service Category':
# 				return [{'label': k, 'value': k} for k in list(filter_list.keys())], list(filter_list.keys()), False 
# 			else:
# 				if v2:
# 					df = df_pt_epi_phy_srv_lv1[df_pt_epi_phy_srv_lv1[v2].isin(v3)]
# 				else:
# 					df = df_pt_epi_phy_srv_lv1
# 				options = list(df[v1].unique())
# 				return [{'label':k, 'value':k} for k in options], options, False 
# 	return [],[],True

# @app.callback(
# 	[Output('drilldown-dropdown-dimension-2', 'options'),
# 	Output('drilldown-dropdown-dimension-2', 'disabled')],
# 	[Input('drilldown-dropdown-dimension-1', 'value')]
# 	)
# def update_dimension_option_2(v):
# 	if v:
# 		if v =='Service Category':
# 			dropdown_option = [{"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys()) if len(dimension[k]) != 0] + [{"label": 'Service Category', "value": 'Service Category', 'disabled' : True}, {"label": 'Sub Category', "value": 'Sub Category'}] + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension.keys()) if len(dimension[k]) == 0]
# 			return dropdown_option, False
# 		else:
# 			dropdown_option = [{"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys()) if len(dimension[k]) != 0 and k != v] + [{"label": 'Service Category', "value": 'Service Category'}, {"label": 'Sub Category', "value": 'Sub Category', 'disabled' : True}] + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension.keys()) if len(dimension[k]) == 0 or k ==v]
# 			return dropdown_option, False
# 	return [], True


# @app.callback(
# 	[Output("drilldown-dropdown-dimension-filter-2", 'options'),
# 	Output("drilldown-dropdown-dimension-filter-2", 'value'),
# 	Output("drilldown-dropdown-dimension-filter-2", 'disabled')],
# 	[Input('drilldown-dropdown-dimension-2', 'value'),
# 	Input('drilldown-dropdown-dimension-filter-selection', 'value'),
# 	Input('drilldown-dropdown-dimension-filter', 'value'),
# 	Input('drilldown-dropdown-dimension-1', 'value'),
# 	Input('drilldown-dropdown-dimension-filter-1', 'value')],
# 	[State('drilldown-dropdown-dimension-filter', 'options')]
# 	)
# def update_dimension_filter_2(v1, v2, v3, d1, d1v, op):
# 	if v1:
# 		if v2 and v1 == v2:
# 			return op, v3, False
# 		else:
# 			if v1 == 'Service Category':
# 				return [{'label': k, 'value': k} for k in list(filter_list.keys())], list(filter_list.keys()), False 
# 			elif v1 == 'Sub Category':
# 				return [{'label':'All','value':'All'}],["All"],True
# 			else:
# 				if v2:
# 					df = df_pt_epi_phy_srv_lv1[(df_pt_epi_phy_srv_lv1[v2].isin(v3)) & (df_pt_epi_phy_srv_lv1[d1].isin(d1v))]
# 				else:
# 					df = df_pt_epi_phy_srv_lv1[df_pt_epi_phy_srv_lv1[d1].isin(d1v)]
# 				options = list(df[v1].unique())
# 				return [{'label':k, 'value':k} for k in options], options, False 
# 	return [],[],True

# @app.callback(
# 	[Output('drilldown-dropdown-dimension-3', 'options'),
# 	Output('drilldown-dropdown-dimension-3', 'disabled')],
# 	[Input('drilldown-dropdown-dimension-2', 'value'),
# 	Input('drilldown-dropdown-dimension-1', 'value')]
# 	)
# def update_dimension_option_3(v1,v2):
# 	v = [v1, v2]
# 	if v1:
# 		if 'Service Category' in v and 'Sub Category' not in v:
# 			dropdown_option = [{"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys()) if len(dimension[k]) != 0] + [{"label": 'Service Category', "value": 'Service Category', 'disabled' : True}, {"label": 'Sub Category', "value": 'Sub Category'}] + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension.keys()) if len(dimension[k]) == 0]
# 			return dropdown_option, False
# 		elif 'Service Category' in v and 'Sub Category' in v:
# 			dropdown_option =  [{"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys()) if len(dimension[k]) != 0] + [{"label": 'Service Category', "value": 'Service Category', 'disabled' : True}, {"label": 'Sub Category', "value": 'Sub Category', 'disabled' : True}] + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension.keys()) if len(dimension[k]) == 0]
# 			return dropdown_option, False
# 		else:
# 			dropdown_option = [{"label": k, "value": k, 'disabled' : False} for k in list(dimension.keys()) if len(dimension[k]) != 0 and k not in v] + [{"label": 'Service Category', "value": 'Service Category'}, {"label": 'Sub Category', "value": 'Sub Category', 'disabled' : True}] + [{"label": k, "value": k, 'disabled' : True} for k in list(dimension.keys()) if len(dimension[k]) == 0 or k in v]
# 			return dropdown_option, False
# 	return [], True


# @app.callback(
# 	[Output("drilldown-dropdown-dimension-filter-3", 'options'),
# 	Output("drilldown-dropdown-dimension-filter-3", 'value'),
# 	Output("drilldown-dropdown-dimension-filter-3", 'disabled')],
# 	[Input('drilldown-dropdown-dimension-3', 'value'),
# 	Input('drilldown-dropdown-dimension-filter-selection', 'value'),
# 	Input('drilldown-dropdown-dimension-filter', 'value'),
# 	Input('drilldown-dropdown-dimension-1', 'value'),
# 	Input('drilldown-dropdown-dimension-filter-1', 'value'),
# 	Input('drilldown-dropdown-dimension-2', 'value'),
# 	Input('drilldown-dropdown-dimension-filter-2', 'value')],
# 	[State('drilldown-dropdown-dimension-filter', 'options')]
# 	)
# def update_dimension_filter_3(v1, v2, v3, d1, d1v, d2, d2v, op):
# 	if v1:
# 		if v2 and v1 == v2:
# 			return op, v3, False
# 		else:
# 			if v1 == 'Service Category':
# 				return [{'label': k, 'value': k} for k in list(filter_list.keys())], list(filter_list.keys()), False 
# 			elif v1 == 'Sub Category':
# 				return [{'label':'All','value':'All'}],["All"],True
# 			else:
# 				if v2:
# 					df = df_pt_epi_phy_srv_lv1[(df_pt_epi_phy_srv_lv1[v2].isin(v3)) & (df_pt_epi_phy_srv_lv1[d1].isin(d1v)) & (df_pt_epi_phy_srv_lv1[d2].isin(d2v))]
# 				elif d2 == 'Sub Category':
# 					df = df_pt_epi_phy_srv_lv1[df_pt_epi_phy_srv_lv1[d1].isin(d1v)]
# 				else:
# 					df = df_pt_epi_phy_srv_lv1[(df_pt_epi_phy_srv_lv1[d1].isin(d1v)) & (df_pt_epi_phy_srv_lv1[d2].isin(d2v))]
# 				options = list(df[v1].unique())
# 				return [{'label':k, 'value':k} for k in options], options, False 
# 	return [],[],True

# @app.callback(
# 	Output('drilldown-dropdown-measure-1', 'options'),
# 	[Input('drilldown-dropdown-dimension-1', 'value'),
# 	Input('drilldown-dropdown-dimension-2', 'value'),
# 	Input('drilldown-dropdown-dimension-3', 'value')]
# 	)
# def update_measure_option(d1, d2, d3):
# 	d = [d1, d2, d3]
# 	if len(d) == 0:
# 		return [{"label": k, "value": k} for k in measure]
# 	else:
# 		if 'Service Category' in d:
# 			return [{"label": k, "value": k} for k in measure]
# 		elif 'Clinical Condition Type' in d or 'Clinical Condition' in d:
# 			return [{"label": k, "value": k} for k in measure] + [{"label": k, "value": k} for k in clinical_measure] + [{"label": k, "value": k} for k in episode_measure]
# 		else:
# 			return [{"label": k, "value": k} for k in measure] + [{"label": k, "value": k} for k in clinical_measure]

# @app.callback(
# 	[Output('drilldown-datatable-tableview', "columns"),
# 	Output('drilldown-datatable-tableview', "data")],
# 	[Input('drilldown-dropdown-dimension-1','value'),
# 	Input('drilldown-dropdown-dimension-2','value'),
# 	Input('drilldown-dropdown-dimension-3','value'),
# 	Input('drilldown-dropdown-dimension-filter-1','value'),
# 	Input('drilldown-dropdown-dimension-filter-2','value'),
# 	Input('drilldown-dropdown-dimension-filter-3','value'),
# 	Input('drilldown-dropdown-dimension-filter-selection','value'),
# 	Input('drilldown-dropdown-dimension-filter', 'value'),
# 	Input('drilldown-dropdown-measure-1', 'value')]
# 	)
# def datatable_data_selection(d1, d2, d3, d1v, d2v, d3v, f, fv, m):
# 	if f:
# 		df_pt_lv1_f = df_pt_lv1[df_pt_lv1[f].isin(fv)]
# 		df_pt_epi_phy_lv1_f = df_pt_epi_phy_lv1[df_pt_epi_phy_lv1[f].isin(fv)]
# 		df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1[df_pt_epi_phy_srv_lv1[f].isin(fv)]
# 	else:
# 		df_pt_lv1_f = df_pt_lv1
# 		df_pt_epi_phy_lv1_f = df_pt_epi_phy_lv1
# 		df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1

# 	d = []
# 	show_column = []
# 	if d1 is not None:
# 		d.append(d1)
# 	if d2 is not None:
# 		d.append(d2)
# 	if d3 is not None:
# 		d.append(d3)
# 	show_column = d + ['Patient %'] + m


# 	for i in range(3):
# 		if eval('d'+str(i+1)) and eval('d'+str(i+1)) not in ['Service Category', 'Sub Category']:
# 			df_pt_lv1_f = df_pt_lv1_f[(df_pt_lv1_f[eval('d'+str(i+1))].isin(eval('d'+str(i+1)+'v')))]
# 			df_pt_epi_phy_lv1_f = df_pt_epi_phy_lv1_f[(df_pt_epi_phy_lv1_f[eval('d'+str(i+1))].isin(eval('d'+str(i+1)+'v')))]
# 			df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1_f[(df_pt_epi_phy_srv_lv1_f[eval('d'+str(i+1))].isin(eval('d'+str(i+1)+'v')))]
# 		elif eval('d'+str(i+1)) == 'Service Category':
# 			df_pt_lv1_f = df_pt_lv1_f
# 			df_pt_epi_phy_lv1_f = df_pt_epi_phy_lv1_f
# 			df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1_f[(df_pt_epi_phy_srv_lv1_f[eval('d'+str(i+1))].isin(eval('d'+str(i+1)+'v')))]
# 		else:		
# 			df_pt_lv1_f = df_pt_lv1_f
# 			df_pt_epi_phy_lv1_f = df_pt_epi_phy_lv1_f
# 			df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1_f

# 	d_set = list(set(d) - set(['Service Category', 'Sub Category']))
# 	if len(d_set)>0:
# 		df_agg_pt = df_pt_lv1_f.groupby(by = d_set).agg({'Pt Ct':'nunique', 'Episode Ct':'count'}).reset_index()
# 		df_agg_clinical = df_pt_epi_phy_lv1_f.groupby(by = d_set).sum().reset_index()
# 		df_agg_cost = df_pt_epi_phy_srv_lv1_f.groupby(by = d).sum().reset_index()

# 		df_agg_pre = pd.merge(df_agg_pt, df_agg_clinical, how = 'left', on = d_set )
# 		df_agg = pd.merge(df_agg_cost, df_agg_pre, how = 'left', on = d_set )


# 		df_agg['YTD Inpatient Short Stay Utilization'] = 1000*df_agg['YTD Inpatient Short Stay Utilization']/df_agg['Pt Ct']
# 		df_agg['Annualized Inpatient Short Stay Utilization'] = 1000*df_agg['Annualized Inpatient Short Stay Utilization']/df_agg['Pt Ct']
# 		df_agg['Benchmark Inpatient Short Stay Utilization'] = 1000*df_agg['Benchmark Inpatient Short Stay Utilization']/df_agg['Pt Ct']
# 		df_agg['Diff % from Benchmark Inpatient Short Stay Utilization'] = (df_agg['Annualized Inpatient Short Stay Utilization'] - df_agg['Benchmark Inpatient Short Stay Utilization'])/df_agg['Benchmark Inpatient Short Stay Utilization']

# 		df_agg['YTD Inpatient Short Stay Utilization per Episode'] = 1000*df_agg['YTD Inpatient Short Stay Utilization']/df_agg['Episode Ct']
# 		df_agg['Annualized Inpatient Short Stay Utilization per Episode'] = 1000*df_agg['Annualized Inpatient Short Stay Utilization']/df_agg['Episode Ct']
# 		df_agg['Benchmark Inpatient Short Stay Utilization per Episode'] = 1000*df_agg['Benchmark Inpatient Short Stay Utilization']/df_agg['Episode Ct']
# 		df_agg['Diff % from Benchmark Inpatient Short Stay Utilization per Episode'] = (df_agg['Annualized Inpatient Short Stay Utilization per Episode'] - df_agg['Benchmark Inpatient Short Stay Utilization per Episode'])/df_agg['Benchmark Inpatient Short Stay Utilization per Episode']

# 		df_agg['YTD 30D Readmission Rate per Episode'] = df_agg['YTD 30D Readmission Rate - N']/df_agg['YTD 30D Readmission Rate - D']
# 		df_agg['Annualized 30D Readmission Rate per Episode'] = df_agg['Annualized 30D Readmission Rate - N']/df_agg['Annualized 30D Readmission Rate - D']
# 		df_agg['Benchmark 30D Readmission Rate per Episode'] = df_agg['Benchmark 30D Readm Rate - N']/df_agg['Benchmark 30D Readm Rate - D']
# 		df_agg['Diff % from Benchmark 30D Readmission Rate per Episode'] = (df_agg['Annualized 30D Readmission Rate per Episode'] - df_agg['Benchmark 30D Readmission Rate per Episode'])/df_agg['Benchmark 30D Readmission Rate per Episode']

# 		df_agg['YTD 30D Post Discharge ER Rate per Episode'] = df_agg['YTD 30D Post Discharge ER Rate - N']/df_agg['YTD 30D Post Discharge ER Rate - D']
# 		df_agg['Annualized 30D Post Discharge ER Rate per Episode'] = df_agg['Annualized 30D Post Discharge ER Rate - N']/df_agg['Annualized 30D Post Discharge ER Rate - D']
# 		df_agg['Benchmark 30D Post Discharge ER Rate per Episode'] = df_agg['Benchmark 30D ER Rate - N']/df_agg['Benchmark 30D ER Rate - D']
# 		df_agg['Diff % from Benchmark 30D Post Discharge ER Rate per Episode'] = (df_agg['Annualized 30D Post Discharge ER Rate per Episode'] - df_agg['Benchmark 30D Post Discharge ER Rate per Episode'])/df_agg['Benchmark 30D Post Discharge ER Rate per Episode']
		
		
# 	else:
# #			df_agg_pt = df_pt_lv1_f.groupby(by = d_set).agg({'Pt Ct':'nunique', 'Episode Ct':'count'}).reset_index()
# #			df_agg_clinical = df_pt_epi_phy_lv1_f.groupby(by = d_set).sum().reset_index()
# 		df_agg = df_pt_epi_phy_srv_lv1_f.groupby(by = d).sum().reset_index()
# 		df_agg['Pt Ct'] = 5000
# 		df_agg['Episode Ct'] = 91277


# 	df_agg['Patient %'] = df_agg['Pt Ct']/5000
# 	df_agg['Episode %'] = df_agg['Episode Ct']/91277

# 	df_agg['YTD Utilization'] = df_agg['YTD Utilization']/df_agg['Pt Ct']
# 	df_agg['Annualized Utilization'] = df_agg['Annualized Utilization']/df_agg['Pt Ct']
# 	df_agg['Benchmark Utilization'] = df_agg['Benchmark Utilization']/df_agg['Pt Ct']
# 	df_agg['Diff % from Benchmark Utilization'] = (df_agg['Annualized Utilization'] - df_agg['Benchmark Utilization'])/df_agg['Benchmark Utilization']

# 	df_agg['YTD Total Cost'] = df_agg['YTD Total Cost']/df_agg['Pt Ct']
# 	df_agg['Annualized Total Cost'] = df_agg['Annualized Total Cost']/df_agg['Pt Ct']
# 	df_agg['Benchmark Total Cost'] = df_agg['Benchmark Total Cost']/df_agg['Pt Ct']
# 	df_agg['Diff % from Benchmark Total Cost'] = (df_agg['Annualized Total Cost'] - df_agg['Benchmark Total Cost'])/df_agg['Benchmark Total Cost']

# 	df_agg['YTD Unit Cost'] = df_agg['YTD Total Cost']/df_agg['YTD Utilization']
# 	df_agg['Annualized Unit Cost'] = df_agg['Annualized Total Cost']/df_agg['Annualized Utilization']
# 	df_agg['Benchmark Unit Cost'] = df_agg['Benchmark Total Cost']/df_agg['Benchmark Utilization']
# 	df_agg['Diff % from Benchmark Unit Cost'] = (df_agg['Annualized Unit Cost'] - df_agg['Benchmark Unit Cost'])/df_agg['Benchmark Unit Cost']


# 	if 'Diff % from Benchmark Total Cost' in m:
# 		df_agg =  df_agg[show_column].sort_values(by =  'Diff % from Benchmark Total Cost', ascending =False)
# 	else:
# 		df_agg = df_agg[show_column]

# 	pct_list = ['Diff % from Benchmark Utilization', 'Diff % from Benchmark Total Cost', 'Diff % from Benchmark Unit Cost', 'Diff % from Benchmark Inpatient Short Stay Utilization',
# 	'Episode %', 'Patient %', 'Diff % from Benchmark Inpatient Short Stay Utilization per Episode', 
# 	'YTD 30D Readmission Rate per Episode', 'Annualized 30D Readmission Rate per Episode','Benchmark 30D Readmission Rate per Episode','Diff % from Benchmark 30D Readmission Rate per Episode',
# 	'YTD 30D Post Discharge ER Rate per Episode','Annualized 30D Post Discharge ER Rate per Episode','Benchmark 30D Post Discharge ER Rate per Episode', 'Diff % from Benchmark 30D Post Discharge ER Rate per Episode']
# 	dollar_list = ['YTD Total Cost', 'Annualized Total Cost', 'Benchmark Total Cost',
# 	'YTD Unit Cost', 'Annualized Unit Cost', 'Benchmark Unit Cost']

# 	return [{"name": i, "id": i, "selectable":True,"type":"numeric", "format": FormatTemplate.percentage(1)} if i in pct_list else {"name": i, "id": i, "selectable":True, "type":"numeric","format": FormatTemplate.money(0)} if i in dollar_list else {"name": i, "id": i, "selectable":True, "type":"numeric","format": Format(precision=1, scheme = Scheme.fixed)} for i in show_column], df_agg.to_dict('records')






if __name__ == "__main__":
	app.run_server(host="127.0.0.1",debug=True, port=8051)
