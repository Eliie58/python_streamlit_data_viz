import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from Introduction import footer

st.markdown("# Car Accidents 🚗")
st.sidebar.markdown("# Car Accidents 🚗")

st.markdown("For families looking to move, car safety is a major concern. In this page we can see the location of car "
            "accidents in Barcelona during 2017, alongside the exact time, and number of injuries.")

df_victims = pd.read_csv('archive/accidents_2017.csv', na_values='Unknown')

df_victims.dropna(inplace=True)

selected_number_of_victims = st.selectbox(
    'How many victims should accident involve?',
    np.sort(df_victims['Victims'].unique()))

filtered_df = df_victims[df_victims['Victims'] == selected_number_of_victims]

fig_map_accidents = px.scatter_mapbox(filtered_df,
                                      lat='Latitude',
                                      lon='Longitude',
                                      color='Weekday',
                                      zoom=10,
                                      height=300,
                                      hover_name='Accident No ' + filtered_df['Id'],
                                      hover_data=['District Name', 'Neighborhood Name', 'Street', 'Victims'],
                                      title='Accident localization per number of victims')

fig = px.density_mapbox(filtered_df, lat='Latitude', lon='Longitude', zoom=10,
                        mapbox_style="stamen-terrain",
                        height=300,
                        hover_name='Accident No ' + filtered_df['Id'],
                        hover_data=['District Name', 'Neighborhood Name', 'Street', 'Victims'],
                        title='Accident localization per number of victims')

fig_map_accidents.update_layout(mapbox_style='open-street-map')
fig_map_accidents.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
fig_map_accidents

df_accidents = pd.read_csv('archive/accidents_2017.csv', na_values='Unknown').rename(
    columns={
        'District Name': 'District', 'Part of the day': 'Most frequent accident time'})

df_accidents.dropna(inplace=True)
df_victims_by_district_and_weekday = df_accidents.loc[:,
                                     ['District', 'Weekday', 'Victims', 'Most frequent accident time']].groupby(
    ['District', 'Weekday']).agg({'Victims': 'sum', 'Most frequent accident time': pd.Series.mode, }).explode(
    'Most frequent accident time').reset_index()

fig_scatter_victims = px.scatter(df_victims_by_district_and_weekday,
                                 x='District',
                                 y='Weekday',
                                 size='Victims',
                                 color='Most frequent accident time',
                                 title='Number of victims represented by size of the bubbles by district and weekday '
                                       'of the accident '
                                 )
fig_scatter_victims

st.markdown(footer, unsafe_allow_html=True)
