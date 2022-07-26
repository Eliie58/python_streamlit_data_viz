import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
from Introduction import footer
from urllib.request import urlopen
import json
import plotly.graph_objects as go

st.markdown("# Transportation 🚌")
st.sidebar.markdown("# Transportation 🚌")
st.markdown(footer, unsafe_allow_html=True)

st.markdown("Access to public transport is a top priority for anyone who does not rely on a car, or other personal "
            "transportation device (bike, scooter, ...) as a main means of transport. Let's discover the distribution "
            "of Bus Stops in Barcelona City.")


def get_deck_df(df, selected_districts, grouped_by):
    # Make a copy of the original Dataframe
    df_copy = df.copy()
    # Filter by selected districts
    df_copy = df_copy[df_copy['District.Name'].isin(selected_districts)]
    if grouped_by == 'Neighborhood':
        # Group the bus stops by District and Neighborhood, and get the mean of their Longitude and latitude
        df_copy = df_copy.groupby(['District.Name', 'Neighborhood.Name']).agg(
            {'Bus.Stop': 'count', 'Longitude': 'mean', 'Latitude': 'mean'})
    else:
        # Group the bus stops by District, and get the mean of their Longitude and latitude
        df_copy = df_copy.groupby(['District.Name']).agg({'Bus.Stop': 'count', 'Longitude': 'mean', 'Latitude': 'mean'})
    # Calculate the color, by scaling the Bus.Stop counts to between 0 and 255
    df_copy['color'] = (df_copy['Bus.Stop'] - df_copy['Bus.Stop'].min()) / (
            df_copy['Bus.Stop'].max() - df_copy['Bus.Stop'].min()) * 255
    return df_copy.reset_index().rename(columns={'Bus.Stop': 'Bus_Stop'})


def plot_map(df, selected_districts, grouped_by, lon=2.185272, lat=41.416365):
    if grouped_by == 'Neighborhood':
        zoom = 12
        elevation_scale = 20
    else:
        zoom = 11
        elevation_scale = 10
    tooltip = {
        "html": "<b>{Bus_Stop} Bus stops in the " +
                ("Neighborhood \"{Neighborhood.Name}\" of " if grouped_by == 'Neighborhood' else '') +
                "District \"{District.Name}\"</b>",
        "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
    }
    deck_df = get_deck_df(df, selected_districts, grouped_by)
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        tooltip=tooltip,
        initial_view_state={
            'latitude': lat,
            'longitude': lon,
            'zoom': zoom,
            'pitch': 50,
        },
        layers=[
            pdk.Layer(
                'ColumnLayer',
                data=deck_df,
                get_elevation='Bus_Stop',
                get_position=['Longitude', 'Latitude'],
                radius=200,
                elevation_scale=elevation_scale,
                elevation_range=[0, 1000],
                get_fill_color=["color", "255 - color", 255, 140],
                pickable=True,
                auto_highlight=True
            ),
        ]
    ))


def get_geopoints():
    with urlopen(
            'https://raw.githubusercontent.com/martgnz/bcn-geodata/master/districtes/districtes.geojson') as response:
        return json.load(response)


def get_distribution_fig():
    geopoints = get_geopoints()
    df_transport = pd.read_csv('archive/transports.csv').rename(columns={'Transport': 'Means of transport'}).dropna()
    distribution_fig = px.choropleth_mapbox(df_transport.groupby('District.Name').count(), geojson=geopoints,
                                            color='Neighborhood.Name',
                                            locations=df_transport.groupby('District.Name').count().index,
                                            title='Car Accidents Distribution',
                                            color_continuous_scale="Blues",
                                            featureidkey="properties.NOM",
                                            center={"lat": 41.390205, "lon": 2.154007},
                                            height=500,
                                            zoom=11,
                                            opacity=0.5, labels={'Neighborhood.Name': 'Public Transport Stations',
                                                                 'District.Name': 'District Name'}
                                            )

    distribution_fig.data[0].coloraxis = None
    distribution_fig.update_traces(showscale=False)

    for mode_of_transport in df_transport['Means of transport'].unique():
        filtered = df_transport[df_transport['Means of transport'] == mode_of_transport]
        distribution_fig.add_trace(go.Scattermapbox(
            lat=filtered['Latitude'].to_list(),
            lon=filtered['Longitude'].to_list(),
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=5
            ),
            text=filtered['Station'].to_list()
        ))
        distribution_fig.data[-1].name = mode_of_transport
    distribution_fig.update_layout(mapbox_style='carto-positron')
    distribution_fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))
    distribution_fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    return distribution_fig


st.markdown('### Bus Stops Distribution')

bus_stops_df = pd.read_csv('archive/bus_stops.csv').dropna()

group_by = st.radio("Group By:", ["District", "Neighborhood"])
districts = st.multiselect('Choose the districts to see on the map', sorted(bus_stops_df['District.Name'].unique()),
                           default=sorted(bus_stops_df['District.Name'].unique()))
st.markdown(f'Bus Stops distribution by {group_by}')
plot_map(bus_stops_df, districts, group_by)

st.markdown('### Public Transport Stations')
st.markdown('In the below Map, we can see the distribution of Public Transport Stations around Barcelona. We can also '
            'toggle on and off the type of Public Transport, and the Map contains the total number of Public '
            'Transportation Station per District')
st.plotly_chart(get_distribution_fig())
st.markdown('### Conclusion')
st.markdown('The Bus Stops distribution map helps us to understand the abundance of Bus Stops in the Center of '
            'Barcelona, especially around "Eixample" district. The farther away from the center, the number of '
            'stations drops.')
st.markdown('If we dive deeper into Neighborhood level, our previous conclusion is validated.')
st.markdown('Buses are not the only mode of public transport available in Barcelona. The second map summarizes '
            'different types of Public transport. Our previous assumption is further validated by finding 120 public '
            'transport stations in "Eixample" district, more than any other district.')
st.markdown('However, after toggling off the "Underground" stations, we find that "Eixample" faces a lack of other '
            'types of transport. The tram that mainly services "Sant Marti", "Les Corts" and "Sarria Sant-Gervasi" '
            'barely ventures into "Eixample".')