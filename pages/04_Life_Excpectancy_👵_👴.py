import streamlit as st
import pandas as pd
import plotly.express as px
from Introduction import footer

st.markdown("# Life Expectancy 👵 👴")
st.sidebar.markdown("# Life Expectancy 👵 👴")
st.markdown(footer, unsafe_allow_html=True)

st.markdown("Who doesn't wanna live to an old age, and enjoy life until the last possible second? Many factors can "
            "affect a person's life expectancy, ranging from the obvious (pollution, safety) to the unexpected such "
            "as distance from the sea. In the below charts we will see the life Expectancy in Barcelona.")

st.markdown('### Neighborhood Life Expectancy Ranking')


def get_life_expectancy_dfs():
    # Read Dataframe from CSV
    df = pd.read_csv('archive/life_expectancy.csv').dropna()
    # Split into 2 Dataframes, one for each gender
    return df[df['Gender'] == 'Male'], df[df['Gender'] == 'Female']


def plot_df(df, date_period, ranking, gender):
    # Sort, and reset the index
    df = df.sort_values(by=[date_period], ascending=False, inplace=False).reset_index(drop=True)
    # Increment the index by 1, to start from 1 instead of 0
    df.index = df.index + 1
    # Create a new Column for Ranking
    df['Ranking'] = df.index
    life_expectancy_fig = px.bar(df.loc[ranking[0]: ranking[1]], x='Neighborhood', y=date_period, text='Ranking',
                                 labels={date_period: 'Average Life Expectancy'},
                                 title=f'{gender} Life Expectancy By Neighborhood (Rank {ranking[0]} to {ranking[1]})')
    life_expectancy_fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                                      marker_line_width=1.5, opacity=0.6)
    st.plotly_chart(life_expectancy_fig)


male_df, female_df = get_life_expectancy_dfs()

left_col, right_col = st.columns(2)

df_male_life_expectancy, df_female_life_expectancy = get_life_expectancy_dfs()
with left_col:
    date_period_select = st.selectbox('Choose the appropriate Date Period',
                                      sorted(df_male_life_expectancy.columns[1:-2]))

with right_col:
    ranking_slider = st.slider('Choose the ranking you want to Visualize', 1, len(df_male_life_expectancy), (1, 5))

plot_df(df_female_life_expectancy, date_period_select, ranking_slider, 'Female')
plot_df(df_male_life_expectancy, date_period_select, ranking_slider, 'Male')
