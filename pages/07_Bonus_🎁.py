import streamlit as st
import pandas as pd
import plotly.express as px
from Introduction import footer
from urllib.request import urlopen
import json
import plotly.graph_objects as go

st.markdown("# Bonus 🎁")
st.sidebar.markdown("# Bonus 🎁")
st.markdown(footer, unsafe_allow_html=True)

st.markdown("Are you a Lionel Messi fan? We give you the chance to live in a District as close as possible to the "
            "house of the superstar, increasing the chances of a surprise encounter.")

st.markdown('### The house of Lionel Messi')


def get_geopoints():
    with urlopen(
            'https://raw.githubusercontent.com/martgnz/bcn-geodata/master/districtes/districtes.geojson') as response:
        return json.load(response)


def get_distribution_fig(map_style):
    geopoints = get_geopoints()
    districts = ['Ciutat Vella', 'Eixample', 'Gràcia', 'Horta-Guinardó', 'Les Corts', 'Nou Barris', 'Sant Andreu',
                 'Sant Martí', 'Sants-Montjuïc', 'Sarrià-Sant Gervasi']
    colors = ['rgb(128,0,0)', 'rgb(139,0,0)', 'rgb(165,42,42)', 'rgb(178,34,34)', 'rgb(220,20,60)', 'rgb(255,0,0)',
              'rgb(255,99,71)', 'rgb(255,127,80)', 'rgb(205,92,92)', 'rgb(240,128,128)']
    df = pd.DataFrame(list(zip(districts, colors)), columns=['District', 'Color'])
    distribution_fig = px.choropleth_mapbox(df, geojson=geopoints, locations=df['District'], color=df['Color'],
                                            featureidkey="properties.NOM", center={"lat": 41.37, "lon": 2.1},
                                            height=500, zoom=10, opacity=0.8, hover_name='District',
                                            hover_data={'Color': False, 'District': False},
                                            title='Location of the Residence of Lionel Messi'
                                            )

    distribution_fig.data[0].name = 'Districts of Barcelona'

    distribution_fig.add_trace(go.Scattermapbox(
        lon=['1.9533844637972901'],
        lat=['41.272137459163275'],
        hovertemplate='The House of Lionel Messi',
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=20
        ),
        text=['The House of Lionel Messi']
    ))
    distribution_fig.data[-1].name = 'The House of Lionel Messi'
    distribution_fig.update_layout(mapbox_style=map_style)
    distribution_fig.update_layout(showlegend=False)
    distribution_fig.update_layout(margin={'r': 0, 't': 50, 'l': 0, 'b': 0})
    return distribution_fig


map_style_select = st.selectbox('Choose the Map Style you want',
                                options=['carto-darkmatter', 'carto-positron', 'open-street-map', 'stamen-terrain',
                                         'stamen-toner', 'stamen-watercolor'])
st.plotly_chart(get_distribution_fig(map_style_select))

