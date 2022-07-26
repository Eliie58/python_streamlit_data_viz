import streamlit as st
import pandas as pd
from Introduction import footer
import plotly.graph_objects as go

st.markdown("# Child Birth 👶")
st.sidebar.markdown("# Child Birth 👶")
st.markdown(footer, unsafe_allow_html=True)

st.markdown("The socio-economic status of a region may change how easy or difficult it may be to have children. New "
            "families want to live in regions where birthing and raising small children is easy and widespread. This "
            "charts below will help in understanding the Child birth statistics around Barcelona.")

df_births = pd.read_csv('archive/births.csv', na_values='No consta').dropna()
df_births['Year'] = df_births['Year'].astype('int')
df_births.sort_values(by='Year', inplace=True)
df_births = df_births.reset_index()
unique_years_of_observation = df_births['Year'].unique()
min_year_of_observation_births = int(unique_years_of_observation[0])
max_year_of_observation_births = int(unique_years_of_observation[-1])

years_of_observation = st.slider(
    'For which years you want to show birth statistics by district?',
    min_year_of_observation_births,
    max_year_of_observation_births,
    (min_year_of_observation_births, max_year_of_observation_births)
)

fig_birth = go.Figure()
df_births_by_district_and_year = df_births[(df_births['Year'] >= years_of_observation[0]) & (
        df_births['Year'] <= years_of_observation[1])].loc[:, ['District Name', 'Number']].groupby(
    ['District Name']).sum().reset_index().sort_values(by='Number', ascending=False)

fig_birth.add_trace(go.Scatter(x=df_births_by_district_and_year['District Name'],
                               y=df_births_by_district_and_year['Number'],
                               mode='markers',
                               marker_color='darkorange',
                               marker_size=10))
for i in range(0, len(df_births_by_district_and_year)):
    fig_birth.add_shape(type='line',
                        x0=i, y0=0,
                        y1=df_births_by_district_and_year['Number'].to_numpy()[i],
                        x1=i,
                        line=dict(color='crimson', width=3))

fig_birth.update_layout(title_text=
                        'Number of children born in ' + str(min_year_of_observation_births)
                        + '-' + str(max_year_of_observation_births) + ' years by district',
                        title_font_size=20)

fig_birth.update_xaxes(title='District')
fig_birth.update_yaxes(title='Total number of children born')
fig_birth

