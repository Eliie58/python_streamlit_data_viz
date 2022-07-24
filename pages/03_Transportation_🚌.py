import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import plotly.express as px
from Introduction import footer

st.markdown("# Transportation 🚌")
st.sidebar.markdown("# Transportation 🚌")

st.markdown("Access to public transport is a top priority for anyone who does not rely on a car, or other personal "
            "transportation device (bike, scooter, ...) as a main means of transport. Let's discover the distribution "
            "of Bus Stops in Barcelona City.")


def plot_map(data, elevation, lon=2.185272, lat=41.416365, zoom=12):
    st.write(
        pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state={
                'latitude': lat,
                'longitude': lon,
                'zoom': zoom,
                'pitch': 50,
            },
            layers=[
                pdk.Layer(
                    'ColumnLayer',
                    data=data,
                    get_elevation=elevation,
                    get_position=['Longitude', 'Latitude'],
                    radius=200,
                    elevation_scale=20,
                    elevation_range=[0, 10000],
                    get_fill_color=[48, 128, 255, 255]
                ),
            ],
        )
    )


bus_stop_new_name = 'Bus_Stop'

df_bus_stops = pd.read_csv('archive/bus_stops.csv').dropna().rename(columns={'Bus.Stop': bus_stop_new_name})

df_mean_latitudes = df_bus_stops[
    [bus_stop_new_name, 'District.Name', 'Neighborhood.Name', 'Longitude', 'Latitude']].groupby(
    by=['District.Name', 'Neighborhood.Name']).agg({bus_stop_new_name: 'count', 'Longitude': 'mean', 'Latitude': 'mean'})

plot_map(df_mean_latitudes, bus_stop_new_name)

df_transport = pd.read_csv('archive/transports.csv').rename(columns={'Transport': 'Means of transport'})
df_transport.dropna(inplace=True)

chosen_means_of_transport = np.sort(df_transport['Means of transport'].unique())
selected_means_of_transport = st.multiselect(
    'Stations for which means of transport you want to display on the map',
    chosen_means_of_transport,
    default=chosen_means_of_transport
)

filtered_df_transport = df_transport[df_transport['Means of transport'].isin(selected_means_of_transport)]

fig_map_transport = px.scatter_mapbox(filtered_df_transport,
                                      lat='Latitude',
                                      lon='Longitude',
                                      color='Means of transport',
                                      zoom=10,
                                      height=300,
                                      hover_name=filtered_df_transport['Station'],
                                      hover_data=['Means of transport', 'District.Name', 'Neighborhood.Name'],
                                      title='Public transport entry')

fig_map_transport.update_layout(mapbox_style='open-street-map')
fig_map_transport.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
fig_map_transport

st.markdown(footer, unsafe_allow_html=True)
