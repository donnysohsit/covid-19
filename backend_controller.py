import pandas as pd
import numpy as np

import plotly.graph_objects as go
from bubbly.bubbly import bubbleplot
from plotly.subplots import make_subplots

def basic_statistics_controller(number_confirmed, prev_number_confirmed, number_deaths, prev_number_deaths, mortality, real_growth_1, real_growth_2, growth_1, growth_2):
    basic_statistics = []
    basic_statistics.append('{:,}'.format(number_confirmed) + " (" + '{:,}'.format(prev_number_confirmed) + ")")
    basic_statistics.append('{:,}'.format(number_deaths) + " (" + '{:,}'.format(prev_number_deaths) + ")")
    basic_statistics.append(str('{0:.2f}'.format(mortality)) + "%")
    basic_statistics.append('{:,}'.format(real_growth_1) + " (" + str('{0:.2f}'.format(growth_1)) + "%)")
    basic_statistics.append('{:,}'.format(real_growth_2) + " (" + str('{0:.2f}'.format(growth_2)) + "%)")

    return basic_statistics

def create_us_map(top_region_list, num_of_days, df1):

    df1 = df1[df1['region'].isin(top_region_list)]

    data = [dict(type='choropleth',
                locations = df1['region'],
                z=df1[df1.columns[1]],
                locationmode='USA-states')]
    
    for i in range(num_of_days):
        data.append(data[0].copy())
        data[-1]['z'] = df1[df1.columns[1 + i]]

    # let's create the steps for the slider
    steps = []
    for i in range(len(data)):
        step = dict(method='restyle',
                    args=['visible', [False] * len(data)],
                    label='Day {}'.format(i))
        step['args'][1][i] = True
        steps.append(step)

    sliders = [dict(active=0,
                    pad={"t": 1},
                    steps=steps)]    
    layout = dict(geo=dict(scope='usa',
                        projection={'type': 'albers usa'}),
                sliders=sliders)

    fig = dict(data=data, 
            layout=layout)

    return go.Figure(fig)

def create_region_map(top_region_list, num_of_days, df1):

    df1 = df1[df1['region'].isin(top_region_list)]

    data = [dict(type='choropleth',
                locations = df1['region'],
                z=df1[df1.columns[1]],
                locationmode='country names')]
    
    for i in range(num_of_days):
        data.append(data[0].copy())
        data[-1]['z'] = df1[df1.columns[1 + i]]

    # let's create the steps for the slider
    steps = []
    for i in range(len(data)):
        step = dict(method='restyle',
                    args=['visible', [False] * len(data)],
                    label='Day {}'.format(i))
        step['args'][1][i] = True
        steps.append(step)

    sliders = [dict(active=0,
                    pad={"t": 1},
                    steps=steps)]    
    layout = dict(geo=dict(scope='world',
                        projection={'type': 'robinson'}),
                sliders=sliders)

    fig = dict(data=data, 
            layout=layout)

    return go.Figure(fig)

def create_bubble(temp_construct):
    figure = bubbleplot(dataset=temp_construct, x_column='deaths', y_column='confirmed', 
        bubble_column='region', time_column='date', size_column='confirmed', color_column='region', 
        x_title="deaths", y_title="Confirmed", title='Covid-19 Spread by top regions.',
        x_logscale=False, y_logscale=False, scale_bubble=1, height=650)

    figure.update
    return figure

def create_figure_controller(graph_statistics):
    fig_main = make_subplots(
        rows=2, cols=3,
        shared_xaxes=True,
        subplot_titles=("Confirmed cases", 
            "Growth of confirmed cases", "Growth rate of confirmed cases", 
            "Deaths", "Growth of deaths", "Growth rate of deaths"
            ))

    fig_main.add_trace(
        go.Bar(
            x=list(range(0,graph_statistics[0].shape[0])),
            y=graph_statistics[0],
            name="Confirm Count"
        ), row=1, col=1)

    fig_main.add_trace(
        go.Bar(
            x=list(range(0,graph_statistics[1].shape[0])),
            y=graph_statistics[1],
            name="Death Count"
        ), row=2, col=1)

    fig_main.add_trace(
        go.Bar(
            x=list(range(0,graph_statistics[2].shape[0])),
            y=graph_statistics[2],
            name="Confirm Growth"
        ), row=1, col=2)

    fig_main.add_trace(
        go.Bar(
            x=list(range(0,graph_statistics[3].shape[0])),
            y=graph_statistics[3],
            name="Death Growth"
        ), row=2, col=2)

    fig_main.add_trace(
        go.Bar(
            x=list(range(0,graph_statistics[4].shape[0])),
            y=graph_statistics[4],
            name="Confirm % Growth"
        ), row=1, col=3)

    fig_main.add_trace(
        go.Bar(
            x=list(range(0,graph_statistics[5].shape[0])),
            y=graph_statistics[5],
            name="Death % Growth"
        ), row=2, col=3)

    fig_main.update_layout(
        margin=dict(l=5, r=5, t=30, b=10),     
        legend_orientation='h',
        paper_bgcolor= 'rgb(255,255,255)',
        plot_bgcolor="rgb(255,255,255)",
    )

    fig_main.update_xaxes(showline=True, linewidth=2, linecolor='LightGrey', gridcolor='LightGrey')
    fig_main.update_yaxes(showline=False, linewidth=2, linecolor='LightGrey', gridcolor='LightGrey')

    return fig_main
