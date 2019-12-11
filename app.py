#!/usr/bin/env python
# coding: utf-8

# In[41]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

#---open file--- 
df = pd.read_csv("nama_10_gdp_1_Data.csv")
    
#---use dash---
app = dash.Dash(__name__)
server = app.server

#---define look by external css---
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

available_indicators = df['NA_ITEM'].unique()
available_countrys = df['GEO'].unique()
available_units = df['UNIT'].unique()

#---creating app---
app.layout = html.Div([
    
    #---first graph---
    html.H2('First Dashboard'),
    #Two dropdown of indicators
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-indicator',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '25%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Dropdown(
                id='yaxis-indicator',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Value added, gross'
            )
        ],
        style={'width': '25%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Dropdown(
                id='unit-1',
                options=[{'label': i, 'value': i} for i in available_units],
                value='Chain linked volumes, index 2010=100'
            )
        ],
        style={'width': '25%', 'display': 'inline-block'})
        
    ]), 
    
    #display first graph
    dcc.Graph(id='indicator-graphic'),
    
    #Slider of Year
    dcc.Slider(
        id='year-slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),
    
    #---spacing between graphs---
    html.Br(),
    html.Br(),
    
    #---second graph---
    html.H2('Second Dashboard'),
    #Dropdown of indicator and country
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='indicator',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '25%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in available_countrys],
                value='Belgium'
            )
        ],
        style={'width': '25%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Dropdown(
                id='unit-2',
                options=[{'label': i, 'value': i} for i in available_units],
                value='Chain linked volumes, index 2010=100'
            )
        ],
        style={'width': '25%', 'display': 'inline-block'})
    ]), 
    
    #display second graph
    dcc.Graph(id='lines-graphic'),
])

#---first graph callback---
@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-indicator', 'value'),
     dash.dependencies.Input('yaxis-indicator', 'value'),
     dash.dependencies.Input('unit-1', 'value'),
     dash.dependencies.Input('year-slider', 'value')])

def update_graph(xaxis_indicator_name, yaxis_indicator_name, unit1, year_value):
    dff = df[(df['TIME'] == year_value) & (df['UNIT'] == unit1)]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_indicator_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_indicator_name]['Value'],
            text=dff[dff['NA_ITEM'] == xaxis_indicator_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            title={'text': unit1, 'xanchor':'center', 'yanchor':'top'},
            xaxis={'title': xaxis_indicator_name},
            yaxis={'title': yaxis_indicator_name},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

#---second graph callback---
@app.callback(
    dash.dependencies.Output('lines-graphic', 'figure'),
    [dash.dependencies.Input('indicator', 'value'),
     dash.dependencies.Input('unit-2', 'value'),
     dash.dependencies.Input('country', 'value')])

def update_graph(indicator_name, unit2, country_value):    
    dff = df[(df['GEO'] == country_value) & (df['UNIT'] == unit2)]
    
    return {
        'data':[go.Scatter(
            x=list(dff['TIME'].unique()),
            y=dff[dff['NA_ITEM'] == indicator_name]['Value'],
            text=dff[dff['NA_ITEM'] == indicator_name]['GEO'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            title={'text': unit2, 'xanchor':'center', 'yanchor':'top',},     
            xaxis={'title': 'Year'},
            yaxis={'title': indicator_name},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

#---run app---
if __name__ == '__main__':
    app.run_server()   


# In[ ]:




