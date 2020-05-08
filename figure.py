
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

colors={'blue':'rgba(18,85,222,100)','yellow':'rgba(246,177,17,100)','transparent':'rgba(255,255,255,0)','grey':'rgba(191,191,191,100)',
       'lightblue':'rgba(143,170,220,100)'}

def qualitytable(df):

	table=dash_table.DataTable(
		data=df.to_dict('records'),
		id='table-measure-setup',
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


def sim_result_box(df_sim_result):
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
                        text='Best: '+str(round(df['Best'].to_list()[1:n][i],1))+'Mn',
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
                        text='Worst: '+str(round(df['Worst'].to_list()[1:n][i],1))+'Mn',
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
                            text=bartext+str(round(base,1))+'Mn',
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
                ticksuffix='Mn',
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
    return fig_sim

def table_sim_result(df):
    column1=[]
    n=len(df)
    style1=[0,3,6]
    style2=[1,4,7]
    style3=[2,5,8]
    
    if len(df)==10:
        column1.append('Baseline')
        style1=[0,1,4,7]
        style2=[2,5,8]
        style3=[3,6,9]
    column1=column1+['Contract','w/o','VBC Payout','Contract with','VBC Payout','(Recommended)','Contract with','VBC Payout','(User Defined)']
 
    df['scenario']=column1
    
   
    table=dash_table.DataTable(
        data=df.to_dict('records'),
        #id=tableid,
        columns=[
        {"name": ["Contract Type","Contract Type"], "id": "scenario"},
        {"name": ["Item","Item"], "id": "Item"},
        {"name": ["","Best Estimate(Mn)"], "id": "Best Estimate",'type': 'numeric',"format":Format( precision=1, scheme=Scheme.fixed,),},
        {"name": [ "Full Range","Low(Mn)"], "id": "Worst",'type': 'numeric',"format":Format( precision=1, scheme=Scheme.fixed,),},
        {"name": [ "Full Range","High(Mn)"], "id": "Best",'type': 'numeric',"format":Format( precision=1, scheme=Scheme.fixed,),},
        {"name": [ "Most Likely Range","Low(Mn)"], "id": "Lower End",'type': 'numeric',"format":Format( precision=1, scheme=Scheme.fixed,),},
        {"name": [ "Most Likely Range","High(Mn)"], "id": "Higher End",'type': 'numeric',"format":Format( precision=1, scheme=Scheme.fixed,),},
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