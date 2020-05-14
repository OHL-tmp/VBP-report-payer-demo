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
from modal_bundle import *


app = dash.Dash(__name__)

df_bundles = pd.read_csv("data/df_bundles_30.csv")
#modal_columns = df_bundles.columns[3:8]

def create_layout():
	return html.Div([
		bundle_modal_bundles(),
		bundle_card_bundleselection(),
		
		])

def bundle_card_bundleselection():
	return html.Div([
		dash_table.DataTable(
			id = 'bundle-table-selectedbundles',
			columns = [{"name":i,"id":i} for i in df_bundles.columns[:8]] + [{"name":i,"id":i} for i in df_bundles.columns[9:13]],
			
			data = df_bundles.iloc[[0,1,2]].to_dict('records'),
			style_cell = {'textAlign': 'center', 'padding': '5px', "font-size":"0.7rem", 'height' : 'auto', 'whiteSpace':'normal'},
			style_data_conditional=[
			        {
			            'if': {'column_id': 'Bundle'},
			            'textAlign': 'left'
			        },
			        {
			            'if': {'column_id': 'Category'},
			            'textAlign': 'left'
			        },
			        {
			            'if': {'column_id': 'IP/OP'},
			            'textAlign': 'left'
			        }] + [
			        {
			        	'if':{'column_id':i},
			        	'width':'5%'
			        } for i in df_bundles.columns[3:8]
			        ] + [
			        {
			        	'if':{'column_id':i},
			        	'width':'5%'
			        } for i in df_bundles.columns[9:13]
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
		        'fontWeight': 'bold'
		    },
			style_as_list_view = True,
			)

		], id = 'bundle-card-bundleselection',)

app.layout = create_layout()

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
	Output('bundle-table-selectedbundles', 'data'),
	[Input('bundle-button-closemodal', 'n_clicks')],
	[State('bundle-table-selectedbundles', 'data'),
	State('bundle-table-modal-spine', 'selected_rows'),
	State('bundle-table-modal-kidney', 'selected_rows'),
	State('bundle-table-modal-infect', 'selected_rows'),
	State('bundle-table-modal-neuro', 'selected_rows'),
	State('bundle-table-modal-cardi', 'selected_rows'),
	State('bundle-table-modal-pul', 'selected_rows'),
	State('bundle-table-modal-gastro', 'selected_rows'),
	State('bundle-table-modal-op', 'selected_rows'),]
	)
def update_selected_bundles(n,data,r1,r2,r3,r4,r5,r6,r7,r8):
	if n:

		df1 = df_bundles[df_bundles['Category'] == "Spine, Bone, and Joint"]
		df2 = df_bundles[df_bundles['Category'] == "Kidney"]
		df3 = df_bundles[df_bundles['Category'] == "Infectious Disease"]
		df4 = df_bundles[df_bundles['Category'] == "Neurological"]
		df5 = df_bundles[df_bundles['Category'] == "Cardiac"]
		df6 = df_bundles[df_bundles['Category'] == "Pulmonary"]
		df7 = df_bundles[df_bundles['Category'] == "Gastrointestinal"]
		df8 = df_bundles[df_bundles['Category'] == "Outpatient"]

		dff = pd.concat([df1.iloc[r1],df2.iloc[r2],df3.iloc[r3],df4.iloc[r4],
			df5.iloc[r5],df6.iloc[r6],df7.iloc[r7],df8.iloc[r8]])

		update_data = dff.to_dict('records')
		return update_data
	return data



if __name__ == '__main__':
    app.run_server(host="127.0.0.1",debug=True, port = 8052)