import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from Introduction import footer

st.markdown("# Life Expectancy 👵 👴")
st.sidebar.markdown("# Life Expectancy 👵 👴")

st.markdown("Who doesn't wanna live to an old age, and enjoy life until the last possible second? Many factors can "
            "affect a person's life expectancy, ranging from the obvious (pollution, safety) to the unexpected such "
            "as distance from the sea. In the below charts we will see the life Expectancy in Barcelona.")

df_life_expectancy = pd.read_csv('archive/life_expectancy.csv')
df_life_expectancy.dropna(inplace=True)

selected_time_period_life_expectancy = st.selectbox(
    'For what time period you want to display life expectancy information?',
    np.sort(df_life_expectancy.columns[1:-2]))

df_life_expectancy_mean_by_neighborhood = df_life_expectancy.drop(columns=['Gender']).groupby(
    by=['Neighborhood']).mean().reset_index()

df_life_expectancy_bar_chart = df_life_expectancy_mean_by_neighborhood.loc[:,
                               ['Neighborhood', selected_time_period_life_expectancy]]
df_life_expectancy_bar_chart['Neighborhood'] = df_life_expectancy_mean_by_neighborhood['Neighborhood'].astype('string')
df_life_expectancy_bar_chart[selected_time_period_life_expectancy] = df_life_expectancy_mean_by_neighborhood[
    selected_time_period_life_expectancy].astype('float')
df_life_expectancy_bar_chart.sort_values(by=selected_time_period_life_expectancy, ascending=False, inplace=True)

number_of_best_districts_from = st.slider(
    'From what best neighborhood No in the rating by life expectancy you want to display?',
    1,
    len(df_life_expectancy_bar_chart['Neighborhood'].unique()),
    (1, 5))

fig_bar_chart_life_expectancy = px.bar(df_life_expectancy_bar_chart.iloc[
                                       (number_of_best_districts_from[0] - 1):(number_of_best_districts_from[1]),
                                       :],
                                       x='Neighborhood',
                                       y=selected_time_period_life_expectancy,
                                       labels={selected_time_period_life_expectancy: 'average life expectancy'},
                                       title='Displaying No' + str(number_of_best_districts_from[0]) + ' - No' + str(
                                           number_of_best_districts_from[1])
                                             + ' in the rating of neighborhoods with highest life expectancy')
fig_bar_chart_life_expectancy

st.markdown(footer, unsafe_allow_html=True)
