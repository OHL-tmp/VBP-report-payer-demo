
import pandas as pd
import plotly
import plotly.graph_objects as go

import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc 
from dash.dependencies import Input, Output, State

from dash_table.Format import Format, Scheme
import dash_table.FormatTemplate as FormatTemplate

df_quality = pd.read_csv("data/quality_setup.csv")

def qualitytable(df):

	table=dash_table.DataTable(
		data=df.to_dict('records'),
		#id=tableid,
		columns=[
		{"name": ["","Measure"], "id": "measure"},
		{"name": ["","Data Source"], "id": "datasource"},
		{"name": [ "ACO Baseline","Value"], "id": "value"},
		{"name": [ "ACO Baseline","Percentile"], "id": "percentile",'type': 'numeric',"format":FormatTemplate.percentage(1),},
		{"name": [ "ACO Baseline","Score"], "id": "score",'type': 'numeric',"format":Format( precision=1, scheme=Scheme.fixed,),},
		{"name": [ "","Cost Implication to Plan"], "id": "costimplication"},
		{"name": [ "","Domain"], "id": "domain"},
		{"name": [ "Weight","Recommended"], "id": "recommended"},
		{"name": [ "Weight","User Defined"], "id": "userdefined",'editable': True},
		],  
		merge_duplicate_headers=True,
		row_selectable='multi',
		selected_rows=list(range(0,23)),
		style_data={
				'color': 'black', 
				'backgroundColor': 'white',
				'font-family': 'NotoSans-CondensedLight',
				#'border':'1px solid grey',
				#'border-bottom': '1px solid grey',
				#'border-top': '1px solid grey',

		},
		style_data_conditional=[
				{ 'if': {'column_id':'measure'}, 
				 'font-weight':'bold', 
				 'textAlign': 'start',
				  },
		]+
		[
			{ 'if': {'row_index':c}, 
					'border':'1px solid grey',
					'border-bottom':'0px',
			 
					  } if c in [0,10,13,20] else
			{'if': {'row_index':c},
					'border':'1px solid grey',
					'border-top':'0px',
			 
					  } if c in [9,12,19,22] else
			{'if': {'row_index':c},
					'border':'1px solid grey',
					'border-bottom':'0px',
					'border-top':'0px',   
					}  for c in range(0,23)


		]+[
			{ 
				'if': {'row_index':c,'column_editable':True}, 
				'backgroundColor': 'white',
				'border':'1px solid blue',
				'border-bottom':'0px',
			 
			} if c in [0,10,13,20] else
			{
				'if': {'row_index':c,'column_editable':True}, 
				'backgroundColor': 'white',
				'border':'1px solid blue',
				'border-top':'0px',
			 
			} if c in [9,12,19,22] else
			{
				'if': {'row_index':c,'column_editable':True},
				'backgroundColor': 'white', 
				'border':'1px solid blue',
				'border-bottom':'0px',
				'border-top':'0px',
			}  for c in range(0,23)

		]+[
			{
				'if': { 'column_id': 'costimplication','filter_query': '{costimplication} eq "Low"'},
				'backgroundColor': 'green',
				'color': 'white',
			},
			{
				'if': { 'column_id': 'costimplication','filter_query': '{costimplication} eq "Mid"' },
				'backgroundColor': 'rgb(246,177,17)',
				'color': 'black',
			},
			{
				'if': { 'column_id': 'costimplication', 'filter_query': '{costimplication} eq "High"'},
				'backgroundColor': 'red',
				'color': "white",
			}
		]+[
			{ 
				'if': {'column_id':'recommended'}, 
				'backgroundColor':'lightgrey', 
				#'textAlign': 'start',
				  },
		
		],
		style_cell={
			'textAlign': 'center',
			'font-family':'NotoSans-Regular',
			'fontSize':12,
			'border':'0px',
			'height': '1.5rem',
		},
		style_cell_conditional=[  
		  {
			'if': {
				'column_id': 'id',
			},
			'display':'none'
			}, 
		],
		style_header={
			'height': '2.5rem',
			'minWidth': '3rem',
			'maxWidth':'3rem',
			'whiteSpace': 'normal',
			'backgroundColor': '#f1f6ff',
			'fontWeight': 'bold',
			'font-family':'NotoSans-CondensedLight',
			'fontSize':14,
			'color': '#1357DD',
			'text-align':'center',
			'border':'0px solid grey',
		},
	)

	return table


app = dash.Dash(__name__)

app.layout = qualitytable(df_quality)

if __name__ == '__main__':
	app.run_server(debug=True,port=8049)