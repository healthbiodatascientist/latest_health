#!/usr/bin/env python
# coding: utf-8

# Import packages/libraries

# In[1]:


import pandas as pd
from dash import Dash, html, dash_table
import dash_bootstrap_components as dbc


# Import data and create tables

# In[2]:


def no_geometry():
    df_hb_beds_filter = pd.read_csv('https://raw.githubusercontent.com/healthbiodatascientist/latest_health/refs/heads/main/mixed_latest_health_data.csv')
    df_hb_beds_filter = df_hb_beds_filter.set_index('HBCode')
    df_hb_beds_table = df_hb_beds_filter.drop('geometry', axis=1)
    return df_hb_beds_table
df_hb_beds_table = no_geometry()
df_numeric_columns = df_hb_beds_table.select_dtypes('number')


# Setup app layout

# In[3]:


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    
app.layout = dbc.Container([
    html.H1("Regional Scottish Health Board Acute Case Latest Mixed Date Data", className='mb-2', style={'padding': '10px 10px', 'textAlign':'center'}),
    dbc.Row([dbc.Col(html.Summary("The map below displays a mixed set of combined open source data from Public Health Scotland (PHS) and the Scottish Ambulance Service (SAS) for each of the Scottish Health Board Regions. Hover over your Health Board for an insight into the factors affecting the efficiency of acute care:", className='mb-2', style={'padding': '10px 10px', 'list-style': 'none'}))]),
    dbc.Row([dbc.Col(html.Iframe(id='my_output', height=600, width=1000, srcDoc=open('latestmap.html', 'r').read()))], style={'text-align':'center'}),
    html.Figcaption("Figure 1: Map of the latest mixed date open health data for the Scottish Health Board Regions", className='mb-2', style={'padding': '10px 10px', 'textAlign':'center'}),
    html.H4("SAS, NHS Scotland and Scottish Government Targets for 2023/24", className='mb-2', style={'margin-top': '1em', 'padding': '10px 10px', 'textAlign': 'center'}),
    html.Summary("Percentage Emergencies Attended/Conveyed (last updated Weekly 27/08/2025): No specific SAS targets set in 2023/24. However, high volumes of ambulance conveyances to A&E departments can significantly worsen waiting times. This is because increased ambulance arrivals can lead to overcrowding, putting strain on resources and staff, and ultimately resulting in longer waits for all patients, including those who arrive by other means", className='mb-2'),
    html.Summary("Median Ambulance Turnaround Time (min) (last updated Weekly 27/08/2025): Target of median turnaround time within 40 minutes set by SAS 2023/24", className='mb-2'),
    html.Summary("Percentage Within 4 Hours A&E, Percentage Over 4, 8, and 12 Hours A&E (last updated Weekly 17/08/2025): Target of 95% of people attending A&E should be seen, admitted, discharged, or transferred within 4 hours set by Scottish Government 2010", className='mb-2'),
    html.Summary("Percentage Occupancy Acute Beds (last updated Quarterly 31/12/2024): In NHS Scotland, 92% bed occupancy is considered a benchmark, but not an absolute standard. The 2023/24 operational planning guidance set 92% as the maximum for bed occupancy, as high occupancy can negatively impact patient flow, waiting times, and infection control", className='mb-2'),
    html.Figcaption("Table 1: Mixed latest date open health data for the Scottish Health Board Regions with the highest 50% of column values highlighted in dark blue", className='mb-2', style={'margin-bottom': '1em', 'padding': '10px 10px', 'textAlign':'center'}),
    dbc.Row([dbc.Col(dash_table.DataTable(
    data=df_hb_beds_table.to_dict('records'),
    sort_action='native',
    columns=[{'name': i, 'id': i} for i in df_hb_beds_table.columns],
    style_cell={'textAlign': 'center'},
    fixed_columns={'headers': True, 'data': 1},
    style_table={'minWidth': '100%'},
    style_data_conditional=
    [
            {
                'if': {
                    'filter_query': '{{{}}} > {}'.format(col, value),
                    'column_id': col
                },
                'backgroundColor': '#301934',
                'color': 'white'
            } for (col, value) in df_numeric_columns.quantile(0.1).items()
        ] +       
        [
            {
                'if': {
                    'filter_query': '{{{}}} <= {}'.format(col, value),
                    'column_id': col
                },
                'backgroundColor': '#A020F0',
                'color': 'white'
            } for (col, value) in df_numeric_columns.quantile(0.5).items()
        ]
    ))
    ]),
    html.H4("Open Data References", className='mb-2', style={'margin-top': '1em', 'padding': '10px 10px', 'textAlign': 'center'}),
    html.Summary("Public Health Scotland"),
    html.Li(html.Cite("https://publichealthscotland.scot/publications/acute-hospital-activity-and-nhs-beds-information-quarterly/acute-hospital-activity-and-nhs-beds-information-quarterly-quarter-ending-31-december-2024/data-files/")),
    html.Li(html.Cite("https://www.opendata.nhs.scot/dataset/0d57311a-db66-4eaa-bd6d-cc622b6cbdfa/resource/a5f7ca94-c810-41b5-a7c9-25c18d43e5a4/download/weekly_ae_activity_20250817.csv")),
    html.Summary("Scottish Ambulance Service"),
    html.Li(html.Cite("https://www.scottishambulance.com/publications/unscheduled-care-operational-statistics/")),
    html.Li(html.Cite("https://www.scottishambulance.com/media/teapv5hp/foi-24-296-service-target-times.pdf")),
    ])


# Run app

# In[4]:


if __name__ == "__main__":
    app.run()

