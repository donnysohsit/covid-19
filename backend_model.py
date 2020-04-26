import dash_core_components as dcc
import backend_controller as bc
import backend_library as bl
import plotly_express as px

def create_basic_statistics(region_confirmed_data, region_death_data, start_of_dates_agg):
    # Metric 1, 2 and 3
    number_confirmed, prev_number_confirmed, daily_growth_confirm = bl.top_metric1(region_confirmed_data)
    number_deaths, prev_number_deaths, daily_growth_deaths = bl.top_metric1(region_death_data)
    mortality_rate = bl.top_metric3(number_confirmed, number_deaths)

    agg_confirmed_data = bl.create_aggregated(region_confirmed_data, start_of_dates_agg)
    agg_death_data = bl.create_aggregated(region_death_data, start_of_dates_agg)

    percent_confirmed_data = bl.create_percent_growth(agg_confirmed_data)
    percent_death_data = bl.create_percent_growth(agg_death_data)

    # Metric 4 and 5
    daily_growth_percent_confirm = bl.top_metric4(percent_confirmed_data)
    daily_growth_percent_death = bl.top_metric4(percent_death_data)

    basic_statistics = bc.basic_statistics_controller(number_confirmed, prev_number_confirmed, number_deaths, prev_number_deaths, 
                            mortality_rate, daily_growth_confirm, daily_growth_deaths, daily_growth_percent_confirm, daily_growth_percent_death)

    return basic_statistics

def create_graph_statistics(region_confirmed_data, region_death_data, start_of_dates_agg):
    # Data for Graph 1: Daily
    agg_confirmed_data = bl.create_aggregated(region_confirmed_data, start_of_dates_agg)
    agg_death_data = bl.create_aggregated(region_death_data, start_of_dates_agg)

    agg_confirmed_data3 = bl.rolling_average(agg_confirmed_data, 3)
    agg_death_data3 = bl.rolling_average(agg_death_data, 3)

    agg_confirmed_data7 = bl.rolling_average(agg_confirmed_data, 7)
    agg_death_data7 = bl.rolling_average(agg_death_data, 7)

    # Data for Graph 2: Daily
    growth_confirmed_data = bl.create_growth(agg_confirmed_data)
    growth_death_data = bl.create_growth(agg_death_data)

    growth_confirmed_data3 = bl.create_growth(agg_confirmed_data3)
    growth_death_data3 = bl.create_growth(agg_death_data3)

    growth_confirmed_data7 = bl.create_growth(agg_confirmed_data7)
    growth_death_data7 = bl.create_growth(agg_death_data7)

    # Data for Graph 3: Daily
    percent_confirmed_data = bl.create_percent_growth(agg_confirmed_data)
    percent_death_data = bl.create_percent_growth(agg_death_data)

    percent_confirmed_data3 = bl.create_percent_growth(agg_confirmed_data3)
    percent_death_data3 = bl.create_percent_growth(agg_death_data3)

    percent_confirmed_data7 = bl.create_percent_growth(agg_confirmed_data7)
    percent_death_data7 = bl.create_percent_growth(agg_death_data7)

    graph_statistics1 = []
    graph_statistics3 = []
    graph_statistics7 = []

    graph_statistics1.append(agg_confirmed_data[0])
    graph_statistics1.append(agg_death_data[0])
    graph_statistics1.append(growth_confirmed_data)
    graph_statistics1.append(growth_death_data)
    graph_statistics1.append(percent_confirmed_data)
    graph_statistics1.append(percent_death_data)

    graph_statistics3.append(agg_confirmed_data3)
    graph_statistics3.append(agg_death_data3)
    graph_statistics3.append(growth_confirmed_data3)
    graph_statistics3.append(growth_death_data3)
    graph_statistics3.append(percent_confirmed_data3)
    graph_statistics3.append(percent_death_data3)

    graph_statistics7.append(agg_confirmed_data7)
    graph_statistics7.append(agg_death_data7)
    graph_statistics7.append(growth_confirmed_data7)
    graph_statistics7.append(growth_death_data7)
    graph_statistics7.append(percent_confirmed_data7)
    graph_statistics7.append(percent_death_data7)

    return graph_statistics1, graph_statistics3, graph_statistics7

def create_region_map2(express_bubble_data):
    map_graph1 = px.choropleth(express_bubble_data, scope="world", locations="region", color="confirmed", locationmode="country names", hover_name="region", animation_frame="date",
        color_continuous_scale=px.colors.sequential.Plasma, projection ='robinson')
    map_graph1 = dcc.Graph(figure=map_graph1)

    map_graph2 = px.choropleth(express_bubble_data, scope="world", locations="region", color="growth", locationmode="country names", hover_name="region", animation_frame="date",
        color_continuous_scale=px.colors.sequential.Plasma, projection ='robinson')
    map_graph2 = dcc.Graph(figure=map_graph2)

    map_graph3 = px.choropleth(express_bubble_data, scope="world", locations="region", color="deaths", locationmode="country names", hover_name="region", animation_frame="date",
        color_continuous_scale=px.colors.sequential.Plasma, projection ='robinson')
    map_graph3 = dcc.Graph(figure=map_graph3)
    return map_graph1, map_graph2, map_graph3


def create_region_map1(region_confirmed_data, region_death_data, start_of_dates_agg, top_region_list):

    agg_region_confirmed_data = region_confirmed_data.groupby(['region']).agg({f : "sum"  for f in region_confirmed_data.columns[start_of_dates_agg:] }).reset_index()

    temp_df1 = agg_region_confirmed_data.iloc[:,2:-1]
    temp_df2 = agg_region_confirmed_data.iloc[:,1:-2]

    temp_df2.reset_index(drop=True, inplace=True)
    temp_df3 = 100.0 * (temp_df1 - temp_df2.values) / temp_df2.values

    temp_df3 = temp_df3.fillna(0)    
    temp_df3.head()

    temp_df3.insert(0, 'region', agg_region_confirmed_data['region'], allow_duplicates=False) 
    agg_region_confirmed_growth_data = temp_df3

    agg_region_death_data = region_death_data.groupby(['region']).agg({f : "sum"  for f in region_death_data.columns[start_of_dates_agg:] }).reset_index()

    num_of_days = len(agg_region_confirmed_data.columns[1:])

    map_graph1 = bc.create_region_map(top_region_list, num_of_days, agg_region_confirmed_data)
    map_graph1 = dcc.Graph(figure=map_graph1)

    map_graph2 = bc.create_region_map(top_region_list, num_of_days-2, agg_region_confirmed_growth_data)
    map_graph2 = dcc.Graph(figure=map_graph2)

    map_graph3 = bc.create_region_map(top_region_list, num_of_days, agg_region_death_data)
    map_graph3 = dcc.Graph(figure=map_graph3)

    return map_graph1, map_graph2, map_graph3

def create_us_map2(express_bubble_data):
    map_graph1 = px.choropleth(express_bubble_data, scope="usa", locations="region", color="confirmed", locationmode="USA-states", hover_name="region", animation_frame="date",
        color_continuous_scale=px.colors.sequential.Plasma, projection ='albers usa')
    map_graph1 = dcc.Graph(figure=map_graph1)

    map_graph2 = px.choropleth(express_bubble_data, scope="usa", locations="region", color="growth", locationmode="USA-states", hover_name="region", animation_frame="date",
        color_continuous_scale=px.colors.sequential.Plasma, projection ='albers usa')
    map_graph2 = dcc.Graph(figure=map_graph2)

    map_graph3 = px.choropleth(express_bubble_data, scope="usa", locations="region", color="deaths", locationmode="USA-states", hover_name="region", animation_frame="date",
        color_continuous_scale=px.colors.sequential.Plasma, projection ='albers usa')
    map_graph3 = dcc.Graph(figure=map_graph3)
    return map_graph1, map_graph2, map_graph3

def create_us_map1(region_confirmed_data, region_death_data, start_of_dates_agg, top_region_list):

    agg_region_confirmed_data = region_confirmed_data.groupby(['region']).agg({f : "sum"  for f in region_confirmed_data.columns[start_of_dates_agg:] }).reset_index()

    temp_df1 = agg_region_confirmed_data.iloc[:,2:-1]
    temp_df2 = agg_region_confirmed_data.iloc[:,1:-2]

    temp_df2.reset_index(drop=True, inplace=True)
    temp_df3 = 100.0 * (temp_df1 - temp_df2.values) / temp_df2.values

    temp_df3 = temp_df3.fillna(0)    
    temp_df3.head()

    temp_df3.insert(0, 'region', agg_region_confirmed_data['region'], allow_duplicates=False) 
    agg_region_confirmed_growth_data = temp_df3

    agg_region_death_data = region_death_data.groupby(['region']).agg({f : "sum"  for f in region_death_data.columns[start_of_dates_agg:] }).reset_index()

    num_of_days = len(agg_region_confirmed_data.columns[1:])

    map_graph1 = bc.create_us_map(top_region_list, num_of_days, agg_region_confirmed_data)
    map_graph1 = dcc.Graph(figure=map_graph1)

    map_graph2 = bc.create_us_map(top_region_list, num_of_days-2, agg_region_confirmed_growth_data)
    map_graph2 = dcc.Graph(figure=map_graph2)

    map_graph3 = bc.create_us_map(top_region_list, num_of_days, agg_region_death_data)
    map_graph3 = dcc.Graph(figure=map_graph3)

    return map_graph1, map_graph2, map_graph3

# def create_bubble(region_confirmed_data, region_death_data, start_of_dates_agg, top_region_list):
def create_bubble(express_bubble_data, top_region_list):
    # agg_region_confirmed_data = region_confirmed_data.groupby(['region']).agg({f : "sum"  for f in region_confirmed_data.columns[start_of_dates_agg:] }).reset_index()
    # agg_region_death_data = region_death_data.groupby(['region']).agg({f : "sum"  for f in region_death_data.columns[start_of_dates_agg:] }).reset_index()

    # num_of_days = len(agg_region_confirmed_data.columns[1:])

    # bubble_graph = bc.create_bubble(top_region_list, num_of_days, agg_region_confirmed_data, agg_region_death_data)

    print(express_bubble_data.head())
    df1 = express_bubble_data[express_bubble_data['region'].isin(top_region_list.head(2))]
    print(df1.head())
    print(top_region_list.head(2))

    bubble_graph = bc.create_bubble(df1)
    bubble_curves = dcc.Graph(figure=bubble_graph)
    bubble_curves = [bubble_curves]

    return bubble_curves


def create_graphs(graph_statistics):
    fig_main = bc.create_figure_controller(graph_statistics)
    timeline_curves = dcc.Graph(figure=fig_main)
    timeline_curves = [timeline_curves]

    return timeline_curves