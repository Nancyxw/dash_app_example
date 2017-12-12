# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 14:42:32 2017

@author: maximjxw
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv('https://raw.githubusercontent.com/Nancyxw/cloudcomputingesade/master/nama_10_gdp_1_Data.csv')
df = df[df['UNIT'] == 'Current prices, million euro']

available_indicators = df['NA_ITEM'].unique()
available_indicators_geo = df['GEO'].unique()

### First Dashboard Design ###
app.layout = html.Div([
    html.H2(children = "Cloud Computing Final Project - Nancy Xiaowen Jiang"),
    
    html.Div([
        html.H3(children = "First Graph"),
        
        html.H5(children = "The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data."),
        
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Value added, gross'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),
    

### Second Dashboard Design###
    html.Div([
        html.H3(children='Second Graph'),
        
        html.H5(children = "The second graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators."),
        
        html.Div([
            dcc.Dropdown(
                id='country_selection',
                options=[{'label': i, 'value': i} for i in available_indicators_geo],
                value='Spain'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column-lc',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic-lc')

])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['TIME'] == year_value]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 30, 'r': 10},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('indicator-graphic-lc', 'figure'),
    [dash.dependencies.Input('country_selection', 'value'),
     dash.dependencies.Input('yaxis-column-lc', 'value')])

def update_graph_lc(country_selection, yaxis_column_name):
    dff = df[df['GEO'] == country_selection]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == yaxis_column_name]['TIME'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['TIME'],
            mode='lines+markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name = yaxis_column_name
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Time'
            },
            yaxis={
                'title': yaxis_column_name
            },
            margin={'l': 60, 'b': 40, 't': 30, 'r': 10},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()
