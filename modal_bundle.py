import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_table

import pandas as pd
import numpy as np

import pathlib
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
from utils import *
from figure import *

#app = dash.Dash(__name__)

df_bundles_default = pd.read_csv("data/df_bundles_90.csv")
modal_columns = df_bundles_default.columns[3:9]

conditional_data_style = [
			        {
			            'if': {'column_id': 'Bundle'},
			            'textAlign': 'left'
			        },
			        {
			        	'if':{'column_id':'Bundle Count'},
			        	'width':'10%'
			        },
			        {
			        	'if':{'column_id':"Total Bundle Cost"},
			        	'width':'10%'
			        },
			        {
			        	'if':{'column_id':'Average Bundle Cost'},
			        	'width':'10%'
			        },
			        {
			        	'if':{'column_id':'Benchmark Average'},
			        	'width':'10%'
			        },
			        {
			        	'if':{'column_id':"Best-in-Class Average"},
			        	'width':'10%'
			        },
			        {
			        	'if':{'column_id':"Estimated Opportunity Size"},
			        	'width':'10%'
			        },
			        ]

def bundle_modal_bundles():
	return html.Div([
		dbc.Button(
			'Edit Bundles', 
			id = 'bundle-button-openmodal',
			style={"background-color":"#38160f", "border":"none", "border-radius":"10rem", "font-family":"NotoSans-Regular", "font-size":"0.6rem", "width":"8rem"},
        ),
		dbc.Modal([
			dbc.ModalHeader(html.H2('Bundles', style={"font-size":"2rem"}),),
			dbc.ModalBody(bundle_modal_bundles_body()),
			dbc.ModalFooter(
				dbc.Button('Submit', id = 'bundle-button-closemodal'))
			], id = 'bundle-modal-bundles', size = 'xl', backdrop = 'static')
		],
		style={"padding":"1rem"})

def bundle_modal_bundles_body():
	return html.Div([
		dbc.Row(html.H4("Inpatient", style={"padding-left":"1rem","font-size":"1.5rem"})),
		html.Hr(),
#		dbc.Row(html.H6("Spine, Bone, and Joint")),
		dbc.Row([
			dbc.Col(
				dash_table.DataTable(
					id = 'bundle-table-modal-spine',
					columns = [{"name":'Spine, Bone, and Joint', "id":'Bundle'}] + [{"name":i, "id":i} for i in modal_columns],
#					data = df_bundles[df_bundles['Category'] == "Spine, Bone, and Joint"].to_dict('records'),
					style_data_conditional=conditional_data_style,
			        style_header_conditional = [
			        {'if': {'column_id': 'Bundle'},
			            'textAlign': 'left',
			            'color':'#1357DD',
			            'font-size':'1rem',
			            'font-family':'NotoSans-SemiBold'}
			        ],
				    style_header={
				        'backgroundColor': '#bfd4ff',
				        'fontWeight': 'bold'
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

			        style_as_list_view = True,
			        row_selectable = 'multi',
			        selected_rows = [5],
				), style = {'padding-bottom' :'1rem'}
			),
		], style={"padding-left":"1rem","padding-right":"1rem"}),
#		dbc.Row(html.H6("Kidney")),
		dbc.Row([
			dbc.Col(
				dash_table.DataTable(
					id = 'bundle-table-modal-kidney',
					columns = [{"name":'Kidney', "id":'Bundle'}] + [{"name":'', "id":i} for i in modal_columns],
#					data = df_bundles[df_bundles['Category'] == "Kidney"].to_dict('records'),
					style_data_conditional=conditional_data_style,
			        style_header_conditional = [
			        {'if': {'column_id': 'Bundle'},
			            'textAlign': 'left',
			            'color':'#1357DD',
			            'font-size':'1rem',
			            'font-family':'NotoSans-SemiBold'}
			        ],
				    style_header={
				        'backgroundColor': '#bfd4ff',
				        'fontWeight': 'bold'
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

			        style_as_list_view = True,
			        row_selectable = 'multi',
			        selected_rows = [],
				), style = {'padding-bottom' :'1rem'}
			),
		], style={"padding-left":"1rem","padding-right":"1rem"}),
#		dbc.Row(html.H6("Infectious Disease")),
		dbc.Row([
			dbc.Col(
				dash_table.DataTable(
					id = 'bundle-table-modal-infect',
					columns = [{"name":'Infectious Disease', "id":'Bundle'}] + [{"name":'', "id":i} for i in modal_columns],
#					data = df_bundles[df_bundles['Category'] == "Infectious Disease"].to_dict('records'),
					style_cell={
                        'textAlign': 'center',
                        'font-family':'NotoSans-Regular',
                        'fontSize':10,
                        'height' : 'auto', 
                        'whiteSpace':'normal',
                        'max-width':'3rem',
                        'padding':'10px',
                    },
                    style_cell_conditional=conditional_data_style,
			        style_header_conditional = [
			        {'if': {'column_id': 'Bundle'},
			            'textAlign': 'left',
			            'color':'#1357DD',
			            'font-size':'1rem',
			            'font-family':'NotoSans-SemiBold'}
			        ],
				    style_header={
				        'backgroundColor': '#bfd4ff',
				        'fontWeight': 'bold'
				    },

			        style_as_list_view = True,
			        row_selectable = 'multi',
			        selected_rows = [],
				), style = {'padding-bottom' :'1rem'}
			),
		], style={"padding-left":"1rem","padding-right":"1rem"}),
#		dbc.Row(html.H6("Neurological")),
		dbc.Row([
			dbc.Col(
				dash_table.DataTable(
					id = 'bundle-table-modal-neuro',
					columns = [{"name":'Neurological', "id":'Bundle'}] + [{"name":'', "id":i} for i in modal_columns],
#					data = df_bundles[df_bundles['Category'] == "Neurological"].to_dict('records'),
					style_cell={
                        'textAlign': 'center',
                        'font-family':'NotoSans-Regular',
                        'fontSize':10,
                        'height' : 'auto', 
                        'whiteSpace':'normal',
                        'max-width':'3rem',
                        'padding':'10px',
                    },
                    style_cell_conditional=conditional_data_style,
			        style_header_conditional = [
			        {'if': {'column_id': 'Bundle'},
			            'textAlign': 'left',
			            'color':'#1357DD',
			            'font-size':'1rem',
			            'font-family':'NotoSans-SemiBold'}
			        ],
				    style_header={
				        'backgroundColor': '#bfd4ff',
				        'fontWeight': 'bold'
				    },

			        style_as_list_view = True,
			        row_selectable = 'multi',
			        selected_rows = [1],
				), style = {'padding-bottom' :'1rem'}
			),
		], style={"padding-left":"1rem","padding-right":"1rem"}),
#		dbc.Row(html.H6("Cardiac")),
		dbc.Row([
			dbc.Col(
				dash_table.DataTable(
					id = 'bundle-table-modal-cardi',
					columns = [{"name":'Cardiac', "id":'Bundle'}] + [{"name":'', "id":i} for i in modal_columns],
#					data = df_bundles[df_bundles['Category'] == "Cardiac"].to_dict('records'),
					style_cell={
                        'textAlign': 'center',
                        'font-family':'NotoSans-Regular',
                        'fontSize':10,
                        'height' : 'auto', 
                        'whiteSpace':'normal',
                        'max-width':'3rem',
                        'padding':'10px',
                    },
                    style_cell_conditional=conditional_data_style,
			        style_header_conditional = [
			        {'if': {'column_id': 'Bundle'},
			            'textAlign': 'left',
			            'color':'#1357DD',
			            'font-size':'1rem',
			            'font-family':'NotoSans-SemiBold'}
			        ],
				    style_header={
				        'backgroundColor': '#bfd4ff',
				        'fontWeight': 'bold'
				    },

			        style_as_list_view = True,
			        row_selectable = 'multi',
			        selected_rows = [4],
				), style = {'padding-bottom' :'1rem'}
			),
		], style={"padding-left":"1rem","padding-right":"1rem"}),
#		dbc.Row(html.H6("Pulmonary")),
		dbc.Row([
			dbc.Col(
				dash_table.DataTable(
					id = 'bundle-table-modal-pul',
					columns = [{"name":'Pulmonary', "id":'Bundle'}] + [{"name":'', "id":i} for i in modal_columns],
#					data = df_bundles[df_bundles['Category'] == "Pulmonary"].to_dict('records'),
					style_cell={
                        'textAlign': 'center',
                        'font-family':'NotoSans-Regular',
                        'fontSize':10,
                        'height' : 'auto', 
                        'whiteSpace':'normal',
                        'max-width':'3rem',
                        'padding':'10px',
                    },
                    style_cell_conditional=conditional_data_style,
			        style_header_conditional = [
			        {'if': {'column_id': 'Bundle'},
			            'textAlign': 'left',
			            'color':'#1357DD',
			            'font-size':'1rem',
			            'font-family':'NotoSans-SemiBold'}
			        ],
				    style_header={
				        'backgroundColor': '#bfd4ff',
				        'fontWeight': 'bold'
				    },
			        style_as_list_view = True,
			        row_selectable = 'multi',
			        selected_rows = [],
				), style = {'padding-bottom' :'1rem'}
			),
		], style={"padding-left":"1rem","padding-right":"1rem"}),
#		dbc.Row(html.H6("Gastrointestinal")),
		dbc.Row([
			dbc.Col(
				dash_table.DataTable(
					id = 'bundle-table-modal-gastro',
					columns = [{"name":'Gastrointestinal', "id":'Bundle'}] + [{"name":'', "id":i} for i in modal_columns],
#					data = df_bundles[df_bundles['Category'] == "Gastrointestinal"].to_dict('records'),
					style_cell={
                        'textAlign': 'center',
                        'font-family':'NotoSans-Regular',
                        'fontSize':10,
                        'height' : 'auto', 
                        'whiteSpace':'normal',
                        'max-width':'3rem',
                        'padding':'10px',
                    },
                    style_cell_conditional=conditional_data_style,
			        style_header_conditional = [
			        {'if': {'column_id': 'Bundle'},
			            'textAlign': 'left',
			            'color':'#1357DD',
			            'font-size':'1rem',
			            'font-family':'NotoSans-SemiBold'}
			        ],
				    style_header={
				        'backgroundColor': '#bfd4ff',
				        'fontWeight': 'bold'
				    },
			        style_as_list_view = True,
			        row_selectable = 'multi',
			        selected_rows = [],
				), style = {'padding-bottom' :'1rem'}
			),
		], style={"padding-left":"1rem","padding-right":"1rem"}),
		dbc.Row(html.H4("Outpatient", style={"padding-top":"2rem","padding-left":"1rem","font-size":"1.5rem"})),
		html.Hr(),
		dbc.Row([
			dbc.Col(
				dash_table.DataTable(
					id = 'bundle-table-modal-op',
					columns = [{"name":'Outpatient', "id":'Bundle'}] + [{"name":'', "id":i} for i in modal_columns],
#					data = df_bundles[df_bundles['Category'] == "Outpatient"].to_dict('records'),
					style_cell={
                        'textAlign': 'center',
                        'font-family':'NotoSans-Regular',
                        'fontSize':10,
                        'height' : 'auto', 
                        'whiteSpace':'normal',
                        'max-width':'3rem',
                        'padding':'10px',
                    },
                    style_cell_conditional=conditional_data_style,
			        style_header_conditional = [
			        {'if': {'column_id': 'Bundle'},
			            'textAlign': 'left',
			            'color':'#1357DD',
			            'font-size':'1rem',
			            'font-family':'NotoSans-SemiBold'}
			        ],
				    style_header={
				        'backgroundColor': '#bfd4ff',
				        'fontWeight': 'bold'
				    },

			        style_as_list_view = True,
			        row_selectable = 'multi',
			        selected_rows = [],
				), style = {'padding-bottom' :'1rem'}
			),
		], style={"padding-left":"1rem","padding-right":"1rem"}),

		], style = {"padding" : '1rem',"border-radius":"0.5rem","background-color":"#f5f5f5"})

#app.layout = bundle_modal_bundles()

#@app.callback(
#	Output('bundle-modal-bundles', 'is_open'),
#	[Input('bundle-button-openmodal', 'n_clicks'),
#	Input('bundle-button-closemodal', 'n_clicks')],
#	[State('bundle-modal-bundles', 'is_open')]
#	)
#def open_modal(n1, n2, is_open):
#	if n1 or n2:
#		return not is_open
#	return is_open

#if __name__ == '__main__':
#    app.run_server(host="127.0.0.1",debug=True, port = 8052)