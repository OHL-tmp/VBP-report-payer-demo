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

app = dash.Dash(__name__)

df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

available_indicators = df['Indicator Name'].unique()

app.layout = html.Div([


    html.Div([
        dcc.Graph(
        	figure = {
	        'data': [dict(
	            x=df[df['Indicator Name'] == "Fertility rate, total (births per woman)"]['Value'],
	            y=df[df['Indicator Name'] == "Life expectancy at birth, total (years)"]['Value'],
	            text=df[df['Indicator Name'] == "Life expectancy at birth, total (years)"]['Country Name'],
	            customdata=df[df['Indicator Name'] == "Life expectancy at birth, total (years)"]['Country Name'],
	            mode='markers',
	            marker={
	                'size': 15,
	                'opacity': 0.5,
	                'line': {'width': 0.5, 'color': 'white'}
	            }
        )],
        'layout': dict(
            xaxis={
                'title': "Fertility rate, total (births per woman)",
                'type': 'linear' 
            },
            yaxis={
                'title': "Life expectancy at birth, total (years)",
                'type': 'linear' 
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    },
            id ='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Japan'}]},
            clickData={'points': [{'customdata': 'Japan'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

])


'''@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['Year'] == year_value]

    return '''


def create_time_series(dff, title):
    return {
        'data': [dict(
            x=dff['Year'],
            y=dff['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear'},
            'xaxis': {'showgrid': False}
        }
    }


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'clickData')])
def update_y_timeseries(clickData):
    country_name = clickData['points'][0]['customdata']
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == "Fertility rate, total (births per woman)"]
    title = '<b>{}</b><br>{}'.format(country_name, "Fertility rate, total (births per woman)")
    return create_time_series(dff, title)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData')])
def update_x_timeseries(hoverData):
    dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == "Life expectancy at birth, total (years)"]
    return create_time_series(dff, "Life expectancy at birth, total (years)")


if __name__ == '__main__':
    app.run_server(host="127.0.0.1",debug=True, port = 8052)