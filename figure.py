
import pandas as pd
import numpy as np
from collections import OrderedDict

import plotly
import plotly.graph_objects as go
import dash_daq as daq

import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc 
from dash.dependencies import Input, Output, State

from dash_table.Format import Format, Scheme
import dash_table.FormatTemplate as FormatTemplate

df_quality = pd.read_csv("data/quality_setup.csv")

df_pt_lv1=pd.read_csv("data/Pt Level V1.csv")
df_pt_epi_phy_lv1=pd.read_csv("data/Pt Episode Phy Level V1.csv")
df_pt_epi_phy_srv_lv1=pd.read_csv("data/Pt Episode Phy Srv Level V1.csv")

df_pt_bundle=pd.read_csv("data/bundled level data.csv")
df_pt_epi_phy_srv_bundle=pd.read_csv("data/bundle service level data.csv")

colors={'blue':'rgba(18,85,222,100)','yellow':'rgba(246,177,17,100)','transparent':'rgba(255,255,255,0)','grey':'rgba(191,191,191,100)',
	   'lightblue':'rgba(143,170,220,100)'}
domain_color={'Patient/Caregiver Experience':'rgb(244,160,159)','Care Coordination/Patient Safety':'rgb(244,160,41)',
			  'Preventive Health':'rgb(18,85,222)','At-Risk Population':'rgb(208,118,203)'}


aco_oppo_drill_mapping = pd.read_csv('data/aco_oppo_drill_mapping.csv')

####################################################################################################################################################################################
######################################################################       Dashboard         #####################################################################################
#################################################################################################################################################################################### 
def waterfall_overall(df): 

	if df.values[0,1]>df.values[0,2]:
		gaincolor='red'
		gain='Losses'
		base=df.values[0,2]
	else:
		gaincolor='green'
		gain-'Savings'
		base=df.values[0,1]

	if df.values[0,1]<10000:
		number_fomart='%{y:,.0f}'
	else:
		number_fomart='%{y:,.0f}'


	fig_waterfall = go.Figure(data=[
		go.Bar(
			name='',
			x=df.columns[0:3].tolist()+[gain], 
			y=df.values[0,0:3].tolist()+[base],
			cliponaxis=False,
			#text=y1_waterfall,
			textposition='outside',
			textfont=dict(color=['black','black','black',colors['transparent']]),
			texttemplate=number_fomart,
			marker=dict(
					color=[colors['blue'],colors['blue'],colors['grey'],colors['transparent']],
					opacity=[1,0.7,0.7,0]
					),
			marker_line=dict( color = colors['transparent'] ),
			hovertemplate='%{y:,.0f}',
			hoverinfo='skip',
			
		),
		go.Bar(  
			name='',
			x=df.columns[0:3].tolist()+[gain], 
			y=[0,0,0,df.values[0,3]],
			#text=y2_waterfall,
			cliponaxis=False,
			textposition='outside',
			textfont=dict(color=[colors['transparent'],colors['transparent'],colors['transparent'],'black']),
			texttemplate=number_fomart,
			marker=dict(
					color=gaincolor,
					opacity=0.7
					),
			hovertemplate='%{y:,.0f}',
			hoverinfo='skip',
		)
	])
	# Change the bar mode
	fig_waterfall.update_layout(
		barmode='stack',
		#title='Revenue Projection',
		plot_bgcolor=colors['transparent'],
		paper_bgcolor=colors['transparent'],
		yaxis = dict(
			showgrid = True, 
			gridcolor =colors['grey'],
			nticks=5,
			showticklabels=True,
			zeroline=True,
			zerolinecolor=colors['grey'],
			zerolinewidth=1,
			range=[0,df.max(axis=1)*1.4]
		),
		showlegend=False,
		modebar=dict(
			bgcolor=colors['transparent'],
		),
		margin=dict(l=10,r=10,b=10,t=50,pad=0),
		font=dict(
			family="NotoSans-Condensed",
			size=12,
			color="#38160f"
		),
	)
	return fig_waterfall


def sharing_split(df): 

	if df.values[0,1]>df.values[0,2]:
		gaincolor='red'
		gain='Losses'
	else:
		gaincolor='green'
		gain-'Savings'

	plan_share=round(df.values[0,4]/df.values[0,3]*100,0)
	aco_share=100-plan_share

	fig_bar = go.Figure(data=[
		go.Bar(
			name='',
			x=[gain], 
			y=[df.values[0,4]],
			#text=y1_waterfall,
			textposition='auto',
			textfont=dict(color='black'),
			texttemplate='%{y:,.0f}',
			marker=dict(
					color=gaincolor,
					opacity=0.5
					),
			width=0.5,
			marker_line=dict( color = colors['transparent'] ),
			hovertemplate='%{y:,.0f}',
			hoverinfo='y',
			
		),
		go.Bar(  
			name='',
			x=[gain], 
			y=[df.values[0,5]],
			#text=y2_waterfall,
			textposition='auto',
			textfont=dict(color='black'),
			texttemplate='%{y:,.0f}',
			marker=dict(
					color=gaincolor,
					opacity=0.3
					),
			width=0.5,
			hovertemplate='%{y:,.0f}',
			hoverinfo='y',
		)
	])

	annotations=[]

	annotations.append(dict(xref='paper', yref='y',
							x=1.15, y=df.values[0,4]/2,
							text="Plan's Share ("+str(plan_share)+' %)',
							font=dict(family='NotoSans-SemiBold', size=14, color='#38160f'),
							showarrow=False,
						   )
					  )

	annotations.append(dict(xref='paper', yref='y',
							x=1.15, y=df.values[0,4]+df.values[0,5]/2,
							text="ACO's Share ("+str(aco_share)+' %)',
							font=dict(family='NotoSans-SemiBold', size=14, color='#38160f'),
							showarrow=False,
						   )
					  )


	# Change the bar mode
	fig_bar.update_layout(
		barmode='stack',
		#title='Revenue Projection',
		plot_bgcolor=colors['transparent'],
		paper_bgcolor=colors['transparent'],
		yaxis = dict(
			showgrid = True, 
			gridcolor =colors['grey'],
			nticks=5,
			showticklabels=True,
			zeroline=True,
			zerolinecolor=colors['grey'],
			zerolinewidth=1,
		),
		showlegend=False,
		modebar=dict(
			bgcolor=colors['transparent']
		),
		margin=dict(l=10,r=100,b=10,t=10,pad=0),
		font=dict(
			family="NotoSans-Condensed",
			size=12,
			color="#38160f"
		),
		annotations=annotations,
	)
	return fig_bar  

def waterfall_target_adj(df):

	if df.values[0,1]<100000:
		number_fomart='%{y:,.0f}'
		base=df['base']
		adj=df['adj']
		suf=''
	else:
		number_fomart='%{y:,.0f}'
		base=df['base']
		adj=df['adj']
		suf=''

	fig_waterfall = go.Figure(data=[
		go.Bar(
			name='',
			x=df['name'], 
			y=base,
			text=df['base'],
			textposition='auto',
			textfont=dict(color=['black',colors['transparent'],colors['transparent'],'black']),
			texttemplate=number_fomart,
			marker=dict(
					color=[colors['grey'],colors['transparent'],colors['transparent'],colors['grey']],
					opacity=[0.5,0,0,0.7]
					),
			marker_line=dict( color = colors['transparent'] ),
			hovertemplate='%{text:,.0f}',
			hoverinfo='skip',
			
		),
		go.Bar(  
			name='',
			x=df['name'].tolist(), 
			y=adj,
			text=df['adj'],
			textposition='outside',
			textfont=dict(color=[colors['transparent'],'black','black',colors['transparent']]),
			texttemplate=number_fomart,
			marker=dict(
					color=[colors['transparent'],colors['blue'],colors['blue'],colors['transparent'],],
					opacity=0.7
					),
			hovertemplate='%{text:,.0f}',
			hoverinfo='skip',
		)
	])
	# Change the bar mode
	fig_waterfall.update_layout(
		barmode='stack',
		plot_bgcolor=colors['transparent'],
		paper_bgcolor=colors['transparent'],
		yaxis = dict(
			showgrid = True, 
			gridcolor =colors['grey'],
			nticks=5,
			showticklabels=True,
			ticksuffix=suf,
			zeroline=True,
			zerolinecolor=colors['grey'],
			zerolinewidth=1,
			range=[0,base.max()*1.2],
		),
		showlegend=False,
		modebar=dict(
			bgcolor=colors['transparent']
		),
		margin=dict(l=10,r=10,b=10,t=10,pad=0),
		font=dict(
			family="NotoSans-Condensed",
			size=12,
			color="#38160f"
		),
	)
	return fig_waterfall

def table_result_dtls(df):

	if len(df)>10:
		select=[5,6,9,10]
	else:
		select=[4,7]

	table=dash_table.DataTable(
		data=df.to_dict('records'),
		columns=[{'id': c, 'name': ''} for c in df.columns[0:2]],
		style_data={
			'whiteSpace': 'normal',
			'height': 'auto'
		},
		style_data_conditional=[
			{'if': {'column_id': df.columns[1],'row_index':c},
			 'color':'red',
			 'font-family':'NotoSans-Condensed',
			} for c in select
		],
		style_cell={
			'textAlign': 'center',
			'font-family':'NotoSans-Condensed',
			'fontSize':14,
			'backgroundColor':"#f7f7f7"
		},
		style_cell_conditional=[
			{'if': {'column_id': df.columns[0]},
			 'width': '20rem',
			 'textAlign':'start',
			 'font-family':'NotoSans-Condensed',
			 'backgroundColor': "#f1f6ff",
			 'color': '#1357DD',
			}, 
			   
		],
		style_header={
			'height': '0rem',
			'backgroundColor': colors['transparent'],
			'color': colors['transparent'],
			'border':'0px'
		},
	)

	return table


def bargraph_h(df):

	fig = go.Figure(data=[
		go.Bar(
			name='',
			x=df['member'].tolist(), 
			y=df['type'].tolist(),
			text="",
			textposition='inside', 
			texttemplate='%{x:,.0f}',
			width=0.3,
			textangle=0,
			marker=dict(
					color=['#1357DD','#1357DD'],
					opacity=[0.7,1]
					),
			orientation='h',
			hoverinfo='skip',
			#hovertemplate='%{x:,.2f}',
		)
	])
	# Change the bar mode
	fig.update_layout(
		
		xaxis=dict(
			ticklen=2,
			tickwidth=5,
			position=0.1,
			#ticksuffix='Mn',
			),
		bargap=0,
		paper_bgcolor=colors['transparent'],
		plot_bgcolor=colors['transparent'],
		showlegend=False,
		margin=dict(l=0,r=0,b=0,t=0,pad=10),
		font=dict(
			family="NotoSans-Condensed",
			size=14,
			color="#38160f"
		),
	)
	return fig

def bar_riskdist(df):
	fig=go.Figure()

	color_bar=['#47b736','#5b9bd5','#ffc000']

	for i in range(0,3):
		fig.add_trace(
			go.Bar(
				name=df.values[i,0],
				x=df.columns[1:3].tolist(),
				y=df.values[i,1:3].tolist(),
				textposition='auto', 
				texttemplate='%{y:,.0f}',
				width=0.5,
				textangle=0,
				marker=dict(
						color=color_bar[i],
						opacity=[1,1]
						),
				hoverinfo='skip',
				#hovertemplate='%{x:,.2f}',
				)

			)

	fig.update_layout(
		barmode='stack',
		
		plot_bgcolor=colors['transparent'],
		paper_bgcolor=colors['transparent'],
		yaxis = dict(
			showgrid = True, 
			gridcolor =colors['grey'],
			nticks=5,
			showticklabels=True,
			zeroline=True,
			zerolinecolor=colors['grey'],
			zerolinewidth=1,
			range=[0,max(df['Baseline'].sum(),df['PY Projected'].sum())*1.2],
		),
		showlegend=True,
		legend=dict(
			orientation='h',
			x=0.3,y=-0.08
		),
		modebar=dict(
			bgcolor=colors['transparent']
		),
		margin=dict(l=0,r=0,b=10,t=20,pad=4),
		font=dict(
			family="NotoSans-Condensed",
			size=12,
			color="#38160f"
		),
	)
	return fig


def waterfall_rs(df):
	fig_waterfall = go.Figure(data=[
		go.Bar(
			name='',
			x=df['name'].tolist(), 
			y=df['base'].tolist(),
			#text=y1_waterfall,
			textposition='auto',
			textfont=dict(color=['black',colors['transparent'],'black']),
			texttemplate='%{y:,.1f}',
			marker=dict(
					color=[colors['blue'],colors['transparent'],colors['grey']],
					opacity=[0.7,0.7,0.7]
					),
			marker_line=dict( color = colors['transparent'] ),
			#hovertemplate='%{y:,.0f}',
			hoverinfo='skip',
			
		),
		go.Bar(  
			name='',
			x=df['name'].tolist(), 
			y=df['adj'].tolist(),
			#text=y2_waterfall,
			textposition='outside',
			textfont=dict(color=[colors['transparent'],'black',colors['transparent']]),
			texttemplate='%{y:,.1f}',
			marker=dict(
					color=colors['yellow'],
					opacity=0.7
					),
			#hovertemplate='%{y:,.0f}',
			hoverinfo='skip',
		)
	])
	# Change the bar mode
	fig_waterfall.update_layout(
		barmode='stack',
		
		plot_bgcolor=colors['transparent'],
		paper_bgcolor=colors['transparent'],
		yaxis = dict(
			showgrid = True, 
			gridcolor =colors['grey'],
			nticks=5,
			showticklabels=True,
			zeroline=True,
			zerolinecolor=colors['grey'],
			zerolinewidth=1,
			range=[0,df['base'].max()*1.2],
		),
		showlegend=False,
		modebar=dict(
			bgcolor=colors['transparent']
		),
		margin=dict(l=10,r=10,b=10,t=20,pad=0),
		font=dict(
			family="NotoSans-Condensed",
			size=12,
			color="#38160f"
		),
	)
	return fig_waterfall

def domain_quality_bubble(df): # 数据，[0,1] ,'Domain' or 'Measure'
	
	fig_domain_perform=go.Figure()
	
	
	for i in range(0,4):

		if i==1:
			selected=0
		else:
			selected=10

		fig_domain_perform.add_trace(
				go.Scatter(     
				x=[i+0.5], 
				y=[df.values[i,1]],
				x0=0,y0=0,
				textposition='middle center',
				texttemplate='%{y:.0%}',
				textfont=dict(
					size=15,
					color='black',

					),
				#text=df_domain_perform[df_domain_perform['Domain']==domain_set[k]][obj],
				mode='markers+text',             
				name=df.values[i,0],
				customdata=[df.values[i,0]],
				#dx=0.1,dy=0.1,
				marker=dict(
					size=[df.values[i,2]*10000],
					color=domain_color[df.values[i,0]],
					opacity=0.7,
					sizemode='area',
				),
				selectedpoints=selected,
				selected=dict(
					marker=dict(
						opacity=1
						)

					),
				unselected=dict(
					marker=dict(
						opacity=0.5
						)

					),
				hoverinfo='name+y',
				

			)
		)
	
	fig_domain_perform.update_layout(
		paper_bgcolor=colors['transparent'],
		plot_bgcolor=colors['transparent'],
		showlegend=True,
		xaxis = dict(
			visible=False,
			range=[0,4],
			rangemode="tozero"
		),
		margin=dict(l=0,r=0,b=50,t=10,pad=0),
		font=dict(
			family="NotoSans-CondensedLight",
			size=12,
			color="#38160f"
		),
		yaxis = dict(
			showgrid = True, 
			gridcolor =colors['grey'],
			showline=True,
			linecolor='grey',
			tickmode='linear',
			dtick=0.2,
			range=[0,1.1],
			tickformat='%',
			showticklabels=True,
			zeroline=True,
			zerolinecolor='grey',
			ticks='inside'
		),
		legend=dict(
			orientation='h',
			x=0,y=-0.05
		),
		#hovermode=True,
		clickmode='event+select',
		modebar=dict(
			bgcolor=colors['transparent']
		),
	)
	return fig_domain_perform


def measure_quality_bar(df,domain):

	
	fig = go.Figure(data=[
		
		go.Scatter(
			name='Target',
			x=[1]*len(df), 
			y=df['measure'].tolist(),
			text="",
			#textposition='none', 
			texttemplate='%{x:.0%}',
			#width=0.3,
			#textangle=0,
			mode='lines',
			marker=dict(
					color='rgba(191,191,191,0.9)',
					opacity=0
					),
			orientation='h',
			hoverinfo='y+x',
			hovertemplate='%{x:.0%}',
		),

		go.Bar(
			name='Annualized',
			x=df['Annualized'].tolist(), 
			y=df['measure'].tolist(),
			text="",
			textposition='none', 
			texttemplate='%{x:.0%}',
			#width=0.3,
			textangle=0,
			marker=dict(
					color=domain_color[domain].replace('rgb','rgba').replace(')',',0.8)'),
					#opacity=0.5
					),
			orientation='h',
			hoverinfo='y+x',
			hovertemplate='%{x:.0%}',
		),

		go.Bar(
			name='YTD',
			x=df['YTD'].tolist(), 
			y=df['measure'].tolist(),
			text="",
			textposition='none', 
			texttemplate='%{x:.0%}',
			#width=0.3,
			textangle=0,
			marker=dict(
					color=domain_color[domain].replace('rgb','rgba').replace(')',',0.5)'),
					#opacity=0.8
					),
			orientation='h',
			hoverinfo='y+x',
			hovertemplate='%{x:.0%}',
		),
		go.Bar(
			name='Baseline',
			x=df['Baseline'].tolist(), 
			y=df['measure'].tolist(),
			text="",
			textposition='none', 
			texttemplate='%{x:.0%}',
			#width=0.3,
			textangle=0,
			marker=dict(
					color='rgba(191,191,191,0.5)',
					#opacity=0.5
					),
			orientation='h',
			hoverinfo='y+x',
			hovertemplate='%{x:.0%}',
		),
	])

	shapes=[]
	shapes.append( dict(type='line',
						xref='x',yref='paper',x0=1,x1=1,y0=0,y1=1,
						line=dict(color=colors['grey'],width=2),
					   )
	
	)

	# Change the bar mode
	fig.update_layout(
		title=dict(
			text=domain,
			font=dict(
			family="NotoSans-Condensed",
			size=16,
			color="#38160f",
			),
			xref='container',
			yref='container',
			x=0.7,
			y=0.98,
			xanchor='center',
			yanchor='middle',
			),
		xaxis=dict(
			title=dict(
				text='Quality Measure Performance(Comparing to target)',
				font=dict(
				family="NotoSans-Condensed",
				size=14,
				color="#38160f",
				),
				standoff=5,
				),
			position=0,
			visible=True,
			range=[0,1.1],
			tickformat='0%'

			),
		barmode='group',
		bargap=0.2,
		bargroupgap=0,
		paper_bgcolor=colors['transparent'],
		plot_bgcolor=colors['transparent'],
		showlegend=True,
		legend=dict(
			orientation='h',
			traceorder='reversed',
			x=-0.5,y=-0.1
		),
		margin=dict(l=300,r=60,b=80,t=20,pad=5,autoexpand=False,),
		font=dict(
			family="NotoSans-Condensed",
			size=14,
			color="#38160f"
		),
		shapes=shapes,
	)
	return fig

def table_quality_dtls(df,domain='all'):

	if domain=='all':
		col=df.columns
		firstcol=df.columns[0]
	else:
		df=df[df['Domain']==domain]
		col=df.columns[1:6]
		firstcol=df.columns[1]

	table=dash_table.DataTable(
		data=df.to_dict('records'),
		columns=[{'id': c, 'name': c} for c in col],
		style_data={
			'whiteSpace': 'normal',
			'height': 'auto'
		},
		style_data_conditional=[
			{'if': {'row_index':len(df)-1},
			 'backgroundColor':'lightgrey',
			 'font-family':'NotoSans-Condensed',
			 'fontWeight':'bold'
			},
			{'if': {'column_id':firstcol},
			 'textAlign':'start',
			},
		],
		style_cell={
			'textAlign': 'center',
			'font-family':'NotoSans-Condensed',
			'fontSize':14,
			'backgroundColor':"#f7f7f7"
		},

		style_header={
			'height': '4rem',
			'backgroundColor': '#f1f6ff',
			'color': '#1357DD',
			'whiteSpace': 'normal',
			'fontWeight': 'bold',
			'font-family':'NotoSans-CondensedLight',
			'fontSize':14,
		
		},
	)

	return table

def pie_cost_split(df):
	labels = df['type']
	values = df['value']

	fig = go.Figure(data=[
		go.Pie(
			labels=labels, 
			values=values, 
			hole=.6,
			textinfo='label+percent',
			textposition='auto',
			texttemplate='%{label}: %{percent:.0%}',
			insidetextorientation='horizontal',
			opacity=0.7,
			marker=dict(
					colors=[colors['yellow'],colors['blue']],#.replace('rgb','rgba').replace(')',',0.7)')
					#
				),
			hovertemplate='%{value:,.0f} <extra>%{label}</extra>',

			)
		])

	fig.update_layout(
		paper_bgcolor=colors['transparent'],
		plot_bgcolor=colors['transparent'],
		legend=dict(
			orientation='h',
			x=0.2,y=-0.2
			),
		margin=dict(l=0,r=0,b=30,pad=0),
		font=dict(
			family='NotoSans-Condensed',
			size=14,
			color='#38160f',

			)
		)

	return fig

def network_cost_stack_h(df):

	n=len(df)

	#df=df[(n-4):n]

	fig = go.Figure(data=[
		
		go.Bar(
			name='In ACO',
			x=df['In ACO'], 
			y=df[df.columns[0]],
			text="",
			textposition='none', 
			texttemplate='%{x:,.0f}',
			#width=0.3,
			textangle=0,
			marker=dict(
					color=colors['blue'],
					opacity=0.7
					),
			orientation='h',
			hoverinfo='name+y+x',
			hovertemplate='%{x:,.0f}',
		),

		go.Bar(
			name='Out of ACO',
			x=df['Out of ACO'], 
			y=df[df.columns[0]],
			text="",
			textposition='none', 
			texttemplate='%{x:,.0f}',
			#width=0.3,
			textangle=0,
			marker=dict(
					color=colors['yellow'],
					#opacity=0.5
					),
			orientation='h',
			hoverinfo='name+y+x',
			hovertemplate='%{x:,.0f}',
		),
	])
		
	# Change the bar mode
	fig.update_layout(
		
		xaxis=dict(
			#position=0,
			visible=True,
			range=[0,(df['Out of ACO']+df['In ACO']).max()*1.02],
#			ticksuffix='Mn',
			tickfont=dict(
			family="NotoSans-Condensed",
			size=10,
			color="#38160f"
		),

			),
		barmode='stack',
		bargap=0.2,
		#bargroupgap=0,
		paper_bgcolor=colors['transparent'],
		plot_bgcolor=colors['transparent'],
		showlegend=False,

		margin=dict(l=0,r=0,b=0,t=0,pad=10,),
		font=dict(
			family="NotoSans-Condensed",
			size=10,
			color="#38160f"
		),
	)

	return fig

####################################################################################################################################################################################
######################################################################    Bundle Dashboard     #####################################################################################
####################################################################################################################################################################################
def waterfall_overall_bundle(df): 

	if df.values[0,1]>df.values[0,2]:
		gaincolor='red'
		gain='Losses'
		
	else:
		gaincolor='green'
		gain-'Savings'
	

	if df.values[0,1]<10000:
		number_fomart='%{y:,.0f}'
	else:
		number_fomart='%{y:,.0f}'


	fig_waterfall = go.Figure(data=[
		go.Bar(
			name='',
			x=df['name'], 
			y=df['base'],
			text=df['base'],
			textposition='outside',
			textfont=dict(color=['black','black','black',colors['transparent'],colors['transparent'],'black']),
			texttemplate='%{y:,.0f}',
			marker=dict(
					color=[colors['blue'],colors['blue'],colors['grey'],colors['transparent'],colors['transparent'],colors['blue']],
					opacity=[1,0.7,0.7,0,0,1]
					),
			marker_line=dict( color = colors['transparent'] ),
			hovertemplate='%{text:,.0f}',
			hoverinfo='skip',
			
		),
		go.Bar(  
			name='',
			x=df['name'], 
			y=df['adj'],
			text=df['adj'],
			cliponaxis=False,
			textposition='outside',
			textfont=dict(color=[colors['transparent'],colors['transparent'],colors['transparent'],'black','black',colors['transparent']]),
			texttemplate='%{y:,.0f}',
			marker=dict(
					color=colors['yellow'],
					opacity=0.7
					),
			hovertemplate='%{text:,.0f}',
			hoverinfo='skip',
		)
	])
	# Change the bar mode
	fig_waterfall.update_layout(
		barmode='stack',
		#title='Revenue Projection',
		plot_bgcolor=colors['transparent'],
		paper_bgcolor=colors['transparent'],
		yaxis = dict(
			showgrid = True, 
			gridcolor =colors['grey'],
			nticks=5,
			showticklabels=True,
#			ticksuffix='M',
			zeroline=True,
			zerolinecolor=colors['grey'],
			zerolinewidth=1,
			range=[0,df['base'].max()*1.2]
		),
		showlegend=False,
		modebar=dict(
			bgcolor=colors['transparent'],
		),
		margin=dict(l=10,r=10,b=10,t=50,pad=0),
		font=dict(
			family="NotoSans-Condensed",
			size=12,
			color="#38160f"
		),
	)
	return fig_waterfall


def measure_quality_bar_bundle(df):

	
	fig = go.Figure(data=[
		
		go.Scatter(
			name='Target',
			x=[1]*len(df), 
			y=df['measure'].tolist(),
			text="",
			#textposition='none', 
			texttemplate='%{x:.0%}',
			#width=0.3,
			#textangle=0,
			mode='lines',
			marker=dict(
					color='rgba(191,191,191,0.9)',
					opacity=0
					),
			orientation='h',
			hoverinfo='y+x',
			hovertemplate='%{x:.0%}',
		),

		go.Bar(
			name='Annualized',
			x=df['Annualized'].tolist(), 
			y=df['measure'].tolist(),
			text="",
			textposition='none', 
			texttemplate='%{x:.0%}',
			#width=0.3,
			textangle=0,
			marker=dict(
					color=colors['blue'].replace('100)','1)'),
					#opacity=0.5
					),
			orientation='h',
			hoverinfo='y+x',
			hovertemplate='%{x:.0%}',
		),

		go.Bar(
			name='YTD',
			x=df['YTD'].tolist(), 
			y=df['measure'].tolist(),
			text="",
			textposition='none', 
			texttemplate='%{x:.0%}',
			#width=0.3,
			textangle=0,
			marker=dict(
					color=colors['blue'].replace('100)','0.5)'),
					#opacity=0.8
					),
			orientation='h',
			hoverinfo='y+x',
			hovertemplate='%{x:.0%}',
		),
		go.Bar(
			name='Baseline',
			x=df['Baseline'].tolist(), 
			y=df['measure'].tolist(),
			text="",
			textposition='none', 
			texttemplate='%{x:.0%}',
			#width=0.3,
			textangle=0,
			marker=dict(
					color='rgba(191,191,191,0.5)',
					#opacity=0.5
					),
			orientation='h',
			hoverinfo='y+x',
			hovertemplate='%{x:.0%}',
		),
	])

	shapes=[]
	shapes.append( dict(type='line',
						xref='x',yref='paper',x0=1,x1=1,y0=0,y1=1,
						line=dict(color=colors['grey'],width=2),
					   )
	
	)

	# Change the bar mode
	fig.update_layout(
		title=dict(
			text='Quality Score',
			font=dict(
			family="NotoSans-Condensed",
			size=16,
			color="#38160f",
			),
			xref='container',
			yref='container',
			x=0.5,
			y=0.98,
			xanchor='center',
			yanchor='middle',
			),
		xaxis=dict(
			title=dict(
				text='Quality Measure Performance',
				font=dict(
				family="NotoSans-Condensed",
				size=14,
				color="#38160f",
				),
				standoff=5,
				),
			position=0,
			visible=True,
			range=[0,1.1],
			tickformat='0%'

			),
		barmode='group',
		bargap=0.2,
		bargroupgap=0,
		paper_bgcolor=colors['transparent'],
		plot_bgcolor=colors['transparent'],
		showlegend=True,
		legend=dict(
			orientation='h',
			traceorder='reversed',
			x=0,y=-0.1
		),
		margin=dict(l=350,r=60,b=80,t=20,pad=5,autoexpand=False,),
		font=dict(
			family="NotoSans-Condensed",
			size=14,
			color="#38160f"
		),
		shapes=shapes,
	)
	return fig

def data_bars_diverging_bundle(df, column,width, color_above='#FF4136', color_below='#3D9970'):

	col_max=df[column].abs().max()
	styles = []
	col_wid=round(width/2,1)+0.2
	for i in df[column].to_list():

		bound_percentage = round(i/col_max/2,4) * 100

		if i>0:
			bound_percentage=min(bound_percentage+50,100)
			styles.append({
				'if': {
					'filter_query': (
						'{{{column}}} = {value}'
					).format(column=column, value=i),
					'column_id': column
				},
				'background': (
					"""
						linear-gradient(90deg,
						white 0%,
						white 50%,
						{color_above} 50%,
						{color_above} {bound_percentage}%,
						white {bound_percentage}%,
						white 100%)
					""".format(bound_percentage=bound_percentage,color_above=color_above)
				),
				'paddingBottom': 2,
				'paddingTop': 2,
				'textAlign':'end',
				'paddingRight':str(col_wid)+'rem',
				'color':color_above,
			})

		else :
			bound_percentage=max(50+bound_percentage,0)
			styles.append({
				'if': {
					'filter_query': (
						'{{{column}}} = {value}' 
					).format(column=column, value=i),
					'column_id': column
				},
				'background': (
					"""
						linear-gradient(90deg,
						white 0%,
						white  {bound_percentage}%,
						{color_below} {bound_percentage}%,
						{color_below} 50%,
						white 50%,
						white 100%)
					""".format(bound_percentage=bound_percentage,color_below=color_below)
				),
				'paddingBottom': 2,
				'paddingTop': 2,
				'textAlign':'start',
				'paddingLeft':str(col_wid)+'rem',
				'color':color_below,
			})
			


	return styles

def table_perform_bundle(df):


	tbl=dash_table.DataTable(
#		id=tableid,
		data=df.to_dict('records'),
		columns=[
		{"name": 'Bundle Name', "id": 'Bundle Name'},
		{"name": 'YTD Cnt', "id": 'YTD Cnt','type':'numeric','format':Format( precision=0, group=',',scheme=Scheme.fixed,)},
#		{"name": 'YTD FFS Cost', "id": 'YTD FFS Cost','type':'numeric','format':FormatTemplate.money(0)},
		{"name": 'Projected PY Gain/Loss', "id": 'Projected PY Gain/Loss','type':'numeric','format':FormatTemplate.money(0)}, 
		{"name": 'Projected PY Gain/Loss %', "id": 'Projected PY Gain/Loss %','type':'numeric','format':FormatTemplate.percentage(1)}, 
		],
		
		sort_action="native",
		sort_mode='single',
		sort_by=[{"column_id":"Projected PY Gain/Loss","direction":"desc"}],
		style_data={
			'whiteSpace': 'normal',
			'height': 'auto'
		},
		style_data_conditional=(
		data_bars_diverging_bundle(df, 'Projected PY Gain/Loss',15) +
		data_bars_diverging_bundle(df, 'Projected PY Gain/Loss %',15)+
		[{'if': {'column_id':'Projected PY Gain/Loss'},
			 
			 'width': '15rem',
			}, 
		{'if': {'column_id': 'Projected PY Gain/Loss %'},
			 
			 'width': '15rem',
			},
#		{'if': {'column_id': 'YTD Cnt'},
#			 
#			 'width': '5rem',
#			},
		{'if': {'column_id': 'Bundle Name'},
			 
			 'textAlign': 'start',
#			 'width': '20rem',
			 'paddingLeft':'10px'
			},

		]
		),
	   
		style_cell={
			'textAlign': 'center',
			'font-family':'NotoSans-Condensed',
			'fontSize':14
		},
		style_header={
			'height': '4rem',
			'minWidth': '3rem',
			'maxWidth':'3rem',
			'whiteSpace': 'normal',
			'backgroundColor': "#f1f6ff",
			'fontWeight': 'bold',
			'font-family':'NotoSans-CondensedLight',
			'fontSize':16,
			'color': '#1357DD',
			'text-align':'center',
		},
	)
	return tbl

def table_bundle_dtls(df):

	table=dash_table.DataTable(
		data=df.to_dict('records'),
		columns=[{'id': c, 'name': c} for c in df.columns],
		style_data={
			'whiteSpace': 'normal',
			'height': 'auto'
		},
		style_data_conditional=[
			{'if': {'column_id':df.columns[0]},
			 'textAlign':'start',
			 'paddingLeft':'10px',
			},
			{'if': {'column_id':df.columns[4],'row_index':4},
			 'color':'green',
			},
			{'if': {'column_id':df.columns[4],'row_index':7},
			 'color':'green',
			},
		]+[

		{'if': {'column_id':c,'row_index':4},
			 'color':'red',
			} for c in df.columns[1:4]


		]+[

		{'if': {'column_id':c,'row_index':7},
			 'color':'red',
			} for c in df.columns[1:4]


		],
		style_cell={
			'textAlign': 'center',
			'font-family':'NotoSans-Condensed',
			'fontSize':14,
#			'backgroundColor':"#f7f7f7"
		},
		style_cell_conditional=[
		{'if': {'column_id':df.columns[c]},
			 'width':'40%',
			} if c==0 else 
		{'if': {'column_id':df.columns[c]},
			 'width':'15%',
			} 
			for c in range(len(df.columns))
		],

		style_header={
			'height': '4rem',
			'backgroundColor': '#f1f6ff',
			'color': '#1357DD',
			'whiteSpace': 'normal',
			'fontWeight': 'bold',
			'font-family':'NotoSans-CondensedLight',
			'fontSize':14,
		
		},
	)

	return table
####################################################################################################################################################################################
######################################################################       DrillDown         ####################################################################################
####################################################################################################################################################################################
def gaugegraph(df,row):
	fig=daq.Gauge(
			#showCurrentValue=True,
			scale={'start': -5, 'interval': 1, 'labelInterval': 2},
			#units="%",
			color={"gradient":True,"ranges":{"#18cc75":[-5,-1],"#39db44":[-1,0],"#aeff78":[0,2],"#ffeb78":[2,3.5],"#ff4d17":[3.5,5]}}, #
			value=df['%'][row]*100,
			label=df['Name'][row],
			labelPosition='top',    
			max=5,
			min=-5,
			size=110,
			style={"font-family":"NotoSans-CondensedLight","font-size":"0.4rem"}
		)  
	return fig

def table_driver_all(df):        
	table=dash_table.DataTable(
		data=df.to_dict('records'),
		#id=tableid,
		columns=[
		{"name": 'Key Driver', "id":'Name' ,'type':'numeric','format':FormatTemplate.percentage(1)},
		{"name": 'Contribution to Overall Performance', "id":'%' ,'type':'numeric','format':FormatTemplate.percentage(1)},
		],  
		sort_action="native",
		sort_mode='single',
		sort_by=[{"column_id":"Contribution to Overall Performance","direction":"desc"},],
		style_data={
			'whiteSpace': 'normal',
			'height': 'auto'
		},
	   
		style_cell={
			'textAlign': 'center',
			'font-family':'NotoSans-Regular',
			'fontSize':12
		},
		style_cell_conditional=[
			{'if': {'column_id': df.columns[0]},
			 
			 'fontWeight': 'bold',

			}, 
			
		],
		style_table={
			'back':  colors['blue'],
		},
		style_header={
			'height': '4rem',
			'minWidth': '3rem',
			'maxWidth':'3rem',
			'whiteSpace': 'normal',
			'backgroundColor': '#f1f6ff',
			'fontWeight': 'bold',
			'font-family':'NotoSans-CondensedLight',
			'fontSize':14,
			'color': '#1357DD',
			'text-align':'center',
		},
	)
	return table

def drilldata_process(d,d1='All',d1v='All',d2='All',d2v='All',d3='All',d3v='All'):
	# d1 is patient cohort dimension, d2 is condition dimension, d3 is service category
	df_pt_lv1_f = df_pt_lv1
	df_pt_epi_phy_lv1_f = df_pt_epi_phy_lv1
	df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1

	if d1v!='All':
		df_pt_lv1_f = df_pt_lv1_f[df_pt_lv1_f[d1]==d1v]
		df_pt_epi_phy_lv1_f = df_pt_epi_phy_lv1_f[(df_pt_epi_phy_lv1_f[d1]==d1v)]
		df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1_f[(df_pt_epi_phy_srv_lv1_f[d1]==d1v)]

	if d2v!='All':
		d2='Clinical Condition'
		df_pt_lv1_f = df_pt_lv1_f[df_pt_lv1_f[d2]==d2v]
		df_pt_epi_phy_lv1_f = df_pt_epi_phy_lv1_f[(df_pt_epi_phy_lv1_f[d2]==d2v)]
		df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1_f[(df_pt_epi_phy_srv_lv1_f[d2]==d2v)]

	if d3v!='All':
		df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1_f[(df_pt_epi_phy_srv_lv1_f[d3]==d3v)]

	d_ori=d

	if d in ['Top 10 Chronic','Top 10 Acute']:

		df_pt_lv1_f = df_pt_lv1_f[df_pt_lv1_f['Clinical Condition Type']==d.replace('Top 10 ','')]
		df_pt_epi_phy_lv1_f = df_pt_epi_phy_lv1_f[(df_pt_epi_phy_lv1_f['Clinical Condition Type']==d.replace('Top 10 ',''))]
		df_pt_epi_phy_srv_lv1_f = df_pt_epi_phy_srv_lv1_f[(df_pt_epi_phy_srv_lv1_f['Clinical Condition Type']==d.replace('Top 10 ',''))]
		d='Clinical Condition'

	if d not in ['Service Category', 'Sub Category']:
		df_agg_pt = df_pt_lv1_f.groupby(by = [d]).agg({'Pt Ct':'nunique', 'Episode Ct':'count'}).reset_index()
		df_agg_clinical = df_pt_epi_phy_lv1_f.groupby(by = [d]).sum().reset_index()
		df_agg_cost = df_pt_epi_phy_srv_lv1_f.groupby(by = [d]).sum().reset_index()

		df_agg_pre = pd.merge(df_agg_pt, df_agg_clinical, how = 'left', on = [d] ).reset_index()
		df_agg = pd.merge(df_agg_cost, df_agg_pre, how = 'left', on = [d] ).reset_index() 
		
	else:           
		df_agg = df_pt_epi_phy_srv_lv1_f.groupby(by = [d]).sum().reset_index()
		df_agg['Pt Ct'] = df_pt_lv1_f['Pt Ct'].agg('nunique')
		df_agg['Episode Ct'] = df_pt_lv1_f['Episode Ct'].agg('count')



	allvalue=df_agg.sum().values

	selected_index_d=[j for j, e in enumerate(df_agg.columns) if e == d][0]

	if d_ori=='Top 10 Chronic':
		allvalue[selected_index_d]='All Chronic'
	elif d_ori=='Top 10 Acute':
		allvalue[selected_index_d]='All Acute'
	else:
		allvalue[selected_index_d]='All'

	
	selected_index=[j for j, e in enumerate(df_agg.columns) if e == 'Pt Ct'][0]
	selected_index_ep=[j for j, e in enumerate(df_agg.columns) if e == 'Episode Ct'][0]

	if d in ['Service Category', 'Sub Category']:
		allvalue[selected_index]=df_agg['Pt Ct'].mean()
		allvalue[selected_index_ep]=df_agg['Episode Ct'].mean()
	elif d in ['Clinical Condition']:
		allvalue[selected_index]=df_pt_lv1_f.agg({'Pt Ct':'nunique'})[0]

	df_agg.loc[len(df_agg)] = allvalue
	df_agg=df_agg.reset_index(drop=True)

	if len(df_agg[df_agg[d]=='Others'])>0:
		otherpos=df_agg[df_agg[d]=='Others'].index[0]
		otherlist=df_agg.loc[otherpos]
		df_agg.loc[otherpos]=df_agg.loc[len(df_agg)-2]
		df_agg.loc[len(df_agg)-2]=otherlist

	df_agg=df_agg.reset_index(drop=True)
  

	df_agg['Patient %'] = df_agg['Pt Ct']/df_pt_lv1_f['Pt Ct'].agg('nunique')
	df_agg['Episode %'] = df_agg['Episode Ct']/ df_pt_lv1_f['Episode Ct'].agg('count')
	df_agg['Cost %'] = df_agg['YTD Total Cost']/(df_agg.tail(1)['YTD Total Cost'].values[0])


	df_agg['YTD Avg Cost/Patient'] = df_agg['YTD Total Cost']/df_agg['Pt Ct']
	df_agg['Annualized Avg Cost/Patient'] = df_agg['Annualized Total Cost']/df_agg['Pt Ct']
	df_agg['Benchmark Avg Cost/Patient'] = df_agg['Benchmark Total Cost']/df_agg['Pt Ct']
	df_agg['Diff % from Benchmark Avg Cost/Patient'] = (df_agg['Annualized Avg Cost/Patient'] - df_agg['Benchmark Avg Cost/Patient'])/df_agg['Benchmark Avg Cost/Patient']


	df_agg['YTD Avg Cost/Episode'] = df_agg['YTD Total Cost']/df_agg['Episode Ct']
	df_agg['Annualized Avg Cost/Episode'] = df_agg['Annualized Total Cost']/df_agg['Episode Ct']
	df_agg['Benchmark Avg Cost/Episode'] = df_agg['Benchmark Total Cost']/df_agg['Episode Ct']
	df_agg['Diff % from Benchmark Avg Cost/Episode'] = (df_agg['Annualized Avg Cost/Episode'] - df_agg['Benchmark Avg Cost/Episode'])/df_agg['Benchmark Avg Cost/Episode']
	df_agg['Avg Cost/Episode Diff % from Best-in-Class'] = (df_agg['Annualized Avg Cost/Episode'] - df_agg['Benchmark Avg Cost/Episode']*0.9)/(df_agg['Benchmark Avg Cost/Episode']*0.9)


	df_agg['Contribution to Overall Performance Difference']=(df_agg['Annualized Total Cost'] - df_agg['Benchmark Total Cost'])/(52495307.84)


	df_agg['YTD Avg Utilization Rate/Patient'] = df_agg['YTD Utilization']/df_agg['Pt Ct']*1000
	df_agg['Annualized Avg Utilization Rate/Patient'] = df_agg['Annualized Utilization']/df_agg['Pt Ct']*1000
	df_agg['Benchmark Avg Utilization Rate/Patient'] = df_agg['Benchmark Utilization']/df_agg['Pt Ct']*1000
	df_agg['Diff % from Benchmark Avg Utilization Rate/Patient'] = (df_agg['Annualized Avg Utilization Rate/Patient'] - df_agg['Benchmark Avg Utilization Rate/Patient'])/df_agg['Benchmark Avg Utilization Rate/Patient']

	df_agg['YTD Avg Utilization Rate/Episode'] = df_agg['YTD Utilization']/df_agg['Episode Ct']*1000
	df_agg['Annualized Avg Utilization Rate/Episode'] = df_agg['Annualized Utilization']/df_agg['Episode Ct']*1000
	df_agg['Benchmark Avg Utilization Rate/Episode'] = df_agg['Benchmark Utilization']/df_agg['Episode Ct']*1000
	df_agg['Diff % from Benchmark Avg Utilization Rate/Episode'] = (df_agg['Annualized Avg Utilization Rate/Episode'] - df_agg['Benchmark Avg Utilization Rate/Episode'])/df_agg['Benchmark Avg Utilization Rate/Episode']

	df_agg['YTD Avg Cost per Unit'] = df_agg['YTD Total Cost']/df_agg['YTD Utilization']
	df_agg['Annualized Avg Cost per Unit'] = df_agg['Annualized Total Cost']/df_agg['Annualized Utilization']
	df_agg['Benchmark Avg Cost per Unit'] = df_agg['Benchmark Total Cost']/df_agg['Benchmark Utilization']
	df_agg['Diff % from Benchmark Unit Cost'] = (df_agg['Annualized Avg Cost per Unit'] - df_agg['Benchmark Avg Cost per Unit'])/df_agg['Benchmark Avg Cost per Unit']

	if d in ['Clinical Condition']:
		df_agg =  pd.concat([df_agg[0:len(df_agg)-1].nlargest(10,'Cost %'),df_agg.tail(1)]).reset_index(drop=True)
		df_agg=df_agg.rename(columns={d:d_ori})

	if d in ['Service Category','Sub Category']:
		if d2v=='All':
			showcolumn=[d_ori,'YTD Avg Cost/Patient','Diff % from Benchmark Avg Cost/Patient','Contribution to Overall Performance Difference','YTD Avg Utilization Rate/Patient','Diff % from Benchmark Avg Utilization Rate/Patient','YTD Avg Cost per Unit','Diff % from Benchmark Unit Cost']
		else:
			showcolumn=[d_ori,'YTD Avg Cost/Episode','Diff % from Benchmark Avg Cost/Episode','Contribution to Overall Performance Difference','YTD Avg Utilization Rate/Episode','Diff % from Benchmark Avg Utilization Rate/Episode','YTD Avg Cost per Unit','Diff % from Benchmark Unit Cost']
	else:
		if d in ['Clinical Condition']:
			df_agg=df_agg.rename(columns={'Diff % from Benchmark Avg Cost/Episode':'Diff % from Benchmark'})
			showcolumn=[d_ori,'Episode Ct','Cost %','YTD Avg Cost/Episode','Diff % from Benchmark','Contribution to Overall Performance Difference']
		
		elif d in ['Managing Physician Specialty',	'Managing Physician']:
			df_agg=df_agg.rename(columns={'Diff % from Benchmark Avg Cost/Episode':'Avg Cost/Episode Diff % from Benchmark'})
			showcolumn=[d_ori,'Episode Ct','YTD Total Cost','Cost %','Avg Cost/Episode Diff % from Benchmark','Contribution to Overall Performance Difference']
		
		else:
		
			df_agg=df_agg.rename(columns={'Diff % from Benchmark Avg Cost/Patient':'Diff % from Benchmark'})
			showcolumn=[d_ori,'Patient %','Cost %','YTD Avg Cost/Patient','Diff % from Benchmark','Contribution to Overall Performance Difference']
		
#	df_agg.to_csv(d+'.csv')
	return df_agg[showcolumn]



def data_bars_diverging(df, column,col_max, color_above='#FF4136', color_below='#3D9970'):

#	col_max=df[column].max()
	styles = []
	for i in df[column].to_list():

		bound_percentage = round(i/col_max/2,4) * 100

		if i>0:
			bound_percentage=bound_percentage+50
			styles.append({
				'if': {
					'filter_query': (
						'{{{column}}} = {value}'
					).format(column=column, value=i),
					'column_id': column
				},
				'background': (
					"""
						linear-gradient(90deg,
						white 0%,
						white 50%,
						{color_above} 50%,
						{color_above} {bound_percentage}%,
						white {bound_percentage}%,
						white 100%)
					""".format(bound_percentage=bound_percentage,color_above=color_above)
				),
				'paddingBottom': 2,
				'paddingTop': 2,
				'textAlign':'start',
				'paddingLeft':'7.5rem',
				'color':color_above,
			})

		else :
			bound_percentage=50+bound_percentage
			styles.append({
				'if': {
					'filter_query': (
						'{{{column}}} = {value}' 
					).format(column=column, value=i),
					'column_id': column
				},
				'background': (
					"""
						linear-gradient(90deg,
						white 0%,
						white  {bound_percentage}%,
						{color_below} {bound_percentage}%,
						{color_below} 50%,
						white 50%,
						white 100%)
					""".format(bound_percentage=bound_percentage,color_below=color_below)
				),
				'paddingBottom': 2,
				'paddingTop': 2,
				'textAlign':'start',
				'paddingLeft':'10.5rem',
				'color':color_below,
			})
			


	return styles

def drilltable_lv1(df,tableid):
	#df['Growth Trend']=df['Trend'].apply(lambda x: '↗️' if x > 0.02 else '↘️' if x<-0.02 else '→' )
	#col=df.columns.tolist()
	if (tableid=='table-patient-drill-lv1') or (tableid=='dashtable_patient_lv1_bundle'):
		sort_col=[{"column_id":"Contribution to Overall Performance Difference","direction":"desc"}]
	else:
		sort_col=[{"column_id":"Cost %","direction":"desc"}]

	if 'Episode Ct' in df.columns:
		col1_format=Format( precision=0,group=',', scheme=Scheme.fixed,)

	else:
		col1_format=FormatTemplate.percentage(1)

	sel_default=len(df)-1

	col_max=max(df['Diff % from Benchmark'].abs().max(),df['Contribution to Overall Performance Difference'].abs().max())

	df['id']=df[df.columns[0]]
	tbl=dash_table.DataTable(
		id=tableid,
		data=df.to_dict('records'),
		columns=[{"name": i, "id": i} if i==df.columns[0] else {"name": i, "id": i,'type':'numeric','format':col1_format} if i==df.columns[1] else {"name": i, "id": i,'type':'numeric','format':FormatTemplate.money(0)} if i==df.columns[3] else {"name": i, "id": i,'type':'numeric','format':FormatTemplate.percentage(1)} for i in df.columns[0:6]],
		row_selectable="single",
		selected_rows=[sel_default],
		#selected_row_ids=['All'],
		sort_action="custom",
		sort_mode='single',
		sort_by=sort_col,
		style_data={
			'whiteSpace': 'normal',
			'height': 'auto'
		},
		style_data_conditional=(
		data_bars_diverging(df, 'Diff % from Benchmark',col_max) +
		data_bars_diverging(df, 'Contribution to Overall Performance Difference',col_max)+
		[{'if': {'column_id':'Diff % from Benchmark'},
			 
			 'width': '20rem',
			}, 
		{'if': {'column_id': 'Contribution to Overall Performance Difference'},
			 
			 'width': '20rem',
			},

		]
		),
	   
		style_cell={
			'textAlign': 'center',
			'font-family':'NotoSans-Condensed',
			'fontSize':14
		},
		style_header={
			'height': '4rem',
			'minWidth': '3rem',
			'maxWidth':'3rem',
			'whiteSpace': 'normal',
			'backgroundColor': "#f1f6ff",
			'fontWeight': 'bold',
			'font-family':'NotoSans-CondensedLight',
			'fontSize':16,
			'color': '#1357DD',
			'text-align':'center',
		},
	)
	return tbl


def drilltable_lv3(df,dimension,tableid,row_select):#row_select: numeric 0 or 1
	
	#df1=df[0:len(df)-1].sort_values(by='Contribution to Overall Performance Difference',ascending=False)
	#df1.append(df[len(df)-1:len(df)])
	#df1['id']=df1[df1.columns[0]]
	#df1.set_index('id', inplace=True, drop=False)

	if row_select==0:
		row_sel=False
	else:
		row_sel='single'

	sel_default=len(df)-1

	if tableid.find('bundle')>=0:
		sort='none'
	else:
		sort='custom'

	df['id']=df[df.columns[0]]
	df.set_index('id', inplace=True, drop=False)

	table_lv3=dash_table.DataTable(
		data=df.to_dict('records'),
		id=tableid,
		columns=[{"name": ["", dimension], "id": dimension},]+
		[{"name": ["Total Cost", df.columns[1]], "id": df.columns[1],'type': 'numeric',"format":FormatTemplate.money(0)},]+
		[{"name": ["Total Cost", 'Diff % from Benchmark'], "id": c,'type': 'numeric',"format":FormatTemplate.percentage(1)} for c in df.columns[2:3]]+
		[{"name": ["Total Cost", c], "id": c,'type': 'numeric',"format":FormatTemplate.percentage(1)} for c in df.columns[3:4]]+  
		[{"name": ["Utilization Rate",  df.columns[4].replace('/', '/1000 ')], "id": df.columns[4],'type': 'numeric',"format":Format( precision=0,group=',', scheme=Scheme.fixed,),},
		{"name": ["Utilization Rate",'Diff % from Benchmark'], "id": df.columns[5],'type': 'numeric',"format":FormatTemplate.percentage(1)},
		{"name": ["Unit Cost",  df.columns[6]], "id":  df.columns[6],'type': 'numeric',"format":FormatTemplate.money(0)},
		{"name": ["Unit Cost",  'Diff % from Benchmark'], "id":  df.columns[7],'type': 'numeric',"format":FormatTemplate.percentage(1)},
		],
		merge_duplicate_headers=True,
		sort_action=sort,
		sort_mode='single',
		sort_by=[{"column_id":"Contribution to Overall Performance Difference","direction":"desc"},],
		row_selectable=row_sel,
		selected_rows=[sel_default],
		#selected_row_ids=['All'],
		style_data={
			'whiteSpace': 'normal',
			'height': 'auto'
		},
	   
		style_cell={
			'textAlign': 'center',
			'font-family':'NotoSans-Regular',
			'fontSize':12
		},
		style_cell_conditional=[
			{'if': {'column_id': df.columns[0]},
			 
			 'fontWeight': 'bold',
			}, 
			
		],
		style_header={
			'height': '4rem',
			'minWidth': '3rem',
			'maxWidth':'3rem',
			'whiteSpace': 'normal',
			'backgroundColor': '#f1f6ff',
			'fontWeight': 'bold',
			'font-family':'NotoSans-CondensedLight',
			'fontSize':14,
			'color': '#1357DD',
			'text-align':'center',
		},
	)
	return table_lv3

def drilltable_physician(df,tableid,row_select):
	#df['Growth Trend']=df['Trend'].apply(lambda x: '↗️' if x > 0.02 else '↘️' if x<-0.02 else '→' )
	#col=df.columns.tolist()

	df['id']=df[df.columns[0]]

	if row_select==0:
		row_sel=False
		export_format='none'

	else:
		row_sel='single'
		export_format='none'

	if tableid.find('bundle')>=0:
		col_max=max(df['Avg Cost/Bundle Diff % from Benchmark'].abs().max(),df['Contribution to Overall Performance Difference'].abs().max())
		col='Avg Cost/Bundle Diff % from Benchmark'
	else:
		col_max=max(df['Avg Cost/Episode Diff % from Benchmark'].abs().max(),df['Contribution to Overall Performance Difference'].abs().max())
		col='Avg Cost/Episode Diff % from Benchmark'
	tbl=dash_table.DataTable(
		id=tableid,
		data=df.to_dict('records'),
		columns=[{"name": i, "id": i} if i==df.columns[0] else {"name": i, "id": i,'type':'numeric','format':Format( precision=0,group=',', scheme=Scheme.fixed,)} if i==df.columns[1] else {"name": i, "id": i,'type':'numeric','format':FormatTemplate.money(0)} if i==df.columns[2] else {"name": i, "id": i,'type':'numeric','format':FormatTemplate.percentage(1)} for i in df.columns[0:6]],
		row_selectable=row_sel,
		selected_rows=[len(df)-1],
		sort_action="custom",
		sort_mode='single',
		sort_by=[{"column_id":"Contribution to Overall Performance Difference","direction":"desc"},],
		page_action="native",
		page_current= 0,
		page_size= 10,
		export_columns='all',
		export_format=export_format,
		export_headers='display',
		style_data={
			'whiteSpace': 'normal',
			'height': 'auto'
		},
		style_data_conditional=(
		data_bars_diverging(df, col,col_max) +
		data_bars_diverging(df, 'Contribution to Overall Performance Difference',col_max)+
		[{'if': {'column_id':col},
			 
			 'width': '20rem',
			}, 
		{'if': {'column_id': 'Contribution to Overall Performance Difference'},
			 
			 'width': '20rem',
			},

		]
		),
	   
		style_cell={
			'textAlign': 'center',
			'font-family':'NotoSans-Condensed',
			'fontSize':14
		},
		style_header={
			'height': '4rem',
			'minWidth': '3rem',
			'maxWidth':'3rem',
			'whiteSpace': 'normal',
			'backgroundColor': "#f1f6ff",
			'fontWeight': 'bold',
			'font-family':'NotoSans-CondensedLight',
			'fontSize':16,
			'color': '#1357DD',
			'text-align':'center',
		},
	)
	return tbl

####################################################################################################################################################################################
######################################################################    Bundle DrillDown     #####################################################################################
####################################################################################################################################################################################

def table_perform_bundle_drill(df1,df2):

	df=pd.merge(df1,df2,how='left',on='Bundle Name')

	df['id']=df['Bundle Name']
	df.set_index('id', inplace=True, drop=False)

	tbl=dash_table.DataTable(
		id='table_perform_drill_bundle',
		data=df.to_dict('records'),
		columns=[
		{"name": [' ','Bundle Name'], "id": 'Bundle Name'},
		{"name": ['','YTD Cnt'], "id": 'YTD Cnt_x','type':'numeric','format':Format( precision=0, group=',',scheme=Scheme.fixed,)},
#		{"name": 'YTD FFS Cost', "id": 'YTD FFS Cost','type':'numeric','format':FormatTemplate.money(0)},
		{"name": ['Projected PY Gain/Loss','Bundle Total'], "id": 'Projected PY Gain/Loss_x','type':'numeric','format':FormatTemplate.money(0)},
		{"name": ['Projected PY Gain/Loss','Bundle Average'], "id": 'Projected PY Gain/Loss_y','type':'numeric','format':FormatTemplate.money(0)},  
		{"name": ['Projected PY Gain/Loss','Projected PY Gain/Loss %'], "id": 'Projected PY Gain/Loss %_x','type':'numeric','format':FormatTemplate.percentage(1)}, 

		],
		merge_duplicate_headers=True,
		row_selectable='single',
		selected_rows=[0],
		sort_action="native",
		sort_mode='single',
		sort_by=[{"column_id":"Projected PY Gain/Loss %_x","direction":"desc"}],
		style_data={
			'whiteSpace': 'normal',
			'height': 'auto'
		},
		style_data_conditional=(
		data_bars_diverging_bundle(df, 'Projected PY Gain/Loss_x',15) +
		data_bars_diverging_bundle(df, 'Projected PY Gain/Loss %_x',15)+
		data_bars_diverging_bundle(df, 'Projected PY Gain/Loss_y',15) +
		[{'if': {'column_id':'Projected PY Gain/Loss_x'},
			 
			 'width': '15rem',
			}, 
		{'if': {'column_id': 'Projected PY Gain/Loss %_x'},
			 
			 'width': '15rem',
			},
		{'if': {'column_id':'Projected PY Gain/Loss_y'},
			 
			 'width': '15rem',
			}, 
		{'if': {'column_id': 'YTD Cnt'},
			 
			 'width': '4rem',
			},
		{'if': {'column_id': 'Bundle Name'},
			 
			 'textAlign': 'start',
			 'width': '25rem',
			 'paddingLeft':'10px'
			},

		]
		),
	   
		style_cell={
			'textAlign': 'center',
			'font-family':'NotoSans-Condensed',
			'fontSize':14
		},
		style_header={
			'height': '4rem',
			'minWidth': '3rem',
			'maxWidth':'3rem',
			'whiteSpace': 'normal',
			'backgroundColor': "#f1f6ff",
			'fontWeight': 'bold',
			'font-family':'NotoSans-CondensedLight',
			'fontSize':16,
			'color': '#1357DD',
			'text-align':'center',
		},
	)
	return tbl


def waterfall_bundle_cost(df): 

	number_fomart='%{y:,.0f}'

	n=len(df)


	fig_waterfall = go.Figure(data=[
		go.Bar(
			name='',
			x=df['Service Category'], 
			y=df['YTD Cost PMPM'].cumsum(),
			#text=y1_waterfall,
			textposition='outside',
			textfont=dict(color=['black']+[colors['transparent']]*(n-2)+['black']),
			texttemplate=number_fomart,
			marker=dict(
					color=[colors['blue']]+[colors['transparent']]*(n-2)+[colors['blue']],
					opacity=0.7
					),
			marker_line=dict( color = colors['transparent'] ),
			hovertemplate='%{y:,.0f}',
			hoverinfo='skip',
			
		),
		go.Bar(  
			name='',
			x=df['Service Category'], 
			y=[0]+(df['YTD Cost PMPM'][1:(n-2)].tolist())+[0],
			#text=y2_waterfall,
			cliponaxis=False,
			textposition='outside',
			textfont=dict(color=[colors['transparent']]+['black']*(n-2)+[colors['transparent']]),
			texttemplate=number_fomart,
			marker=dict(
					color=[colors['transparent']]+[colors['yellow']]*(n-2)+[colors['transparent']],
					opacity=0.7
					),
			hovertemplate='%{y:,.0f}',
			hoverinfo='skip',
		)
	])
	# Change the bar mode
	fig_waterfall.update_layout(
		barmode='stack',
		#title='Revenue Projection',
		plot_bgcolor=colors['transparent'],
		paper_bgcolor=colors['transparent'],
		yaxis = dict(
			showgrid = True, 
			gridcolor =colors['grey'],
			nticks=5,
			showticklabels=True,
			zeroline=True,
			zerolinecolor=colors['grey'],
			zerolinewidth=1,
			range=[0,df['YTD Cost PMPM'].max()*1.2]
		),
		showlegend=False,
		modebar=dict(
			bgcolor=colors['transparent'],
		),
		margin=dict(l=10,r=10,b=10,t=50,pad=0),
		font=dict(
			family="NotoSans-Condensed",
			size=12,
			color="#38160f"
		),
	)
	return fig_waterfall

def drilldata_process_bundle(d,d1='All',d1v='All',d2='All',d2v='All'):
	# d1 is patient cohort dimension, d2 is service category
	df_pt_bundle_f = df_pt_bundle
	df_pt_epi_phy_srv_bundle_f = df_pt_epi_phy_srv_bundle

	if d1v!='All':
		df_pt_bundle_f = df_pt_bundle_f[df_pt_bundle_f[d1]==d1v]
		df_pt_epi_phy_srv_bundle_f = df_pt_epi_phy_srv_bundle_f[(df_pt_epi_phy_srv_bundle_f[d1]==d1v)]
		cost_all=df_pt_epi_phy_srv_bundle_f['Benchmark Total Cost'].sum()

	if d2v!='All':
		df_pt_bundle_f = df_pt_bundle_f[df_pt_bundle_f[d2]==d2v]
		df_pt_epi_phy_srv_bundle_f = df_pt_epi_phy_srv_bundle_f[(df_pt_epi_phy_srv_bundle_f[d2]==d2v)]


	if d not in ['Service Category', 'Sub Category']:
		df_agg_pt = df_pt_bundle_f.groupby(by = [d]).agg({'Episode Count':'sum'}).reset_index()
		df_agg_pt=df_agg_pt.rename(columns={'Episode Count':'Episode Ct'})
		df_agg_cost = df_pt_epi_phy_srv_bundle_f.groupby(by = [d]).sum().reset_index()

		df_agg = pd.merge(df_agg_cost, df_agg_pt, how = 'left', on = [d] ).reset_index() 
		
	else:           
		df_agg = df_pt_epi_phy_srv_bundle_f.groupby(by = [d]).sum().reset_index()
		df_agg['Episode Ct'] = df_pt_bundle_f['Episode Count'].agg('sum')

	allvalue=df_agg.sum().values

	selected_index_d=[j for j, e in enumerate(df_agg.columns) if e == d][0]

	allvalue[selected_index_d]='All'

	selected_index_ep=[j for j, e in enumerate(df_agg.columns) if e == 'Episode Ct'][0]

	if d in ['Service Category', 'Sub Category']:
		allvalue[selected_index_ep]=df_agg['Episode Ct'].mean()

	df_agg.loc[len(df_agg)] = allvalue
  
	df_agg['Bundle %'] = df_agg['Episode Ct']/ (df_agg.tail(1)['Episode Ct'].values[0])
	df_agg['Cost %'] = df_agg['YTD Total Cost']/(df_agg.tail(1)['YTD Total Cost'].values[0])


	df_agg['YTD Avg Cost/Bundle'] = df_agg['YTD Total Cost']/df_agg['Episode Ct']
	df_agg['Annualized Avg Cost/Bundle'] = df_agg['Annualized Total Cost']/df_agg['Episode Ct']
	df_agg['Benchmark Avg Cost/Bundle'] = df_agg['Benchmark Total Cost']/df_agg['Episode Ct']
	df_agg['Diff % from Benchmark Avg Cost/Bundle'] = (df_agg['Annualized Avg Cost/Bundle'] - df_agg['Benchmark Avg Cost/Bundle'])/df_agg['Benchmark Avg Cost/Bundle']


	df_agg['Contribution to Overall Performance Difference']=(df_agg['Annualized Total Cost'] - df_agg['Benchmark Total Cost'])/(cost_all)


	df_agg['YTD Avg Utilization Rate/Bundle'] = df_agg['YTD Utilization']/df_agg['Episode Ct']*1000
	df_agg['Annualized Avg Utilization Rate/Bundle'] = df_agg['Annualized Utilization']/df_agg['Episode Ct']*1000
	df_agg['Benchmark Avg Utilization Rate/Bundle'] = df_agg['Benchmark Utilization']/df_agg['Episode Ct']*1000
	df_agg['Diff % from Benchmark Avg Utilization Rate/Bundle'] = (df_agg['Annualized Avg Utilization Rate/Bundle'] - df_agg['Benchmark Avg Utilization Rate/Bundle'])/df_agg['Benchmark Avg Utilization Rate/Bundle']

	df_agg['YTD Avg Cost per Unit'] = df_agg['YTD Total Cost']/df_agg['YTD Utilization']
	df_agg['Annualized Avg Cost per Unit'] = df_agg['Annualized Total Cost']/df_agg['Annualized Utilization']
	df_agg['Benchmark Avg Cost per Unit'] = df_agg['Benchmark Total Cost']/df_agg['Benchmark Utilization']
	df_agg['Diff % from Benchmark Unit Cost'] = (df_agg['Annualized Avg Cost per Unit'] - df_agg['Benchmark Avg Cost per Unit'])/df_agg['Benchmark Avg Cost per Unit']

	if d in ['Service Category']:

		sort_dim=pd.DataFrame(
			{'Service Category':['Anchor Inpatient Stay','Readmission','Post-Discharge ER','Post-Discharge Professional Services','Post-Discharge Non-ER Outpatient Services','Post-Discharge SNF','Post-Discharge HH','Post-Discharge IRF','All'],
			'ordering':list(range(0,9))}
			)
		df_agg=df_agg.merge(sort_dim,how='left',on='Service Category').sort_values(by='ordering')
		
		showcolumn=[d,'YTD Avg Cost/Bundle','Diff % from Benchmark Avg Cost/Bundle','Contribution to Overall Performance Difference','YTD Avg Utilization Rate/Bundle','Diff % from Benchmark Avg Utilization Rate/Bundle','YTD Avg Cost per Unit','Diff % from Benchmark Unit Cost']
	
	elif d in ['Physician ID']:

		df1=df_agg[0:(len(df_agg)-1)].sort_values(by='Diff % from Benchmark Avg Cost/Bundle',ascending=False)
		df_agg=pd.concat([df1,df_agg.tail(1)])

		df_agg=df_agg.rename(columns={'Diff % from Benchmark Avg Cost/Bundle':'Avg Cost/Bundle Diff % from Benchmark','Episode Ct':'Bundle Ct'})
		showcolumn=[d,'Bundle Ct','YTD Total Cost','Cost %','Avg Cost/Bundle Diff % from Benchmark','Contribution to Overall Performance Difference']
		
	else:
		df1=df_agg[0:(len(df_agg)-1)].sort_values(by='Diff % from Benchmark Avg Cost/Bundle',ascending=False)
		df_agg=pd.concat([df1,df_agg.tail(1)])
		df_agg=df_agg.rename(columns={'Diff % from Benchmark Avg Cost/Bundle':'Diff % from Benchmark'})
		showcolumn=[d,'Bundle %','Cost %','YTD Avg Cost/Bundle','Diff % from Benchmark','Contribution to Overall Performance Difference']	

#	df_agg.to_csv(d+'.csv')
	return df_agg[showcolumn]


####################################################################################################################################################################################
######################################################################      Simulation         ##################################################################################### 
#################################################################################################################################################################################### 
def qualitytable_dropdown_conditional(selected_rows):
	dropdown_conditional=[{
			'if': {
				'column_id': 'tar_user_type',
				'filter_query': '{{rowid}} = {}'.format(c)
			} ,
			'clearable':False,
			'options': [
							{'label': i, 'value': i}
							for i in [
								'Performance',
								'Report',
							]
						]
		} if c in selected_rows else 
		{
			'if': {
				'column_id': 'tar_user_type',
				'filter_query': '{{rowid}} = c'.format(c)
			} ,
			'clearable':False,
			'options': [
							{'label': '', 'value': ''}
						]
		} 
		for c in range(0,23)
		]
	return dropdown_conditional

def qualitytable_data_conditional(selected_rows):
	style_data_conditional=[
				{ 'if': {'column_id':'measure'}, 
				 'font-weight':'bold', 
				 'textAlign': 'start',
				 'width':'14rem',
				 'height':'3rem',
				 'whiteSpace':'normal'
				 #'minWidth': '25rem',
				 #'maxWidth':'25rem',
				  },
		]+[
			{ 'if': {'row_index':c}, 
					'border':'1px solid grey',
					'border-bottom':'0px',
			 
					  } if c in [0,10,14,20] else
			{'if': {'row_index':c},
					'border':'1px solid grey',
					'border-top':'0px solid grey',
			 
					  } if c in [9,13,19,22] else
			{'if': {'row_index':c},
					'border':'1px solid grey',
					'border-bottom':'0px solid grey',
					'border-top':'0px solid grey',   
					}  for c in range(0,23)


		]+[
            { 
                'if': {'row_index':c,'column_id':"domain"}, 
                
                'border-top':'1px solid grey',
                'border-left':'1px solid grey',
                'border-right':'1px solid grey',
                'border-bottom':'0px solid grey',
             
            } if c in [0,10,14,20] else
            {
                'if': {'row_index':c,'column_id':"domain"}, 
                
                'border-bottom':'1px solid grey',
                'border-left':'1px solid grey',
                'border-right':'1px solid grey',
                'border-top':'0px solid grey',
             
            } if c in [9,13,19,22] else
            {
                'if': {'row_index':c,'column_id':"domain"},
                
                'border-left':'1px solid grey',
                'border-right':'1px solid grey',
                'border-bottom':'0px solid grey',
                'border-top':'0px solid grey',
            }  for c in range(0,23)

        ]+[
			{ 
				'if': {'row_index':c,'column_id':"userdefined"}, 
				'backgroundColor': 'rgba(18,85,222,0.1)',
				'font-weight':'bold',
				'border-top':'1px solid blue',
				'border-left':'1px solid blue',
				'border-right':'1px solid blue',
				'border-bottom':'1px solid rgba(18,85,222,0.1)',
			 
			} if c in [0,10,14,20] else
			{
				'if': {'row_index':c,'column_id':"userdefined"}, 
				'backgroundColor': 'rgba(18,85,222,0.1)',
				'font-weight':'bold',
				'border-bottom':'1px solid blue',
				'border-left':'1px solid blue',
				'border-right':'1px solid blue',
				'border-top':'1px solid rgba(18,85,222,0.1)',
			 
			} if c in [9,13,19,22] else
			{
				'if': {'row_index':c,'column_id':"userdefined"},
				'backgroundColor': 'rgba(18,85,222,0.1)', 
				'font-weight':'bold',
				'border-left':'1px solid blue',
				'border-right':'1px solid blue',
				'border-bottom':'1px solid rgba(18,85,222,0.1)',
				'border-top':'1px solid rgba(18,85,222,0.1)',
			}  for c in range(0,23)

		]+[
			{
				'if': { 'column_id': 'tar_user','row_index': c},
				#'backgroundColor': 'green',
				'border': '1px solid blue',
			} if c in selected_rows else
			{
				'if': { 'column_id': 'tar_user','row_index': c},
				#'backgroundColor': 'green',
				'color': 'rgba(0,0,0,0)',
			} for c in range(0,23)
		]+[
			{
				'if': { 'column_id': 'tar_user_type','row_index': c},
				#'backgroundColor': 'green',
				'border': '1px solid blue',
			} if c in selected_rows else
			{
				'if': { 'column_id': 'tar_user_type','row_index': c},
				#'backgroundColor': 'green',
				'color': 'rgba(0,0,0,0)',
			} for c in range(0,23)
		]
	return style_data_conditional


def qualitytable(df,selected_rows=list(range(0,23))):


	table=dash_table.DataTable(
		data=df,
		id='table-measure-setup',
		columns=[
		{"name": ["","Measure"], "id": "measure"},
		{"name": [ "ACO Baseline","ACO"], "id": "aco"},
		{"name": [ "ACO Baseline","Benchmark"], "id": "benchmark"},
		{"name": [ "ACO Baseline","Best-in-Class"], "id": "bic"},
		{"name": [ "Target","Recommend"], "id": "tar_recom"},
		{"name": [ "Target","P4P/P4R"], "id": "tar_user_type",'editable':True,'presentation':'dropdown'},
		{"name": [ "Target","User Defined Value"], "id": "tar_user",'editable': True},
		{"name": [ "Weight","Domain"], "id": "domain"},
		{"name": [ "Weight","Recommend"], "id": "recommended"},
		{"name": [ "Weight","User Defined"], "id": "userdefined",'editable': True},
		#{"name": [ "","id"], "id": "rowid"},
		],
		merge_duplicate_headers=True,
		dropdown_conditional=qualitytable_dropdown_conditional(selected_rows) ,
#		dropdown={
#			'tar_user_type': {
#				'options': [
#					{'label': k, 'value': k}
#					for k in ['Performance','Report']
#				]
#			},
#		},
		row_selectable='multi',
		selected_rows=selected_rows,
		style_data={
				'color': 'black', 
				'backgroundColor': 'rgba(0,0,0,0)',
				'font-family': 'NotoSans-CondensedLight',
				'width':'4rem',
				'minWidth': '4rem',
				'maxWidth':'14rem',
				#'border':'1px solid grey',
				#'border-bottom': '1px solid grey',
				#'border-top': '1px solid grey',

		},
		style_data_conditional=qualitytable_data_conditional(selected_rows),
		style_cell={
			'textAlign': 'center',
			'font-family':'NotoSans-Regular',
			'fontSize':12,
			'border':'0px',
			'height': '1.5rem',
		},

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
			'border':'1px solid grey',
		},
        persistence = True, 
        persistence_type = 'session',
	)

	return table


'''def sim_result_box(df_sim_result):
	### k used for pick color
	k=1 
	
	if len(df_sim_result)==10:
		df=df_sim_result.iloc[[0,3,6,9]]
		k=k-1
		bartext='Baseline:<br><br>'
		x=['Contract w/o<br>VBC Payout','Contract with VBC Payout<br>(Recommended)','Contract with VBC Payout<br>(User Defined)']
		m=0.4
	else:
		df=df_sim_result.iloc[[2,5,8]]
		bartext='Contract w/o<br>VBC Payout:<br><br>'
		x=['Contract with VBC Payout<br>(Recommended)','Contract with VBC Payout<br>(User Defined)']
		m=0.3
	n=len(df)
	
	
	#x=df['Contract Type'].to_list()[1:n]
	median=df['Best Estimate'].to_list()[1:n]
	base=df.values[0,2]
	
	#color for bar and box
	fillcolor=['rgba(226,225,253,0)','rgba(18,85,222,0)','rgba(246,177,17,0)']
	markercolor=['rgba(226,225,253,0.7)','rgba(191,191,191,0.7)','rgba(18,85,222,0.7)','rgba(246,177,17,0.7)']
		
	annotations = []
	
	if df.values[1,3]<df.values[1,4]:
		lowerfence=df['Worst'].to_list()[1:n]
		q1=df['Lower End'].to_list()[1:n]
		q3=df['Higher End'].to_list()[1:n]
		upperfence=df['Best'].to_list()[1:n]
	else:
		lowerfence=df['Best'].to_list()[1:n]
		q1=df['Higher End'].to_list()[1:n]
		q3=df['Lower End'].to_list()[1:n]
		upperfence=df['Worst'].to_list()[1:n]
		
	if df.values[0,7] in ["ACO's PMPM"]:
		suf=''
	elif df.values[0,7] in ["ACO's Margin %"]:
		suf='%'
	else:
		suf='Mn'

	fig_sim =go.Figure()

	fig_sim.add_trace( 
			go.Bar(
			#name='Revenue before adj', 
			x=x,
			y=[base]*(n-1),
			#text=base,
			textposition='none',
			marker=dict(
				color=markercolor[0+k],
				#opacity=0.7,
				line=dict(
					color=fillcolor[0+k],

				)
					   ), 
			),

	)
	
	for i in range(n-1):
		fig_sim.add_trace(
			go.Box(
				x=[x[i]],      
				lowerfence=[lowerfence[i]],
				q1=[q1[i]],
				median=[median[i]],
				q3=[q3[i]],
				upperfence=[upperfence[i]],
				fillcolor=fillcolor[i],
				width=0.2,
				line_width=3,
				marker=dict(
					color=markercolor[i+1+k],
					#opacity=0.7,

				)

			),  
		)
		annotations.append(dict(xref='x', yref='y',axref='x', ayref='y',
						x=0+i, y=df['Best'].to_list()[1:n][i],ax=m+i, ay=df['Best'].to_list()[1:n][i],
						startstandoff=10,
						text='Best: '+str(round(df['Best'].to_list()[1:n][i],1))+suf,
						font=dict(family='NotoSans-CondensedLight', size=12, color='green'),
						showarrow=True,
						arrowhead=2,
						arrowsize=2,
						arrowside='start',
						arrowcolor='green',
					   )
				  )
		annotations.append(dict(xref='x', yref='y',axref='x', ayref='y',
						x=0+i, y=df['Worst'].to_list()[1:n][i],ax=m+i, ay=df['Worst'].to_list()[1:n][i],
						startstandoff=10,
						text='Worst: '+str(round(df['Worst'].to_list()[1:n][i],1))+suf,
						font=dict(family='NotoSans-CondensedLight', size=12, color='red'),
						showarrow=True,
						arrowhead=2,
						arrowsize=2,
						arrowside='start',
						arrowcolor='red',
					   )
				  )
	
	
	annotations.append(dict(xref='paper', yref='y',axref='pixel', ayref='y',
							x=1.05, y=base,ax=1.05,ay=base/3*2,
							standoff=0,
							showarrow=True,
							arrowcolor=colors['grey'],
							arrowwidth=2,
							arrowhead=2,
						   )
					  )
	annotations.append(dict(xref='paper', yref='y',axref='pixel', ayref='y',
							x=1.05, y=0,ax=1.05,ay=base/3,
							standoff=0,
							showarrow=True,
							arrowcolor=colors['grey'],
							arrowwidth=2,
							arrowhead=2,
						   )
					  )
	annotations.append(dict(xref='paper', yref='y',
							x=1.12, y=base/2,
							text=bartext+str(round(base,1))+suf,
							font=dict(family='NotoSans-CondensedLight', size=12, color='#38160f'),
							showarrow=False,
						   )
					  )
	

	
	shapes=[]
	shapes.append( dict(type='line',
						xref='paper',yref='y',x0=1,x1=1.1,y0=base,y1=base,
						line=dict(color=colors['grey'],width=1),
					   )
	
	)
	
	shapes.append( dict(type='line',
						xref='paper',yref='y',x0=1,x1=1.1,y0=0,y1=0,
						line=dict(color=colors['grey'],width=1),
					   )
	
	)
	
	
	fig_sim.update_layout(
			plot_bgcolor=colors['transparent'],
			paper_bgcolor=colors['transparent'],
			bargap=0, 
			yaxis = dict(
				side='left',
				
				showgrid = True, 
				showline=True,
				linecolor=colors['grey'],
				gridcolor =colors['grey'],
				tickcolor =colors['grey'],
				ticks='inside',
				ticksuffix=suf,
				nticks=5,
				showticklabels=True,
				tickfont=dict(
					color=colors['grey']
				),
				zeroline=True,
				zerolinecolor=colors['grey'],
				zerolinewidth=1,
			),
			xaxis = dict(   
				showgrid = True,
				zeroline=True,
				zerolinecolor=colors['grey'],
				zerolinewidth=1,
			),
			showlegend=False,
			modebar=dict(
				bgcolor=colors['transparent']
			),
			margin=dict(l=10,r=100,b=10,t=40,pad=0),
			font=dict(
				family="NotoSans-Condensed",
				size=14,
				color="#38160f"
			),
		hovermode=False,
		annotations=annotations,
		shapes=shapes,
		)
	return fig_sim'''

def sim_result_box(df_sim_result):
 
	df=df_sim_result.iloc[[3,7,11]]
	x=['FFS Contract','ACO Contract<br>(Recommended)','ACO Contract<br>(User Defined)']
	m=0.3
	n=len(df)
	
	median=df['Best Estimate'].to_list()


	#color for bar and box
	fillcolor=['rgba(226,225,253,0)','rgba(18,85,222,0)','rgba(246,177,17,0)']
	markercolor=['rgba(127,127,127,0.7)','rgba(18,85,222,0.7)','rgba(246,177,17,0.7)']
		
	annotations = []
	
	if df.values[1,5]<df.values[1,6]:
		lowerfence=df['Lower End'].to_list()
		q1=df['Best Estimate'].to_list()#Lower End Best Estimate
		q3=df['Best Estimate'].to_list()#Higher End Best Estimate
		upperfence=df['Higher End'].to_list()
	else:
		lowerfence=df['Higher End'].to_list()
		q1=df['Best Estimate'].to_list()#Higher End Best Estimate
		q3=df['Best Estimate'].to_list()#Lower End Best Estimate
		upperfence=df['Lower End'].to_list()
		
	if df.values[0,7] in ["ACO's PMPM"]:
		suf=''
	elif df.values[0,7] in ["ACO's Margin %"]:
		suf='%'
	else:
		suf='Mn'

	fig_sim =go.Figure()
	
	for i in range(n):
		if upperfence[i]>lowerfence[i]:
			fig_sim.add_trace(
				go.Box(
					x=[x[i]],      
					lowerfence=[lowerfence[i]],
					q1=[q1[i]],
					median=[median[i]],
					q3=[q3[i]],
					upperfence=[upperfence[i]],
					fillcolor=fillcolor[i],
					width=0.2,
					line_width=3,
					marker=dict(
						color=markercolor[i],
						#opacity=0.7,

					)

				),  
			)
		else:
			fig_sim.add_trace(
				go.Box(
					x=[x[i]],      
					lowerfence=[upperfence[i]],
					q1=[q3[i]],
					median=[median[i]],
					q3=[q1[i]],
					upperfence=[lowerfence[i]],
					fillcolor=fillcolor[i],
					width=0.2,
					line_width=3,
					marker=dict(
						color=markercolor[i],
						#opacity=0.7,

					)

				),  
			)

#		annotations.append(dict(xref='x', yref='y',axref='x', ayref='y',
#						x=0+i, y=df['Higher End'].to_list()[i],ax=m+i, ay=df['Higher End'].to_list()[i],
#						startstandoff=10,
#						text='Best: '+str(round(df['Higher End'].to_list()[i],1))+suf,
#						font=dict(family='NotoSans-CondensedLight', size=12, color='green'),
#						showarrow=True,
#						arrowhead=2,
#						arrowsize=2,
#						arrowside='start',
#						arrowcolor='green',
#					   )
#				  )
#		annotations.append(dict(xref='x', yref='y',axref='x', ayref='y',
#						x=0+i, y=df['Lower End'].to_list()[i],ax=m+i, ay=df['Lower End'].to_list()[i],
#						startstandoff=10,
#						text='Worst: '+str(round(df['Lower End'].to_list()[i],1))+suf,
#						font=dict(family='NotoSans-CondensedLight', size=12, color='red'),
#						showarrow=True,
#						arrowhead=2,
#						arrowsize=2,
#						arrowside='start',
#						arrowcolor='red',
#					   )
#				  )
	
	
	fig_sim.update_layout(
			plot_bgcolor=colors['transparent'],
			paper_bgcolor=colors['transparent'],
			bargap=0, 
			yaxis = dict(
				side='left',
				
				showgrid = True, 
				showline=True,
				linecolor=colors['grey'],
				gridcolor =colors['grey'],
				tickcolor =colors['grey'],
				ticks='inside',
				ticksuffix=suf,
				nticks=5,
				showticklabels=True,
				tickfont=dict(
					color=colors['grey']
				),
				zeroline=True,
				zerolinecolor=colors['grey'],
				zerolinewidth=1,
			),
			xaxis = dict(   
				showgrid = True,
				zeroline=True,
				zerolinecolor=colors['grey'],
				zerolinewidth=1,
			),
			showlegend=False,
			modebar=dict(
				bgcolor=colors['transparent']
			),
			margin=dict(l=10,r=100,b=10,t=40,pad=0),
			font=dict(
				family="NotoSans-Condensed",
				size=14,
				color="#38160f"
			),
		hovermode=False,
		annotations=annotations,
		)
	return fig_sim

def table_sim_result(df):
	column1=[]
	n=len(df)
	style1=[0,4,8]
	style2=[1,2,5,6,9,10]
	style3=[3,7,11]

	
	#column1=column1+['Contract','w/o','VBC Payout','Contract with','VBC Payout','(Recommended)','Contract with','VBC Payout','(User Defined)']
	column1=column1+['','FFS','Contract', '','', 'ACO Contract','(Recommended)','','','ACO Contract','(User Defined)','']
	df['scenario']=column1

	if df.values[0,7] in ["ACO's PMPM"]:
		header=['Best Estimate','Worst Case','Best Case','Worst Case','Best Case','Variation']
	elif df.values[0,7] in ["ACO's Margin %"]:
		header=['Best Estimate(%)','Worst Case(%)','Best Case(%)','Worst Case(%)','Best Case(%)','Variation(%)']
	else:
		header=['Best Estimate(M)','Worst Case(M)','Best Case(M)','Worst Case(M)','Best Case(M)','Variation(M)']

	if df.values[0,7] =="ACO's Margin %":
		df.iloc[:,2:7]=df.iloc[:,2:7]/100
		num_format=Format( precision=1, scheme=Scheme.percentage,nully='N/A')   
	elif df.values[0,7] =="ACO's PMPM":
		num_format=Format( precision=0,group=',', scheme=Scheme.fixed,nully='N/A')
	else:
		num_format=Format( precision=1,group=',', scheme=Scheme.fixed,nully='N/A')


	df['Variation']=(df['Lower End']-df['Higher End']).abs().tolist()
	df.loc[[0,1,2,4,5,6,8,9,10],['Variation']]=float('nan')
	
   
	table=dash_table.DataTable(
		data=df.to_dict('records'),
		#id=tableid,
		columns=[
		{"name": ["Contract Type","Contract Type"], "id": "scenario"},
		{"name": ["Item","Item"], "id": "Item"},
		{"name": ["",header[0]], "id": "Best Estimate",'type': 'numeric',"format":num_format,},
		#{"name": [ "Full Range",header[1]], "id": "Worst",'type': 'numeric',"format":num_format,},
		#{"name": [ "Full Range",header[2]], "id": "Best",'type': 'numeric',"format":num_format,},
		{"name": [ "Scenario Analysis",header[3]], "id": "Lower End",'type': 'numeric',"format":num_format,},
		{"name": [ "Scenario Analysis",header[4]], "id": "Higher End",'type': 'numeric',"format":num_format,},
		{"name": [ "Scenario Analysis",header[5]], "id": "Variation",'type': 'numeric',"format":num_format,},
		],  
		merge_duplicate_headers=True,
		style_data={
			'whiteSpace': 'normal',
			'height': 'auto'
		},
	   
		style_cell={
			'textAlign': 'center',
			'font-family':'NotoSans-Regular',
			'fontSize':12,
			'border':'0px',
			'height': '1.5rem',
		},
		style_data_conditional=[
			{ 'if': {'row_index':c }, 
			 'color': 'black', 
			 'font-family': 'NotoSans-CondensedLight',
			 'border-top': '1px solid grey',
			 'border-left': '1px solid grey',
			 'border-right': '1px solid grey',
			  } if c in style1 else 
			
			{ 'if': {'row_index':c }, 
			 'color': 'black', 
			 'font-family': 'NotoSans-CondensedBlackItalic',
			 'border-left': '1px solid grey',
			 'border-right': '1px solid grey',
			 'text-decoration':'underline'
			  } if c in style2 else 
			{ "if": {"row_index":c },
			 'font-family': 'NotoSans-CondensedLight',
			 'backgroundColor':'rgba(191,191,191,0.7)',
			 'color': '#1357DD',
			 'fontWeight': 'bold',
			 'border-bottom': '1px solid grey',
			 'border-left': '1px solid grey',
			 'border-right': '1px solid grey',
			  } if c in style3  else 
			{ "if": {"column_id":"scenario" }, 
			 'font-family': 'NotoSans-CondensedLight',
			 'backgroundColor':'white',
			 'color': 'black',
			 'fontWeight': 'bold', 
			 'text-decoration':'none'
			  } for c in range(0,n+1)
		],
		style_table={
			'back':  colors['blue'],
		},
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
			'border':'1px solid grey',
			'text-decoration':'none'
		},
		style_header_conditional=[
			{ 'if': {'column_id':'scenario'},
			'backgroundColor': colors['transparent'],
			'color': colors['transparent'],
			'border':'0px'        
			},
			{ 'if': {'column_id':'Item'},
			'backgroundColor': colors['transparent'],
			'color': colors['transparent'],
			'border':'0px' , 
			'border-right':'1px solid grey' ,
			},
		],
		
		
	)
	return table

def table_factor_doc(df,tableid='factor_doc'):      
	table=dash_table.DataTable(
		data=df.to_dict('records'),
		id=tableid,
		columns=[{"name": c, "id": c} for c in df.columns  ],      
	   
		style_data={
			'height':'auto',
			'width':'3rem',
			'whiteSpace':'normal',
			'textAlign': 'center',
			'font-family':'NotoSans-Regular',
			'fontSize':12,
			
		},
		style_cell_conditional=[
			{'if': {'column_id': df.columns[0]},
			 
			 'fontWeight': 'bold',
			}, 
			
		],
		style_table={
			'back':  colors['blue'],
		},
		style_header={
			'height': '4rem',
			'whiteSpace': 'normal',
			'backgroundColor': '#f1f6ff',
			'fontWeight': 'bold',
			'font-family':'NotoSans-CondensedLight',
			'fontSize':14,
			'color': '#1357DD',
			'text-align':'center',
		},
	)
	return table

def sim_bundle_result_box(df_sim_result):
 
	df=df_sim_result.iloc[[3,7,11]]
	x=['FFS Contract','Bundled Payment<br>(Recommended)','Bundled Payment<br>(User Defined)']
	m=0.3
	n=len(df)

	df.rename(columns={})
	
	median=df[df.columns[2]].to_list()

#	header=['Best Estimate','Worst Case','Best Case']

	#color for bar and box
	fillcolor=['rgba(226,225,253,0)','rgba(18,85,222,0)','rgba(246,177,17,0)']
	markercolor=['rgba(127,127,127,0.7)','rgba(18,85,222,0.7)','rgba(246,177,17,0.7)']
		
	annotations = []
	
	if df.values[1,3]<df.values[1,4]:
		lowerfence=df[df.columns[3]].to_list()
		q1=df[df.columns[2]].to_list()#Lower End Best Estimate
		q3=df[df.columns[2]].to_list()#Higher End Best Estimate
		upperfence=df[df.columns[4]].to_list()
	else:
		lowerfence=df[df.columns[4]].to_list()
		q1=df[df.columns[2]].to_list()#Higher End Best Estimate
		q3=df[df.columns[2]].to_list()#Lower End Best Estimate
		upperfence=df[df.columns[3]].to_list()
		
#	if df.values[0,7] in ["ACO's PMPM"]:
#		suf=''
#	elif df.values[0,7] in ["ACO's Margin %"]:
#		suf='%'
#	else:
#		suf='Mn'
	suf=''

	fig_sim =go.Figure()
	
	for i in range(n):
		if upperfence[i]>lowerfence[i]:
			fig_sim.add_trace(
				go.Box(
					x=[x[i]],      
					lowerfence=[lowerfence[i]],
					q1=[q1[i]],
					median=[median[i]],
					q3=[q3[i]],
					upperfence=[upperfence[i]],
					fillcolor=fillcolor[i],
					width=0.2,
					line_width=3,
					marker=dict(
						color=markercolor[i],
						#opacity=0.7,

					)

				),  
			)
		else:
			fig_sim.add_trace(
				go.Box(
					x=[x[i]],      
					lowerfence=[upperfence[i]],
					q1=[q3[i]],
					median=[median[i]],
					q3=[q1[i]],
					upperfence=[lowerfence[i]],
					fillcolor=fillcolor[i],
					width=0.2,
					line_width=3,
					marker=dict(
						color=markercolor[i],
						#opacity=0.7,

					)

				),  
			)
#		annotations.append(dict(xref='x', yref='y',axref='x', ayref='y',
#						x=0+i, y=df[df.columns[4]].to_list()[i],ax=m+i, ay=df[df.columns[4]].to_list()[i],
#						startstandoff=10,
#						text='Best: '+str(round(df[df.columns[4]].to_list()[i],1))+suf,
#						font=dict(family='NotoSans-CondensedLight', size=12, color='green'),
#						showarrow=True,
#						arrowhead=2,
#						arrowsize=2,
#						arrowside='start',
#						arrowcolor='green',
#					   )
#				  )
#		annotations.append(dict(xref='x', yref='y',axref='x', ayref='y',
#						x=0+i, y=df[df.columns[3]].to_list()[i],ax=m+i, ay=df[df.columns[3]].to_list()[i],
#						startstandoff=10,
#						text='Worst: '+str(round(df[df.columns[3]].to_list()[i],1))+suf,
#						font=dict(family='NotoSans-CondensedLight', size=12, color='red'),
#						showarrow=True,
#						arrowhead=2,
#						arrowsize=2,
#						arrowside='start',
#						arrowcolor='red',
#					   )
#				  )
	
	
	fig_sim.update_layout(
			plot_bgcolor=colors['transparent'],
			paper_bgcolor=colors['transparent'],
			bargap=0, 
			yaxis = dict(
				side='left',
				
				showgrid = True, 
				showline=True,
				linecolor=colors['grey'],
				gridcolor =colors['grey'],
				tickcolor =colors['grey'],
				ticks='inside',
				ticksuffix=suf,
				nticks=5,
				showticklabels=True,
				tickfont=dict(
					color=colors['grey']
				),
				zeroline=True,
				zerolinecolor=colors['grey'],
				zerolinewidth=1,
			),
			xaxis = dict(   
				showgrid = True,
				zeroline=True,
				zerolinecolor=colors['grey'],
				zerolinewidth=1,
			),
			showlegend=False,
			modebar=dict(
				bgcolor=colors['transparent']
			),
			margin=dict(l=10,r=100,b=10,t=40,pad=0),
			font=dict(
				family="NotoSans-Condensed",
				size=14,
				color="#38160f"
			),
		hovermode=False,
		annotations=annotations,
		)
	return fig_sim


def table_bundle_sim_result(df):
	column1=[]
	n=len(df)
	style1=[0,4,8]
	style2=[1,2,5,6,9,10]
	style3=[3,7,11]

	df=df.reset_index(drop=True)

	df['Variation']=(df[ df.columns[3]]-df[ df.columns[4]]).abs().tolist()
	df.loc[[0,1,2,4,5,6,8,9,10],['Variation']]=float('nan')

	
	
	#column1=column1+['Contract','w/o','VBC Payout','Contract with','VBC Payout','(Recommended)','Contract with','VBC Payout','(User Defined)']
	column1=column1+['','FFS','Contract', '','', 'Bundled Payment','(Recommended)','','','Bundled Payment','(User Defined)','']
	df['scenario']=column1

#	if df.values[0,7] in ["ACO's PMPM"]:
#		header=['Best Estimate','Low','High','Low','High']
#	elif df.values[0,7] in ["ACO's Margin %"]:
#		header=['Best Estimate(%)','Low(%)','High(%)','Low(%)','High(%)']
#	else:
#		header=['Best Estimate(Mn)','Low(Mn)','High(Mn)','Low(Mn)','High(Mn)']
	header=['Best Estimate','Worst Case','Best Case']

#	if df.values[0,7] =="ACO's Margin %":
#		df.iloc[:,2:7]=df.iloc[:,2:7]/100
#		num_format=Format( precision=1, scheme=Scheme.percentage,nully='N/A')   
#	else:
#		num_format=Format( precision=1, scheme=Scheme.fixed,nully='N/A')
	
	num_format=Format( precision=0, group=',',scheme=Scheme.fixed,nully='N/A')
   
	table=dash_table.DataTable(
		data=df.to_dict('records'),
		#id=tableid,
		columns=[
		{"name": ["Contract Type","Contract Type"], "id": "scenario"},
		{"name": ["Item","Item"], "id": "Item"},
		{"name": ["",header[0]], "id": df.columns[2],'type': 'numeric',"format":num_format,},
		#{"name": [ "Full Range",header[1]], "id": "Worst",'type': 'numeric',"format":num_format,},
		#{"name": [ "Full Range",header[2]], "id": "Best",'type': 'numeric',"format":num_format,},
		{"name": [ "Scenario Analysis",header[1]], "id": df.columns[3],'type': 'numeric',"format":num_format,},
		{"name": [ "Scenario Analysis",header[2]], "id": df.columns[4],'type': 'numeric',"format":num_format,},
		{"name": [ "Scenario Analysis",'Variation'], "id": 'Variation','type': 'numeric',"format":num_format,},
		],  
		merge_duplicate_headers=True,
		style_data={
			'whiteSpace': 'normal',
			'height': 'auto'
		},
	   
		style_cell={
			'textAlign': 'center',
			'font-family':'NotoSans-Regular',
			'fontSize':12,
			'border':'0px',
			'height': '1.5rem',
		},
		style_data_conditional=[
			{ 'if': {'row_index':c }, 
			 'color': 'black', 
			 'font-family': 'NotoSans-CondensedLight',
			 'border-top': '1px solid grey',
			 'border-left': '1px solid grey',
			 'border-right': '1px solid grey',
			  } if c in style1 else 
			
			{ 'if': {'row_index':c }, 
			 'color': 'black', 
			 'font-family': 'NotoSans-CondensedBlackItalic',
			 'border-left': '1px solid grey',
			 'border-right': '1px solid grey',
			 'text-decoration':'underline'
			  } if c in style2 else 
			{ "if": {"row_index":c },
			 'font-family': 'NotoSans-CondensedLight',
			 'backgroundColor':'rgba(191,191,191,0.7)',
			 'color': '#1357DD',
			 'fontWeight': 'bold',
			 'border-bottom': '1px solid grey',
			 'border-left': '1px solid grey',
			 'border-right': '1px solid grey',
			  } if c in style3  else 
			{ "if": {"column_id":"scenario" }, 
			 'font-family': 'NotoSans-CondensedLight',
			 'backgroundColor':'white',
			 'color': 'black',
			 'fontWeight': 'bold', 
			 'text-decoration':'none'
			  } for c in range(0,n+1)
		],
		style_table={
			'back':  colors['blue'],
		},
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
			'border':'1px solid grey',
			'text-decoration':'none'
		},
		style_header_conditional=[
			{ 'if': {'column_id':'scenario'},
			'backgroundColor': colors['transparent'],
			'color': colors['transparent'],
			'border':'0px'        
			},
			{ 'if': {'column_id':'Item'},
			'backgroundColor': colors['transparent'],
			'color': colors['transparent'],
			'border':'0px' , 
			'border-right':'1px solid grey' ,
			},
		],
		
		
	)
	return table


def bundle_measure_setup(df):
	table=dash_table.DataTable(
		data = df.to_dict('records'),
		id = 'bundle-table-selectedmeas',
		columns = [
		{"name":['','Measure'],"id":'Measure'}, 
		{"name": ["", "Applicable Episodes"], "id": "Applicable Episodes"},
		{"name": ["Baseline", "Provider"], "id": "provider"},
		{"name": ["Baseline", "Benchmark"], "id": "benchmark"},
		{"name": ["Baseline", "Best-in-Class"], "id": "bic"},
		{"name": ["Target", "Recommended"], "id": "recommended"},
		{"name": ["Target", "User Defined"], "id": "user defined",'editable':True},

		],
		merge_duplicate_headers=True,
		row_selectable='multi',
		selected_rows=list(range(0,len(df))),       
		# style_cell = {'textAlign': 'center', 'padding': '5px', "font-size":"0.7rem", 'height' : 'auto', 'whiteSpace':'normal'},
		style_data_conditional=[
				{
					'if': {'column_id': 'Measure'},
					'textAlign': 'left',
					'width':'30%',
				},
			   
				{
					'if': {'column_id': 'user defined'},
					'border':'1px solid blue',
					'backgroundColor':'white',

				},
				

				],

		style_header={
			'backgroundColor': '#bfd4ff',
			'fontWeight': 'bold',
			'font-family':'NotoSans-Condensed',
			'border':'1px solid white',
		},
		style_data={
			'whiteSpace': 'normal',
			'height': 'auto',
			'backgroundColor':'rgba(0,0,0,0)',
			'border-left':'0px',
			'border-right':'0px',
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
		#style_as_list_view = True,
		)
	return table




#####   carve out figure   #####
def data_bars_sensitivity(df, column,col_max, color='#FF4136'):

#   col_max=df[column].max()
    styles = []
    for i in df[column].to_list():

        bound_percentage = round(i/col_max,4) * 100

        if i>0:
            styles.append({
                'if': {
                    'filter_query': (
                        '{{{column}}} = {value}'
                    ).format(column=column, value=i),
                    'column_id': column
                },
                'background': (
                    """
                        linear-gradient(90deg,
                        {color} 0%,
                        {color} {bound_percentage}%,
                        white {bound_percentage}%,
                        white 100%)
                    """.format(bound_percentage=bound_percentage,color=color)
                ),
                'paddingBottom': 2,
                'paddingTop': 2,
                'textAlign':'start',
                'paddingLeft':str(round(15*bound_percentage/100+0.3,1))+'rem',
                'color':color,
            })

        else :
            bound_percentage = 100+bound_percentage
            styles.append({
                'if': {
                    'filter_query': (
                        '{{{column}}} = {value}' 
                    ).format(column=column, value=i),
                    'column_id': column
                },
                'background': (
                    """
                        linear-gradient(90deg,
                        white 0%,
                        white  {bound_percentage}%,
                        {color} {bound_percentage}%,
                        {color} 100%)
                    """.format(bound_percentage=bound_percentage,color=color)
                ),
                'paddingBottom': 2,
                'paddingTop': 2,
                'textAlign':'start',
                'paddingLeft':str(round(15*bound_percentage/100-2.8,1))+'rem',
                'color':color,
            })
            


    return styles

def tbl_carve_out_dtl(df):
    col_max=round(max(df['upper variation'].max(),abs(df['lower variation'].min()))/0.75,2)

    tbl=dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[
            {"name": "Type of Services", "id": "TypeofServices"},
            {"name": "Average PMPM", "id": "Average PMPM",'type': 'numeric',"format":FormatTemplate.money(0)},
            {"name": "% of Total Cost", "id": "% of Total Cost"},
            {"name": "Variation in total cost if the service is included", "id": "lower variation",'type': 'numeric',"format":FormatTemplate.percentage(1)},
            {"name": "Variation in total cost if the service is included", "id": "upper variation",'type': 'numeric',"format":FormatTemplate.percentage(1)},
        ],
        merge_duplicate_headers=True,
        style_data_conditional=(
            data_bars_sensitivity(df, 'lower variation',0.04) +
            data_bars_sensitivity(df, 'upper variation',0.04)+
            [{'if': {'column_id':'lower variation'},
                 
                 'width': '15rem',
                }, 
            {'if': {'column_id': 'upper variation'},
                 
                 'width': '15rem',
                },

            ]+[
                { 
                    'if': {'row_index':c}, 
                    
                    'border-top':'2px solid blue',
                    'border-left':'2px solid blue',
                    'border-right':'2px solid blue',
                    'border-bottom':'0px solid grey',
                    'height': '1rem'
                 
                } if c in [0,3,6,9] else
                {
                    'if': {'row_index':c}, 
                    
                    'border-bottom':'2px solid blue',
                    'border-left':'2px solid blue',
                    'border-right':'2px solid blue',
                    'border-top':'0px solid grey',
                    'height': '1rem'
                 
                } if c in [2,5,8,11] else
                {
                    'if': {'row_index':c},
                    
                    'border-left':'2px solid blue',
                    'border-right':'2px solid blue',
                    'border-bottom':'0px solid grey',
                    'border-top':'0px solid grey',
                }  for c in range(12)

            ]+[
                { 
                    'if': {'row_index':c}, 
                    
                    'border-top':'1px solid grey',
                    'border-left':'1px solid grey',
                    'border-right':'1px solid grey',
                    'border-bottom':'0px solid grey',
                    'height': '1rem'
                 
                } if c in [9,12,15,18,21,24] else
                {
                    'if': {'row_index':c}, 
                    
                    'border-bottom':'1px solid grey',
                    'border-left':'1px solid grey',
                    'border-right':'1px solid grey',
                    'border-top':'0px solid grey',
                    'height': '1rem'
                 
                } if c in [11,14,17,20,23,26] else
                {
                    'if': {'row_index':c},
                    
                    'border-left':'1px solid grey',
                    'border-right':'1px solid grey',
                    'border-bottom':'0px solid grey',
                    'border-top':'0px solid grey',
                }  for c in range(9,27)

            ]+[
                {
                    'if': { 'column_id': c},
                    'border-right':'1px solid grey',
                } if c in ['Type of Services'] else
                {
                    'if': { 'column_id': c},
                    'border-left':'1px solid grey',
                    'border-right':'1px solid grey',
                } for c in ['Average PMPM','% of Total Cost','lower variation']
            ]
            ),
           
            style_cell={
                'textAlign': 'center',
                'font-family':'NotoSans-Condensed',
                'fontSize':14,
                'border':'0px',
                'height': '3rem'
            },

            style_header={
                'height': '4rem',
                'minWidth': '3rem',
                'maxWidth':'3rem',
                'whiteSpace': 'normal',
                'backgroundColor': "#f1f6ff",
                'fontWeight': 'bold',
                'font-family':'NotoSans-CondensedLight',
                'fontSize':14,
                'color': '#1357DD',
                'text-align':'center',
                'border':'1px solid grey',
            },
    )
    
    return tbl



### opportunities ###
def bubble_bundle(df):

    fig_domain_perform = go.Figure()

    fig_domain_perform.add_trace(
            go.Scatter(        
            x=df['volume'] , 
            y=df['opportunity'] ,
            x0=0,y0=0,
            text=df['bundle'],
            mode='markers',
            customdata=df['bundle'],             
            #name=domain_set[k],
            #dx=0.1,dy=0.1,
            marker=dict(
                size=df['volume']*15,
                color=colors['blue'],
                opacity=0.8,
                sizemode='area',
            ),
            selectedpoints=[18],
            selected=dict(
                marker=dict(
                    opacity=0.8,
                    color='rgb(246,177,17)'
                    )

                ),
            unselected=dict(
                marker=dict(
                    opacity=0.8
                    )

                ),

        )
    )

    annotations = []
    annotations.append(dict(xref='paper', yref='paper',
                            x=0, y=1,
                            text='Cost Reduction Opportunity<br>(as a % of total bundle cost)',
                            font=dict(family='NotoSans-CondensedLight', size=14, color='#38160f'),
                            showarrow=False))
    annotations.append(dict(xref='paper', yref='paper',
                            x=1, y=0.12,
                            text='Bundle Volume',
                            font=dict(family='NotoSans-CondensedLight', size=14, color='#38160f'),
                            showarrow=False))
    annotations.append(dict(xref='paper', yref='paper',
                            x=0.847, y=0.98,
                            text='Ideal Target',
                            font=dict(family='NotoSans-CondensedLight', size=16, color='#38160f'),
                            showarrow=False))

    fig_domain_perform.update_layout(
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        annotations=annotations,
        shapes = [{'type':'rect','layer':'below','fillcolor':'rgba(246,177,17,0.4)',
        'x0':150,'x1':300 ,'y0':0.03,'y1':0.06, 'line':{'color':'rgba(246,177,17,0.4)'}}],
        showlegend=False,
        xaxis = dict(
            tickmode='linear',
            #range=[0,0.5],
            tick0=0,
            dtick=50,
            showticklabels=True,
            #tickformat='%',
            position=0,

            showgrid=True,
            gridcolor =colors['grey'],

            zeroline=False,
            zerolinecolor='grey',
            rangemode="tozero"
        ),
        margin=dict(l=0,r=0,b=50,t=10,pad=0),
        font=dict(
            family="NotoSans-CondensedLight",
            size=12,
            color="#38160f"
        ),
        yaxis = dict(
            showgrid = True, 
            gridcolor =colors['grey'],
            showline=True,
            linecolor='grey',
            tickmode='linear',
            dtick=0.02,
            range=[-0.02,0.06],
            tickformat='%',
            showticklabels=True,
            zeroline=True,
            zerolinecolor='grey',
            ticks='inside'
        ),
        #hovermode=True,
        clickmode='event+select',
        modebar=dict(
            bgcolor=colors['transparent']
        ),
    )
    return fig_domain_perform    

def bundle_trend(df):
    
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df['year'], 
            y=df['volume'],
            #name="Monthly Growth Rate",
            marker=dict(color=colors['blue']),
            mode='lines+markers+text',
            line=dict(color=colors['blue']),
            textfont=dict(
            family="NotoSans-CondensedLight",
            size=12,
            color="black"
            ),
            text=df['volume'],
            textposition='top center',
            texttemplate='%{y:,.0f}',
            hoverinfo='skip',
            #hovertemplate='%{y:,.0f}',
        ),
    )
    fig.update_layout(
        #title='Monthly and Cumulative Revenue',
        plot_bgcolor=colors['transparent'],
        paper_bgcolor=colors['transparent'],
        showlegend=False,
        xaxis = dict(
            gridcolor =colors['grey'],
            dtick=1,
            showticklabels=True,
        ),
        yaxis = dict(
            showgrid = True, 
            gridcolor =colors['grey'],
            nticks=5,
            showticklabels=True,
            rangemode="tozero",
            zeroline=True,
            zerolinecolor='grey',
            range = [0, 300],
        ),
        modebar=dict(
            bgcolor=colors['transparent']
        ),        
        margin=dict(l=10,r=10,b=100,t=40,pad=0),
        font=dict(
            family="NotoSans-Condensed",
            size=12,
            color="#38160f"
        ),
    )
    return fig

def bundle_avgcost(df):
    fig = go.Figure(data=[
        go.Bar(
            name='',
            x=['Provider Group','Benchmark','Best-in-Class'], 
            y=df[['provider','benchmark','best_in_class']].values[0].tolist(),
            text="",
            textposition='inside', 
            texttemplate='%{y:$,.0f}',
            width=0.3,
            textangle=0,
            marker=dict(
                    color=['rgba(246,177,17,1)','rgba(18,85,222,1)','rgba(143,170,220,1)'],
                    opacity=[0.7,0.7,0.7]
                    ),
            orientation='v',
            hoverinfo='skip',
            #hovertemplate='%{x:,.2f}',
        )
    ])
    # Change the bar mode
    fig.update_layout(
        
        yaxis=dict(
            #ticklen=2,
            #tickwidth=5,
            tickformat = '$',
            #position=0.1,
            #ticksuffix='Mn',
            ),
        #bargap=0,
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        showlegend=False,
        margin=dict(l=0,r=0,b=0,t=0,pad=10),
        font=dict(
            family="NotoSans-Condensed",
            size=14,
            color="#38160f"
        ),
        height=360
    )
    return fig

def bundle_svccost(df):

    df_figure = df.sort_values(by='best')

    colmax=df_figure['bench'].max()*1.2

    fig = go.Figure(data=[
    go.Bar(
        name='Compare with Benchmark',
        x=df_figure['bench'], 
        y=df_figure['service'],
        text="",
        textposition='outside',#'inside', 
        texttemplate='%{x:$,.0f}',
        #width=0.3,
        textangle=0,
        marker=dict(
                color=colors['blue'],
                opacity=0.8
                ),
        orientation='h',
        hoverinfo='y+x',
        hovertemplate='%{x:$,.0f}',
    ),

    go.Bar(
        name='Compare with Best-in-Class',
        x=df_figure['best'], 
        y=df_figure['service'],
        text="",
        textposition='outside',#'inside', 
        texttemplate='%{x:$,.0f}',
        #width=0.3,
        textangle=0,
        marker=dict(
                color=colors['lightblue'],
                opacity=0.8
                ),
        orientation='h',
        hoverinfo='y+x',
        hovertemplate='%{x:$,.0f}',
    ),
    ])

    shapes=[]
    shapes.append(dict(type='line',
                        xref='x',yref='paper',x0=0,x1=0,y0=0,y1=1,
                        line=dict(color=colors['grey'],width=2),
                       )
    
    )

    # Change the bar mode
    fig.update_layout(        
        xaxis=dict(
            position=0,
            visible=True,
            range=[-colmax,colmax],
            tickformat='$'
            ),
        barmode='group',
        bargap=0.2,
        bargroupgap=0,
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        showlegend=True,
        legend=dict(
            orientation='h',
            traceorder='reversed',
            x=0,y=-0.1
        ),
        margin=dict(l=120,r=120,b=80,t=20,pad=5,autoexpand=False,),
        font=dict(
            family="NotoSans-Condensed",
            size=14,
            color="#38160f"
        ),
        shapes=shapes,
        height=400
    )
    return fig

def bundle_vertical(df, numformat = 'int'):

    if numformat == 'pct':
        df_figure = df.sort_values(by='est_costpct')
        numformat =  '%{x:.1%}'
        xname = 'est_costpct'
        yname = 'reduction_oppo'
        tickform = '.1%'
    else:
        df_figure = df.sort_values(by='reduct_amount',ascending=False).head(10).sort_values(by='reduct_amount')
        numformat =  '%{x:$,.0f}'
        xname = 'reduct_amount'
        yname = 'bundle'
        tickform = '$'

    fig = go.Figure(data=[
        go.Bar(
            name='',
            x=df_figure[xname], 
            y=df_figure[yname],
            text="",
            textposition='inside', 
            texttemplate = numformat,
            width=0.7,
            textangle=0,
            marker=dict(
                    color='#1357DD',
                    opacity=0.7
                    ),
            orientation='h',
            hoverinfo='y+x',#'y',
            hovertemplate=numformat, #'%{x:,.0f}',
        )
    ])
    
    fig.update_layout(
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        showlegend=False,
        xaxis = dict(
            #dtick=1,
            rangemode="tozero",
            tickformat=tickform,
        ),
        margin=dict(l=0,r=0,b=30,t=30,pad=10),
        font=dict(
            family="NotoSans-Condensed",
            size=14,
            color="#38160f"
        ),
        height=360
    )
    return fig

# aco
def aco_vertical(df, numformat = 'int'):

    if numformat == 'pct':
        df_figure = df.sort_values(by='costpct')
        numformat =  '%{x:.1%}'
        xname = 'costpct'
        yname = 'reduction_oppo'
        tickform = '.1%'
    else:
        df_figure = df.sort_values(by='pmpm')
        numformat =  '%{x:$,.0f}'
        xname = 'pmpm'
        yname = 'reduction_oppo'
        tickform = '$'

    fig = go.Figure(data=[
        go.Bar(
            name='',
            x=df_figure[xname], 
            y=df_figure[yname],
            text="",
            textposition='inside', 
            texttemplate = numformat,
            width=0.5,
            textangle=0,
            marker=dict(
                    color='#1357DD',
                    opacity=0.7
                    ),
            orientation='h',
            hoverinfo='y+x',#'y',
            #hovertemplate='%{x:,.0f}',
        )
    ])
    
    fig.update_layout(
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        showlegend=False,
        xaxis = dict(
            #dtick=1,
            rangemode="tozero",
            tickformat=tickform,
        ),
        margin=dict(l=0,r=0,b=30,t=30,pad=10),
        font=dict(
            family="NotoSans-Condensed",
            size=14,
            color="#38160f"
        ),
        height=360
    )
    return fig

def aco_oppo_bar(df,filter_oppo):

    if filter_oppo == 'referral_steerage':
        col = 'Cost Reduction if Perform as Best-in-Class(PMPM)'
    else:
        col = 'Cost Reduction if Perform as Benchmark(PMPM)'

    df_figure = df[df['oppo']==filter_oppo].sort_values(by = col, ascending = False)

    xname=[]
    for item in df_figure['alias'].tolist():
        if len(item)>25:
            pos=item[int(len(item)/7*3):].find(' ') + int(len(item)/7*3) #item.replace(' ', '-', 2).find(' ')
            temp=item[:pos] + '<br>' + item[pos + 1:]
        else:
            temp=item
        xname.append(temp)

    fig = go.Figure(data=[
        go.Bar(
            name='',
            x=xname, 
            y=df_figure[col],
            text="",
            textposition='inside', 
            texttemplate='%{y:$,.0f}',
            width=0.3,
            textangle=0,
            marker=dict(
                    color=colors['blue'],
                    opacity=np.linspace(1,(1.15-0.15*len(df_figure)),len(df_figure))
                    ),
            orientation='v',
            hoverinfo='skip',
            #hovertemplate='%{x:,.2f}',
        )
    ])
    # Change the bar mode
    fig.update_layout(
        
        yaxis=dict(
            #ticklen=2,
            #tickwidth=5,
            tickformat = '$',
            #position=0.1,
            #ticksuffix='Mn',
            ),
        #bargap=0,
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        showlegend=False,
        margin=dict(l=0,r=0,b=0,t=0,pad=10),
        font=dict(
            family="NotoSans-Condensed",
            size=14,
            color="#38160f"
        ),
        height=200
    )
    return fig

def aco_oppo_tbl(df,filter_oppo):

    df_table = df[df['oppo']==filter_oppo]

    format_money = FormatTemplate.money(0)
    format_pct = FormatTemplate.percentage(0)
    format_num = Format( precision=0,group=',', scheme=Scheme.fixed,)

    dim_name = {'pat_manage':'Patient Cohort', 'overuse_reduction':'Service', 'readmission_reduction':'Disease', 'service_optimize':'Service Rate', 'pac_optimize':'Disease', }

    if filter_oppo == 'referral_steerage':
        col = [['','Service'], ['Preferred Provider','% of Total Units'], ['Preferred Provider','Avg Cost/Unit'], 
        ['Non-Preferred Provider','% of Total Units'], ['Non-Preferred Provider','Avg Cost/Unit'],['','Cost Reduction if Steering All Visits to Preferred Provider(PMPM)']]
        table_col = [{'name':col[k], 'id':df_table.columns[k], 'type':'numeric', 'format':format_money} if k in[2,4,5] \
        else {'name':col[k], 'id':df_table.columns[k], 'type':'numeric', 'format':format_pct}for k in range(6)]
    elif filter_oppo in ['pat_manage']:
        table_col = [{'name':dim_name[filter_oppo], 'id':df_table.columns[k]} if k==0 \
        else {'name':df_table.columns[k], 'id':df_table.columns[k], 'type':'numeric', 'format':format_money} for k in range(6)]
    elif filter_oppo in ['overuse_reduction']:
        table_col = [{'name':dim_name[filter_oppo], 'id':df_table.columns[k]} if k==0 \
        else {'name':df_table.columns[k], 'id':df_table.columns[k], 'type':'numeric', 'format':format_num} if k in [1,2,4] \
        else {'name':df_table.columns[k], 'id':df_table.columns[k], 'type':'numeric', 'format':format_money} for k in range(6)]
    else:
        table_col = [{'name':dim_name[filter_oppo], 'id':df_table.columns[k]} if k==0 \
        else {'name':df_table.columns[k], 'id':df_table.columns[k], 'type':'numeric', 'format':format_pct} if k in [1,2,4] \
        else {'name':df_table.columns[k], 'id':df_table.columns[k], 'type':'numeric', 'format':format_money} for k in range(6)]
    
    table=dash_table.DataTable(
        data=df_table.to_dict('records'),
        columns=table_col,  
        merge_duplicate_headers=True,
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_data_conditional=[
            {'if': {'column_id':df_table.columns[0]},
             'textAlign':'start',
             'width':'15rem'
            },
        ],
        style_cell={
            'textAlign': 'center',
            'font-family':'NotoSans-Regular',
            'fontSize':12,
            'border':'1px solid grey',
            'height': '1.5rem',
        },
        style_table={
            'back':  colors['blue'],
        },
        style_header={
            'height': '2.5rem',
            'minWidth':'3rem',
            'maxWidth':'8rem',
            'whiteSpace': 'normal',
            'backgroundColor': '#f1f6ff',
            'fontWeight': 'bold',
            'font-family':'NotoSans-CondensedLight',
            'fontSize':12,
            'color': '#1357DD',
            'text-align':'center',
            'border':'1px solid grey',
            'text-decoration':'none'
        },
    )
    return table


def bundle_oppo_tbl(df):
    
    format_money = FormatTemplate.money(0)
    format_pct = FormatTemplate.percentage(1)
    format_num = Format( precision=0,group=',', scheme=Scheme.fixed,)

    df_table = df.sort_values(by = 'reduct_amount', ascending = False)

    col = ['Bundle','Bundle Volume','Average Cost/Bundle','Estimated Cost Reduction Opportunity(average bundle cost)',
    'Estimated Cost Reduction Opportunity(% of average bundle cost)','Total Cost Reduction Opportunity']

    table_col = [{'name':col[k], 'id':df_table.columns[k]} if k==0 \
    else {'name':col[k], 'id':df_table.columns[k], 'type':'numeric', 'format':format_num} if k==1 \
    else {'name':col[k], 'id':df_table.columns[k], 'type':'numeric', 'format':format_money} if k in [2,3,5] \
    else {'name':col[k], 'id':df_table.columns[k], 'type':'numeric', 'format':format_pct} for k in range(6)]

    table=dash_table.DataTable(
        data=df_table.to_dict('records'),
        columns=table_col,  
        merge_duplicate_headers=True,
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_data_conditional=[
            {'if': {'column_id':df_table.columns[0]},
             'textAlign':'start',
             'width':'24rem'
            },
        ],
        style_cell={
            'textAlign': 'center',
            'font-family':'NotoSans-Regular',
            'fontSize':12,
            'border':'1px solid grey',
            'height': '1.5rem',
        },
        style_table={
            'back':  colors['blue'],
        },
        style_header={
            'height': '2.5rem',
            'minWidth':'3rem',
            'maxWidth':'8rem',
            'whiteSpace': 'normal',
            'backgroundColor': '#f1f6ff',
            'fontWeight': 'bold',
            'font-family':'NotoSans-CondensedLight',
            'fontSize':12,
            'color': '#1357DD',
            'text-align':'center',
            'border':'1px solid grey',
            'text-decoration':'none'
        },
    )
    return table

def bundle_oppo_dtl_bydim(df, tableid):
    
    format_money = FormatTemplate.money(0)
    format_pct = FormatTemplate.percentage(1)
    format_num = Format( precision=0,group=',', scheme=Scheme.fixed,)

    col = [['',df.columns[k]] if k<=3 else ['Comparison with Benchmark',df.columns[k]] for k in range(1,10)]

    table_col = [{'name':col[k-1], 'id':df.columns[k]} if k==1 \
    else {'name':col[k-1], 'id':df.columns[k], 'type':'numeric', 'format':format_num} if k==2 \
    #else {'name':col[k-1], 'id':df.columns[k], 'type':'numeric', 'format':format_money} if k in [4,9] \
    else {'name':col[k-1], 'id':df.columns[k], 'type':'numeric', 'format':format_pct} for k in range(1,10)]

    table=dash_table.DataTable(
        data=df.to_dict('records'),
        id=tableid,
        columns=table_col,  
        merge_duplicate_headers=True,
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_data_conditional=(
        data_bars_diverging_bundle(df, df.columns[4],10) +
        data_bars_diverging_bundle(df, df.columns[5],10) +
        data_bars_diverging_bundle(df, df.columns[6],10) +
        data_bars_diverging_bundle(df, df.columns[7],10) +
        data_bars_diverging_bundle(df, df.columns[8],10) +
        data_bars_diverging_bundle(df, df.columns[9],10) +
        [{'if': {'column_id':df.columns[k]},
             
             'width': '10rem',
            } for k in range(4,10)]+[ 
        {'if': {'column_id':df.columns[1]},
             
             'width': '5rem',
            }, 
        ]
        ),
        style_cell={
            'textAlign': 'center',
            'font-family':'NotoSans-Regular',
            'fontSize':12,
            'border':'1px solid grey',
            'height': '1.5rem',
        },
        style_table={
            'back':  colors['blue'],
        },
        style_header={
            'height': '2.5rem',
            'minWidth':'3rem',
            'maxWidth':'8rem',
            'whiteSpace': 'normal',
            'backgroundColor': '#f1f6ff',
            'fontWeight': 'bold',
            'font-family':'NotoSans-CondensedLight',
            'fontSize':12,
            'color': '#1357DD',
            'text-align':'center',
            'border':'1px solid grey',
            'text-decoration':'none'
        },
    )
    return table

def bundle_oppo_dtl_bench(df, tableid, title):
    
    format_money = FormatTemplate.money(0)
    format_pct = FormatTemplate.percentage(1)
    format_num = Format( precision=0,group=',', scheme=Scheme.fixed,)

    col = [['',df.columns[k]] if k<=1 else [title,df.columns[k]] for k in range(1,7)]

    if 'Rate' in title:
        format_others = format_pct
    elif 'Cost' in title:
        format_others = format_money
    else:
        format_others = format_num

    table_col = [{'name':col[k-1], 'id':df.columns[k]} if k==1 \
    else {'name':col[k-1], 'id':df.columns[k], 'type':'numeric', 'format':format_pct} if k in [4,6] \
    else {'name':col[k-1], 'id':df.columns[k], 'type':'numeric', 'format':format_others} for k in range(1,7)]

    table=dash_table.DataTable(
        data=df.to_dict('records'),
        id=tableid,
        columns=table_col,  
        merge_duplicate_headers=True,
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_data_conditional=(
        data_bars_diverging(df, 'Diff from Benchmark',df['Diff from Benchmark'].max()/0.9) +
        data_bars_diverging(df, 'Diff from BIC',df['Diff from BIC'].max()/0.9) +
        [{'if': {'column_id':'Diff from Benchmark'},
             
             'width': '20rem',
            }, 
        {'if': {'column_id':'Diff from BIC'},
             
             'width': '20rem',
            }, 
        {'if': {'column_id':df.columns[1]},
             
             'width': '10rem',
            }, 
        ]
        ),
        style_cell={
            'textAlign': 'center',
            'font-family':'NotoSans-Regular',
            'fontSize':12,
            'border':'1px solid grey',
            'height': '1.5rem',
        },
        style_table={
            'back':  colors['blue'],
        },
        style_header={
            'height': '2.5rem',
            'minWidth':'3rem',
            'maxWidth':'8rem',
            'whiteSpace': 'normal',
            'backgroundColor': '#f1f6ff',
            'fontWeight': 'bold',
            'font-family':'NotoSans-CondensedLight',
            'fontSize':12,
            'color': '#1357DD',
            'text-align':'center',
            'border':'1px solid grey',
            'text-decoration':'none'
        },
    )
    return table

def aco_oppo_drill_tbl(df):
    
    df_table = df[(df['oppo']=='pat_manage') & (df['category']=='High Risk Chronic Patient')]

    fstcol_name = aco_oppo_drill_mapping[(aco_oppo_drill_mapping['oppo']=='pat_manage') & (aco_oppo_drill_mapping['category']=='High Risk Chronic Patient')].values[0]

    format_money = FormatTemplate.money(0)
    format_pct = FormatTemplate.percentage(0)
    format_num = Format( precision=0,group=',', scheme=Scheme.fixed,)

    table_col = [{'name':'Disease', 'id':df_table.columns[k]} if k==0 else {'name':df_table.columns[k], 'id':df_table.columns[k], 'type':'numeric', 'format':format_money} for k in range(6)]
   
    table=dash_table.DataTable(
        data=df_table.to_dict('records'),
        columns=table_col, 
        id = 'oppo-table-acodrill',
        merge_duplicate_headers=True,
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_data_conditional=[
            {'if': {'column_id':'Subcategory'},
             'textAlign':'start',
             'width':'15rem'
            },
        ],
        style_cell={
            'textAlign': 'center',
            'font-family':'NotoSans-Regular',
            'fontSize':12,
            'border':'1px solid grey',
            'height': '1.5rem',
        },
        style_table={
            'back':  colors['blue'],
        },
        style_header={
            'height': '2.5rem',
            'minWidth':'3rem',
            'maxWidth':'8rem',
            'whiteSpace': 'normal',
            'backgroundColor': '#f1f6ff',
            'fontWeight': 'bold',
            'font-family':'NotoSans-CondensedLight',
            'fontSize':12,
            'color': '#1357DD',
            'text-align':'center',
            'border':'1px solid grey',
            'text-decoration':'none'
        },
    )
    return table
