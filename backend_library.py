import pandas as pd
import numpy as np

import dash_core_components as dcc

def remove_columns(df1, extra_columns):
    df1.drop([] + extra_columns, axis=1, inplace=True)
    return df1

def top_metric1(df1):
    return df1[df1.columns[-1]].sum(), df1[df1.columns[-2]].sum(), df1[df1.columns[-1]].sum() - df1[df1.columns[-2]].sum()

def top_metric3(m1, m2):
    return m2 / m1 * 100

def create_aggregated(df1, date1):
    return df1.agg({f : "sum"  for f in df1.columns[date1:] }).reset_index()

def create_growth(df1):
    #sloppy
    if len(df1.shape) == 2:
        return np.asarray(df1[0][1:]) - np.asarray(df1[0][:-1])
    else:
        return np.asarray(df1[1:]) - np.asarray(df1[:-1])

def create_percent_growth(df1):
    if len(df1.shape) == 2:
        return (np.asarray(df1[0][1:]) - np.asarray(df1[0][:-1])) / np.asarray(df1[0][:-1]) * 100
        # return (np.asarray(df1[0][1:]) - np.asarray(df1[0][:-1])) / 1 * 100
    else:
        return (np.asarray(df1[1:]) - np.asarray(df1[:-1])) / np.asarray(df1[:-1]) * 100
        # return (np.asarray(df1[1:]) - np.asarray(df1[:-1])) / 1 * 100

def top_metric4(df1):
    return df1[-1]

def rolling_average(df1, days):
    return df1[0].rolling(window=days).mean()

def create_top_regions(region_table, num_top_regions):
    region_table = region_table.sort_values(['confirmed'], ascending=[False])
    return region_table['region'].head(num_top_regions).replace(us_state_abbrev)

def create_top_table(df1, df2):
    start_of_dates_agg = 2
    agg_df1 = df1.groupby(['region']).agg({f : "sum"  for f in df1.columns[start_of_dates_agg:] }).reset_index()
    agg_df2 = df2.groupby(['region']).agg({f : "sum"  for f in df2.columns[start_of_dates_agg:] }).reset_index()

    derivative1_agg_df1 = (100 * (agg_df1[agg_df1.columns[-1]] - agg_df1[agg_df1.columns[-2]]) / agg_df1[agg_df1.columns[-2]])
    prev_derivative1_agg_df1 = (100 * (agg_df1[agg_df1.columns[-2]] - agg_df1[agg_df1.columns[-3]]) / agg_df1[agg_df1.columns[-3]])
    derivative2_agg_df1 = 100 * ((derivative1_agg_df1 - prev_derivative1_agg_df1) / prev_derivative1_agg_df1)

    derivative1_agg_df1 = derivative1_agg_df1.round(1)
    derivative2_agg_df1 = derivative2_agg_df1.round(1)

    derivative1_agg_df2 = (100 * (agg_df2[agg_df2.columns[-1]] - agg_df2[agg_df2.columns[-2]]) /
                 agg_df2[agg_df2.columns[-2]])
    derivative1_agg_df2 = derivative1_agg_df2.round(1)

    df3 = pd.DataFrame()

    agg_df1['region'] = agg_df1['region'].replace(us_state_abbrev)
    df3['region'] = agg_df1['region'].str.slice(0,14)
    df3['confirmed'] = agg_df1[agg_df1.columns[-1]].astype(int)
    df3['c-growth'] = derivative1_agg_df1.astype(float)
    df3['c-growth rate'] = derivative2_agg_df1.astype(float)

    df3['death'] = agg_df2[agg_df2.columns[-1]].astype(int)
    df3['d-growth'] = derivative1_agg_df2.astype(float)

    df3 = df3.fillna(0)
    df3 = df3.sort_values(['confirmed'], ascending=[False])
    return df3

def create_express_data(region_confirmed_data, region_death_data, start_of_dates_agg, top_region_list):

    num_days_include = 30
    num_days = len(region_confirmed_data.columns[1:])

    region_confirmed_data = region_confirmed_data.groupby(['region']).agg({f : "sum"  for f in region_confirmed_data.columns[start_of_dates_agg:] }).reset_index()
    region_death_data = region_death_data.groupby(['region']).agg({f : "sum"  for f in region_death_data.columns[start_of_dates_agg:] }).reset_index()

    temp_df2 = 100 * (np.asarray((region_confirmed_data[region_confirmed_data.columns[2:]])) - \
        np.asarray(region_confirmed_data[region_confirmed_data.columns[1:-1]])) / np.asarray(region_confirmed_data[region_confirmed_data.columns[1:-1]]) 
    temp_df2 = pd.DataFrame(temp_df2)
    region_confirmed_growth_data = temp_df2.fillna(0)    
    region_confirmed_growth_data.insert(0, "region", region_confirmed_data['region'], allow_duplicates=False) 

    region_confirmed_data.drop(region_confirmed_data.iloc[:, 1:(num_days-num_days_include)], inplace = True, axis = 1) 
    region_confirmed_growth_data.drop(region_confirmed_growth_data.iloc[:, 1:(num_days-num_days_include-1)], inplace = True, axis = 1) 
    region_death_data.drop(region_death_data.iloc[:, 1:(num_days-num_days_include)], inplace = True, axis = 1) 

    num_of_days = len(region_confirmed_data.columns[1:])

    t_region_confirmed_data = region_confirmed_data
    # t_region_confirmed_data = region_confirmed_data[region_confirmed_data['region'].isin(top_region_list)]

    t_region_death_data = region_death_data
    # t_region_death_data = region_death_data[region_death_data['region'].isin(top_region_list)]

    t_region_confirmed_growth_data = region_confirmed_growth_data

    df_region = t_region_confirmed_data['region']
    df_region = pd.DataFrame(df_region)

    t_region_confirmed_data = t_region_confirmed_data.drop('region', axis=1)
    t_region_confirmed_growth_data = t_region_confirmed_growth_data.drop('region', axis=1)
    t_region_death_data = t_region_death_data.drop('region', axis=1)

    ttt = t_region_confirmed_data.transpose()

    ttt = ttt.reset_index()
    ttt = ttt.rename(columns={'index': 'date'})

    temp_construct = pd.DataFrame()

    temp_construct['date'] =  ttt['date']
    temp_construct['date'] = pd.to_datetime(temp_construct['date'])
    temp_construct['date'] = temp_construct['date'].astype(str)
    temp_construct['date'] = temp_construct['date'].str.replace('\D', '').astype(int)
    temp_construct['day'] = range(0, num_of_days)

    temp_construct = pd.concat([temp_construct]*df_region.shape[0], ignore_index=True)
    temp_construct.head()

    df_region = pd.concat([df_region]*num_of_days, ignore_index=True)
    df_region = df_region.sort_values(['region'], ascending=[True])

    df_region = df_region.reset_index()
    df_region = df_region.drop(['index'], axis=1)
    df_region.head()

    temp_construct['region'] = df_region['region']

    t_region_confirmed_data = t_region_confirmed_data.transpose()
    t_region_confirmed_growth_data = t_region_confirmed_growth_data.transpose()
    t_region_death_data = t_region_death_data.transpose()

    a1 = np.reshape(t_region_confirmed_data.values,(t_region_confirmed_data.shape[0] * t_region_confirmed_data.shape[1], 1), order='F')
    df1 = pd.DataFrame(a1)

    a2 = np.reshape(t_region_death_data.values,(t_region_death_data.shape[0] * t_region_death_data.shape[1], 1), order='F')
    df2 = pd.DataFrame(a2)

    a3 = np.reshape(t_region_confirmed_growth_data.values,(t_region_confirmed_growth_data.shape[0] * t_region_confirmed_growth_data.shape[1], 1), order='F')
    df3 = pd.DataFrame(a3)

    temp_construct['confirmed'] = df1[0]
    temp_construct['deaths'] = df2[0]
    temp_construct['growth'] = df3[0]

    temp_construct.head()
    temp_construct = temp_construct.sort_values(['date'], ascending=True)

    temp_construct = temp_construct.fillna(0)    
    return temp_construct


# United States of America Python Dictionary to translate States,
# Districts & Territories to Two-Letter codes and vice versa.
#
# https://gist.github.com/rogerallen/1583593
#
# Dedicated to the public domain.  To the extent possible under law,
# Roger Allen has waived all copyright and related or neighboring
# rights to this code.

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}