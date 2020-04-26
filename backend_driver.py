import pandas as pd
import numpy as np

import dash_core_components as dcc
import backend_library as bl
import backend_model as bm

#magic numbers
start_of_dates_agg = 1
num_top_regions = 15
top_region_list = []

# GLOBAL DATA
confirmed_data = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
death_data = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")

region_confirmed_data = bl.remove_columns(confirmed_data, ['Province/State', 'Lat','Long'])
region_death_data = bl.remove_columns(death_data, ['Province/State', 'Lat','Long'])

region_confirmed_data.rename(columns={region_confirmed_data.columns[0]:'region'}, inplace=True)
region_death_data.rename(columns={region_death_data.columns[0]:'region'}, inplace=True)

# top curves
basic_statistics_global = bm.create_basic_statistics(region_confirmed_data, region_death_data, start_of_dates_agg)

# middle graphs
graph_statistics1_global, graph_statistics3_global, graph_statistics7_global = bm.create_graph_statistics(region_confirmed_data, region_death_data, start_of_dates_agg)

# right table
region_table_global = bl.create_top_table(region_confirmed_data, region_death_data)
top_region_list = bl.create_top_regions(region_table_global, num_top_regions)

# map and bubble data
express_bubble_data_global = bl.create_express_data(region_confirmed_data, region_death_data, start_of_dates_agg, top_region_list)

# middle map
# map_graph1_global, map_graph2_global, map_graph3_global = bm.create_region_map1(region_confirmed_data, region_death_data, start_of_dates_agg, top_region_list)
map_graph1_global, map_graph2_global, map_graph3_global = bm.create_region_map2(express_bubble_data_global)

# bubble map
show_bubble = False
if show_bubble == True:
    bubble_curves_global = bm.create_bubble(express_bubble_data_global, top_region_list)

# USA DATA
confirmed_us_data = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")
death_us_data = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')

region_confirmed_data = bl.remove_columns(confirmed_us_data, ['Admin2', 'Country_Region', 'UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Combined_Key', 'Lat','Long_'])
region_death_data = bl.remove_columns(death_us_data, ['Admin2', 'Country_Region', 'UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Combined_Key', 'Lat','Long_', 'Population'])

region_confirmed_data.rename(columns={region_confirmed_data.columns[0]:'region'}, inplace=True)
region_death_data.rename(columns={region_death_data.columns[0]:'region'}, inplace=True)

region_confirmed_data['region'] = region_confirmed_data['region'].replace(bl.us_state_abbrev)
region_death_data['region'] = region_death_data['region'].replace(bl.us_state_abbrev)

# top curves
basic_statistics_us = bm.create_basic_statistics(region_confirmed_data, region_death_data, start_of_dates_agg)

# middle graphs
graph_statistics1_us, graph_statistics3_us, graph_statistics7_us = bm.create_graph_statistics(region_confirmed_data, region_death_data, start_of_dates_agg)

# right table
region_table_us = bl.create_top_table(region_confirmed_data, region_death_data)
top_region_list_us = bl.create_top_regions(region_table_us, num_top_regions)

# map and bubble data
express_bubble_data_us = bl.create_express_data(region_confirmed_data, region_death_data, start_of_dates_agg, top_region_list_us)

# middle map
# map_graph1_us, map_graph2_us, map_graph3_us = bm.create_us_map1(region_confirmed_data, region_death_data, start_of_dates_agg, top_region_list_us)
map_graph1_us, map_graph2_us, map_graph3_us = bm.create_us_map2(express_bubble_data_us)

bubble_curves = []
graph_statistics = []

# bubble map
if show_bubble == True:
    bubble_curves_us = bm.create_bubble(express_bubble_data_us, top_region_list_us)

basic_statistics = basic_statistics_global
graph_statistics1 = graph_statistics1_global
graph_statistics3 = graph_statistics3_global
graph_statistics7 = graph_statistics7_global
region_table = region_table_global

map_graph1 = map_graph1_global
map_graph2 = map_graph2_global
map_graph3 = map_graph3_global

map_curves = [map_graph2]
graph_statistics = graph_statistics1

timeline_curves = bm.create_graphs(graph_statistics)

if show_bubble == True:
    bubble_curves = bubble_curves_global

def create_region_table(temp):
    df = region_table

    if temp == -1:
        df = df.sort_values([df.columns[1]], ascending=False)
        df = df.head(15)

        df.iloc[:,1] = df.iloc[:,1].astype(int)
        df.iloc[:,4] = df.iloc[:,4].astype(int)

        df.iloc[:,1] = df.iloc[:,1].apply(lambda x: "{:,}".format(x))
        df.iloc[:,4] = df.iloc[:,4].apply(lambda x: "{:,}".format(x))

    else:
        key_value = temp
        key_values = [1, 2, 4]
        if key_value == 0:
            df = df.sort_values([df.columns[key_values[key_value]]], ascending=False)
        else:
            key_value = key_values[key_value]
            df = df.sort_values([df.columns[key_values[0]]], ascending=False)
            df = df.head(15)
            df = df.sort_values([df.columns[key_value]], ascending=False)

        df.iloc[:,1] = df.iloc[:,1].astype(int)
        df.iloc[:,4] = df.iloc[:,4].astype(int)

        df.iloc[:,1] = df.iloc[:,1].apply(lambda x: "{:,}".format(x))
        df.iloc[:,4] = df.iloc[:,4].apply(lambda x: "{:,}".format(x))

    return df

def trigger_map(map_type):
    global map_curves
    
    map_curves = [map_graph1]
    if map_type == 0:
        map_curves = [map_graph1]
    elif map_type == 1:
        map_curves = [map_graph2]
    elif map_type == 2:
        map_curves = [map_graph3]
    return map_curves

def trigger_graph(graph_type):
    global graph_statistics, timeline_curves

    if graph_type == 1:
        graph_statistics = graph_statistics1
    elif graph_type == 3:
        graph_statistics = graph_statistics3
    elif graph_type == 7:
        graph_statistics = graph_statistics7

    timeline_curves = bm.create_graphs(graph_statistics)

def trigger_country(key_value):
    global basic_statistics, graph_statistics1, graph_statistics3, graph_statistics7, region_table, map_graph1, map_graph2, map_graph3, bubble_curves

    if key_value == 0:        
        basic_statistics = basic_statistics_global
        graph_statistics1 = graph_statistics1_global
        graph_statistics3 = graph_statistics3_global
        graph_statistics7 = graph_statistics7_global
        region_table = region_table_global

        map_graph1 = map_graph1_global
        map_graph2 = map_graph2_global
        map_graph3 = map_graph3_global

        if show_bubble == True:
            bubble_curves = bubble_curves_global
    else:
        basic_statistics = basic_statistics_us
        graph_statistics1 = graph_statistics1_us
        graph_statistics3 = graph_statistics3_us
        graph_statistics7 = graph_statistics7_us
        region_table = region_table_us

        map_graph1 = map_graph1_us
        map_graph2 = map_graph2_us
        map_graph3 = map_graph3_us

        if show_bubble == True:
            bubble_curves = bubble_curves_us
    return
