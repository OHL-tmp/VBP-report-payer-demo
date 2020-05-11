
import pandas as pd
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

colors={'blue':'rgba(18,85,222,100)','yellow':'rgba(246,177,17,100)','transparent':'rgba(255,255,255,0)','grey':'rgba(191,191,191,100)',
       'lightblue':'rgba(143,170,220,100)'}


####################################################################################################################################################################################
######################################################################       Drilldown         ##################################################################################### 
#################################################################################################################################################################################### 


def qualitytable(df):

	table=dash_table.DataTable(
		data=df.to_dict('records'),
		id='table-measure-setup',
		columns=[
		{"name": ["","Measure"], "id": "measure"},
		{"name": [ "ACO Baseline","Value"], "id": "value"},
		{"name": [ "ACO Baseline","Percentile"], "id": "percentile",'type': 'numeric',"format":Format(nully='N/A'),},
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
				'backgroundColor': 'rgba(0,0,0,0)',
				'font-family': 'NotoSans-CondensedLight',
				'width':'4rem',
				'minWidth': '4rem',
				'maxWidth':'14rem',
				#'border':'1px solid grey',
				#'border-bottom': '1px solid grey',
				#'border-top': '1px solid grey',

		},
		style_data_conditional=[
				{ 'if': {'column_id':'measure'}, 
				 'font-weight':'bold', 
				 'textAlign': 'start',
				 'width':'14rem',
				 #'minWidth': '25rem',
				 #'maxWidth':'25rem',
				  },
		]+
		[
			{ 'if': {'row_index':c}, 
					'border':'1px solid grey',
					'border-bottom':'0px',
			 
					  } if c in [0,10,14,20] else
			{'if': {'row_index':c},
					'border':'1px solid grey',
					'border-top':'0px',
			 
					  } if c in [9,13,19,22] else
			{'if': {'row_index':c},
					'border':'1px solid grey',
					'border-bottom':'0px',
					'border-top':'0px',   
					}  for c in range(0,23)


		]+[
			{ 
				'if': {'row_index':c,'column_editable':True}, 
				'backgroundColor': 'rgba(18,85,222,0.1)',
				'font-weight':'bold',
				'border':'1px solid blue',
				'border-bottom':'1px solid rgba(18,85,222,0.1)',
			 
			} if c in [0,10,14,20] else
			{
				'if': {'row_index':c,'column_editable':True}, 
				'backgroundColor': 'rgba(18,85,222,0.1)',
				'font-weight':'bold',
				'border':'1px solid blue',
				'border-top':'1px solid rgba(18,85,222,0.1)',
			 
			} if c in [9,13,19,22] else
			{
				'if': {'row_index':c,'column_editable':True},
				'backgroundColor': 'rgba(18,85,222,0.1)', 
				'font-weight':'bold',
				'border':'1px solid blue',
				'border-bottom':'1px solid rgba(18,85,222,0.1)',
				'border-top':'1px solid rgba(18,85,222,0.1)',
			}  for c in range(0,23)

		]+[
			{
				'if': { 'column_id': 'costimplication','filter_query': '{costimplication} eq "Low"'},
				#'backgroundColor': 'green',
				'color': 'green',
			},
			{
				'if': { 'column_id': 'costimplication','filter_query': '{costimplication} eq "Mid"' },
				#'backgroundColor': 'rgb(246,177,17)',
				'color': 'rgb(237,125,49)',
			},
			{
				'if': { 'column_id': 'costimplication', 'filter_query': '{costimplication} eq "High"'},
				#'backgroundColor': 'red',
				'color': "red",
			}
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
    x=['Contract w/o<br>VBC Payout','Contract with VBC Payout<br>(Recommended)','Contract with VBC Payout<br>(User Defined)']
    m=0.3
    n=len(df)
    
    median=df['Best Estimate'].to_list()
    
    #color for bar and box
    fillcolor=['rgba(226,225,253,0)','rgba(18,85,222,0)','rgba(246,177,17,0)']
    markercolor=['rgba(191,191,191,0.7)','rgba(18,85,222,0.7)','rgba(246,177,17,0.7)']
        
    annotations = []
    
    if df.values[1,3]<df.values[1,4]:
        lowerfence=df['Worst'].to_list()
        q1=df['Lower End'].to_list()
        q3=df['Higher End'].to_list()
        upperfence=df['Best'].to_list()
    else:
        lowerfence=df['Best'].to_list()
        q1=df['Higher End'].to_list()
        q3=df['Lower End'].to_list()
        upperfence=df['Worst'].to_list()
        
    if df.values[0,7] in ["ACO's PMPM"]:
        suf=''
    elif df.values[0,7] in ["ACO's Margin %"]:
        suf='%'
    else:
        suf='Mn'

    fig_sim =go.Figure()
    
    for i in range(n):
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
        annotations.append(dict(xref='x', yref='y',axref='x', ayref='y',
                        x=0+i, y=df['Best'].to_list()[i],ax=m+i, ay=df['Best'].to_list()[i],
                        startstandoff=10,
                        text='Best: '+str(round(df['Best'].to_list()[i],1))+suf,
                        font=dict(family='NotoSans-CondensedLight', size=12, color='green'),
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=2,
                        arrowside='start',
                        arrowcolor='green',
                       )
                  )
        annotations.append(dict(xref='x', yref='y',axref='x', ayref='y',
                        x=0+i, y=df['Worst'].to_list()[i],ax=m+i, ay=df['Worst'].to_list()[i],
                        startstandoff=10,
                        text='Worst: '+str(round(df['Worst'].to_list()[i],1))+suf,
                        font=dict(family='NotoSans-CondensedLight', size=12, color='red'),
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=2,
                        arrowside='start',
                        arrowcolor='red',
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
        )
    return fig_sim

def table_sim_result(df):
    column1=[]
    n=len(df)
    style1=[0,4,8]
    style2=[1,2,5,6,9,10]
    style3=[3,7,11]
    
    #column1=column1+['Contract','w/o','VBC Payout','Contract with','VBC Payout','(Recommended)','Contract with','VBC Payout','(User Defined)']
    column1=column1+['Contract','w/o','VBC', 'Payout','Contract', 'with','VBC Payout','(Recommended)','Contract','with','VBC Payout','(User Defined)']
    df['scenario']=column1

    if df.values[0,7] in ["ACO's PMPM"]:
    	header=['Best Estimate','Low','High','Low','High']
    elif df.values[0,7] in ["ACO's Margin %"]:
    	header=['Best Estimate(%)','Low(%)','High(%)','Low(%)','High(%)']
    else:
    	header=['Best Estimate(Mn)','Low(Mn)','High(Mn)','Low(Mn)','High(Mn)']

    if df.values[0,7] =="ACO's Margin %":
    	df.iloc[:,2:7]=df.iloc[:,2:7]/100
    	num_format=Format( precision=1, scheme=Scheme.percentage,nully='N/A')    
    else:
    	num_format=Format( precision=1, scheme=Scheme.fixed,nully='N/A')
    
   
    table=dash_table.DataTable(
        data=df.to_dict('records'),
        #id=tableid,
        columns=[
        {"name": ["Contract Type","Contract Type"], "id": "scenario"},
        {"name": ["Item","Item"], "id": "Item"},
        {"name": ["",header[0]], "id": "Best Estimate",'type': 'numeric',"format":num_format,},
        {"name": [ "Full Range",header[1]], "id": "Worst",'type': 'numeric',"format":num_format,},
        {"name": [ "Full Range",header[2]], "id": "Best",'type': 'numeric',"format":num_format,},
        {"name": [ "Most Likely Range",header[3]], "id": "Lower End",'type': 'numeric',"format":num_format,},
        {"name": [ "Most Likely Range",header[4]], "id": "Higher End",'type': 'numeric',"format":num_format,},
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

    fig_waterfall = go.Figure(data=[
        go.Bar(
            name='',
            x=df.columns[0:3].tolist()+[gain], 
            y=df.values[0,0:3].tolist()+[base],
            #text=y1_waterfall,
            textposition='auto',
            textfont=dict(color=['black','black','black',colors['transparent']]),
            texttemplate='%{y:s}',
            marker=dict(
                    color=[colors['blue'],colors['blue'],colors['grey'],colors['transparent']],
                    opacity=[1,0.7,0.7,0]
                    ),
            marker_line=dict( color = colors['transparent'] ),
            hovertemplate='%{y:,.0f}',
            hoverinfo='y',
            
        ),
        go.Bar(  
            name='',
            x=df.columns[0:3].tolist()+[gain], 
            y=[0,0,0,df.values[0,3]],
            #text=y2_waterfall,
            textposition='outside',
            textfont=dict(color=[colors['transparent'],colors['transparent'],colors['transparent'],'black']),
            texttemplate='%{y:s}',
            marker=dict(
                    color=gaincolor,
                    opacity=0.7
                    ),
            hovertemplate='%{y:,.0f}',
            hoverinfo='y',
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
            texttemplate='%{y:s}',
            marker=dict(
                    color=gaincolor,
                    opacity=0.5
                    ),
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
            texttemplate='%{y:s}',
            marker=dict(
                    color=gaincolor,
                    opacity=0.3
                    ),
            hovertemplate='%{y:,.0f}',
            hoverinfo='y',
        )
    ])

    annotations=[]

    annotations.append(dict(xref='paper', yref='y',
                            x=1.12, y=df.values[0,4]/2,
                            text="Plan's Share ("+str(plan_share)+' %)',
                            font=dict(family='NotoSans-SemiBold', size=14, color='#38160f'),
                            showarrow=False,
                           )
                      )

    annotations.append(dict(xref='paper', yref='y',
                            x=1.12, y=df.values[0,4]+df.values[0,5]/2,
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
        title=dict(
            text='YTD Attributed Members VS. Target',
            font=dict(
            family="NotoSans-Condensed",
            size=16,
            color="#38160f",
            ),
            xref='container',
            yref='container',
            x=0.5,
            y=0.94,
            xanchor='center',
            yanchor='middle',
            ),
        xaxis=dict(
            ticklen=2,
            tickwidth=5,
            position=0.1,
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
                        opacity=[0.7,1]
                        ),
                hoverinfo='skip',
                #hovertemplate='%{x:,.2f}',
                )

            )

    fig.update_layout(
        barmode='stack',
        title=dict(
            text='Member Distribution by Risk Level',
            font=dict(
            family="NotoSans-Condensed",
            size=16,
            color="#38160f",
            ),
            xref='paper',
            yref='paper',
            x=0.5,
            y=0.98,
            xanchor='center',
            yanchor='middle',
            #pad=dict(b=5)
            ),
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
        showlegend=True,
        legend=dict(
            orientation='h',
            x=0.3,y=-0.05
        ),
        modebar=dict(
            bgcolor=colors['transparent']
        ),
        margin=dict(l=0,r=0,b=0,t=0,pad=4),
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
            textposition='inside',
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
        title=dict(
            text='Risk Score Improvement Opportunity',
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
        margin=dict(l=10,r=10,b=10,t=10,pad=0),
        font=dict(
            family="NotoSans-Condensed",
            size=12,
            color="#38160f"
        ),
    )
    return fig_waterfall
