import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.dash import no_update

import dash_table
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

import top_metrics as tp
import backend_driver as bd

from flask import Flask, request
from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server # the Flask app
server.config.from_mapping(config)
cache = Cache(server)

# make a reuseable navitem for the different examples
nav_item = dbc.NavItem(dbc.NavLink("Contact", href="mailto:donnyandco@gmail.com"))

# make a reuseable dropdown for the different examples
dropdown = dbc.DropdownMenu(
    children=[
        # dbc.DropdownMenuItem("Singapore"),
        dbc.DropdownMenuItem("USA", id="input-1", n_clicks_timestamp=0),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Global", id="input-0", n_clicks_timestamp=0),
    ],
    nav=True,
    in_navbar=True,
    label="Region",
    id="situationmenu",    
)

default = dbc.NavbarSimple(
    children=[nav_item, dropdown],
    brand="Covid-19 Monitoring Dashboard",
    brand_href="#",
    sticky="top",
    className="mb-3",
    dark="true",
    color="dark"
)

dashboard = dcc.Graph(
    id='example-graph',
    figure={
        'data': [
            {'x':[1,2,3], 'y': [4,1,2], 'type': 'bar', 'name': 'Singapore'},
            {'x':[1,2,3], 'y': [2,4,5], 'type': 'bar', 'name': 'Montreal'}
        ],
        'layout': {
            'title': 'Dash Data Visualization'
        }
    }
)

table = html.Div(
    [
        dbc.Table.from_dataframe(bd.region_table.head(15), striped=True, bordered=True, hover=True, size = 'sm', className='table-sm')
    ], id='country-table', style={"maxHeight": "26rem", 'overflow-y': 'scroll'}, className= 'mr-0'
)

rightmiddlegraphs = dbc.Col(
    [dbc.Card(
        [dbc.CardBody(
            [
                html.H5("Daily Statistics", className="card-title"),
            ]
            ), table
        ])], className ='col-5'
)

middlegraphs = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button("filter by confirmed cases", outline=False, color="danger", id='sort_confirm', className='col-12', n_clicks_timestamp=0),
                                ),
                                dbc.Col(
                                    dbc.Button("filter by confirmed growth", outline=False, color="warning", id='sort_confirm_rate', className='col-12', n_clicks_timestamp=0),
                                ),
                                dbc.Col(
                                    dbc.Button("filter by death cases", outline=False, color="dark", id='sort_death', className='col-12', n_clicks_timestamp=0),                        
                                )
                            ], className =['mt-0' , 'mb-1']
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [dbc.Card(
                                        bd.map_curves)],
                                        id="map_charts"
                                )
                            ], className =['mt-0' , 'mb-0']
                        )
                    ], className =['col-7', 'ml-0' , 'mr-0', 'mt-0' , 'mb-0']
                ), rightmiddlegraphs
            ], className= ['justify-content-between', 'ml-2' , 'mr-2', 'mt-2' , 'mb-2']        
        )
    ]
)

middlegraphs2 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Daily", outline=False, color="danger", id='chart_daily', className='col-12', n_clicks_timestamp=0),
                ),
                dbc.Col(
                    dbc.Button("3 Day Moving Average", outline=False, color="warning", id='chart_three', className='col-12', n_clicks_timestamp=0),
                ),
                dbc.Col(
                    dbc.Button("7 day Moving Average", outline=False, color="dark", id='chart_week', className='col-12', n_clicks_timestamp=0),
                )
            ], className= ['justify-content-between', 'ml-2' , 'mr-2', 'mt-4' , 'mb-2']
        ),
        dbc.Row(
            [
                dbc.Col(
                    [dbc.Card(
                        bd.timeline_curves)], id="daily_charts", className=['col-12', 'mt-1', 'mb-1']
                ), 
            ], className= ['justify-content-between', 'ml-2' , 'mr-2', 'mt-2' , 'mb-2']        
        )
    ]
)

bubblegraph = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [dbc.Card(
                        bd.bubble_curves)], id="bubble_charts", className=['col-12', 'mt-1', 'mb-1']
                )
            ], className=['ml-2', 'mb-1', 'mr-2']
        )

    ]
)

data_credits = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    "Data source: John Hopkins University, https://github.com/CSSEGISandData/COVID-19"
                )
            ], className=['ml-2', 'mb-1']
        )
    ]
)

show_bubble_chart = False
if show_bubble_chart:
    app.layout = html.Div(children=[    
        html.Div([default, tp.topmetrics]),
        html.Div([middlegraphs]),
        html.Div([middlegraphs2]),
        html.Div([bubblegraph]),
        html.Div([data_credits])
    ])
else:
    app.layout = html.Div(children=[    
        html.Div([default, tp.topmetrics]),
        html.Div([middlegraphs]),
        html.Div([middlegraphs2]),
        html.Div([data_credits])
    ])

@app.callback(
    [Output('country-table', 'children'), Output('map_charts', 'children'), Output('daily_charts', 'children'),
    Output('confirm_cases_card', 'children'), Output('death_cases_card', 'children'),
    Output('mortality_card', 'children'), Output('growth_confirm_card', 'children'), Output('growth_death_card', 'children')],
    [Input("input-0", "n_clicks_timestamp"), Input("input-1", "n_clicks_timestamp"), Input('sort_confirm', 'n_clicks_timestamp'), Input('sort_confirm_rate', 'n_clicks_timestamp'), 
    Input('sort_death', 'n_clicks_timestamp'), Input('chart_daily', 'n_clicks_timestamp'), Input('chart_three', 'n_clicks_timestamp'), Input('chart_week', 'n_clicks_timestamp')])
@cache.memoize(timeout=300)    
def update_label(input0, input1, input2, input3, input4, input5, input6, input7):
    temp = [input0, input1, input2, input3, input4, input5, input6, input7] 
    key_value = temp.index(max(temp))
    if key_value < 2:
        bd.trigger_country(key_value)
        t_map = bd.trigger_map(0)
        df = bd.create_region_table(-1)

        bd.trigger_graph(1)
        return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size = 'sm', className='table-sm'), [dbc.Card(t_map)], dbc.Card(bd.timeline_curves), \
            bd.basic_statistics[0], bd.basic_statistics[1], bd.basic_statistics[2], bd.basic_statistics[3], bd.basic_statistics[4]
    elif key_value < 5:
        key_value = key_value - 2
        t_map = bd.trigger_map(key_value)
        df = bd.create_region_table(key_value)
        return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size = 'sm', className='table-sm'), [dbc.Card(t_map)], no_update, \
            no_update, no_update, no_update, no_update, no_update
    else:
        key_value = key_value - 5
        rolling_values = [1, 3, 7]
        bd.trigger_graph(rolling_values[key_value])
        return no_update, no_update, dbc.Card(bd.timeline_curves), no_update, no_update, no_update, no_update, no_update

@server.route('/keep_alive')
def query_example():
    return 'This is a keep alive'

if __name__ == '__main__':
    app.run_server(debug=False)