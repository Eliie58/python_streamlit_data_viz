import imp
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from Introduction import footer
import json
from urllib.request import urlopen

st.markdown("# Car Accidents 🚗")
st.sidebar.markdown("# Car Accidents 🚗")
st.markdown(footer, unsafe_allow_html=True)

st.markdown("For families looking to move, car safety is a major concern. In this page we can see the location of car "
            "accidents in Barcelona during 2017, alongside the exact time, and number of injuries.")

df_victims = pd.read_csv('archive/accidents_2017.csv', na_values='Unknown')

df_victims.dropna(inplace=True)

def get_geopoints(chart_type):
    if chart_type == "District":
        with urlopen(
                'https://raw.githubusercontent.com/martgnz/bcn-geodata/master/districtes/districtes.geojson') as response:
            return json.load(response)
    else:
        with urlopen('https://raw.githubusercontent.com/martgnz/bcn-geodata/master/barris/barris.geojson') as response:
            return json.load(response)


def get_victims_distribution(chart_type, population_dataframe):
    if chart_type == "District":
        df = pd.DataFrame({'Accident Count': df_victims['District Name'].value_counts()})
        grouped_population_df = population_dataframe.groupby('District.Name')[['District.Name', 'Number']].sum()
    else:
        df = pd.DataFrame({'Accident Count': df_victims['Neighborhood Name'].value_counts()})
        grouped_population_df = population_dataframe.groupby('Neighborhood.Name')[['Neighborhood.Name', 'Number']].sum()

    df = df.merge(grouped_population_df, left_index=True, right_index=True, how='inner')
    df['Accidents per 1000 Residents'] = df['Accident Count'] * 1000 / df['Number']
    return df


st.markdown('### Card Accident Distribution')

left_col, right_col = st.columns(2)

with left_col:
    chart_tp = st.radio("Accident Distribution:", ["District", "Neighborhood"])

with right_col:
    output_tp = st.radio("Chart Type:", ["Accident Count", "Accidents per 1000 Residents"])

population_df = pd.read_csv('archive/population.csv')
victims_df = get_victims_distribution(chart_tp, population_df)
geopoints = get_geopoints(chart_tp)

victim_distribution_fig = px.choropleth_mapbox(victims_df, geojson=geopoints, color=output_tp,
                                               locations=victims_df.index,
                                               title='Car Accidents Distribution',
                                               color_continuous_scale="Turbo",
                                               featureidkey="properties.NOM",
                                               center={"lat": 41.390205, "lon": 2.154007},
                                               mapbox_style="open-street-map", zoom=10,
                                               opacity=0.5, labels={'index': chart_tp}
                                               )
victim_distribution_fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
victim_distribution_fig.update_layout(mapbox_style='open-street-map')
victim_distribution_fig

st.markdown('#### Accident Count')
st.markdown('##### By District')
st.markdown('In this chart, we see the distribution of Car Accidents in Barcelona. We can choose to group by '
            'District, or Neighborhoods. On the district level, we can see Eixample is the riskiest District, '
            'with over 3000 accidents. Gracia however seems to be hte safest, with just over 500 accidents.')
st.markdown('##### By Neighborhood')
st.markdown('If we switch to the Neighborhood level, we can see that "la Dreta de l''Eixample" in the district of '
            'Eixample is thh most dangerous, with over 1000 car accidents. We can also observe that the farther we '
            'get from the City center, the less car accidents occur')
st.markdown('#### Accidents per 1000 Residents')
st.markdown('The raw accident count per District or Neighborhood may be misleading. To get a more proportional view, '
            'we will use Number of Accidents, per 1000 residents.')
st.markdown('##### By District')
st.markdown('We can clearly see a more equilibrated distribution. In place of a risky center, and more secure '
            'peripheries, now we can see that the north of the city is the safest region.')
st.markdown('##### By Neighborhood')
st.markdown('We can easily spot an outlier in "la Marina del Plat Vermell" neighborhood, with a extremly high nigh '
            'number of accidents. This can be explained by the low population count of this neighborhood.')

st.markdown('### Accident Distribution by Weekdays and Districts')

df_accidents = pd.read_csv('archive/accidents_2017.csv', na_values='Unknown').rename(
    columns={
        'District Name': 'District', 'Part of the day': 'Most frequent accident time'})

df_accidents.dropna(inplace=True)
df_victims_by_district_and_weekday = df_accidents.loc[:, ['District', 'Weekday', 'Victims', 'Most frequent accident '
                                                                                            'time']].groupby(
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

st.markdown('The most noticeable part of this scatter plot, is Eixample district. We can see that throughout the '
            'week, the accidents take place mostly in the afternoon, which can be explained by the after work rush '
            'hour.')
st.markdown('In Horta-Guinardo district, we see a spike of Car Accidents in the morning during the weekdays, '
            'which is a turn-off for parents worried about the morning drive to school.')
st.markdown('### Conclusion')
st.markdown('As long as you stay away from "Eixample" district, and "la Marina del Plat Vermell" neighborhood, '
            'you are less likely to take part in a Car Accident.')
