import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from Introduction import footer

st.markdown("# Unemployment 💼")
st.sidebar.markdown("# Unemployment 💼")
st.markdown(footer, unsafe_allow_html=True)

st.markdown("Unemployment rates can differ greatly from one district to another, based on multiple factors, "
            "including transportation networks, distance to financial and governmental centers, "
            "type of neighborhoods (housing, business, ...). In the following charts you can compare the Unemployment "
            "numbers, and find the best fit for you.")

df_district_unemployment = pd.read_csv('archive/unemployment.csv', na_values='No consta')
df_district_unemployment.dropna(inplace=True)
unique_districts = np.sort(df_district_unemployment['District Name'].unique())
districts_selected = st.multiselect(
    'Which districts you want to display',
    unique_districts,
    default=unique_districts
)

filtered_df_district = \
    df_district_unemployment[(df_district_unemployment['Demand_occupation'] == 'Registered unemployed')
                             & (df_district_unemployment['District Name'].isin(districts_selected))
                             ].groupby(['Year', 'Month', 'District Name']).sum().reset_index()
month_labels = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05',
                'June': '06', 'July': '07', 'August': '08', 'September': '09',
                'October': '10', 'November': '11', 'December': '12'}

filtered_df_district['Month num'] = filtered_df_district['Month'].apply(lambda x: month_labels[x])

for i in range(len(filtered_df_district)):
    result = str(filtered_df_district.loc[i, 'Year']) + '-' + str(
        filtered_df_district.loc[i, 'Month num'])
    filtered_df_district.loc[i, 'month'] = result

fig_district_unemployment = px.line(
    filtered_df_district.sort_values('month').rename(columns={'Number': 'Registered unemployed'}),
    x='month',
    y='Registered unemployed',
    color='District Name',
    title='Number of unemployed people by district through time')

fig_district_unemployment

district_selected = st.selectbox(
    'Which district you want to display unemployment information by neighborhood for?',
    unique_districts
)

filtered_df_district_unemployment_treemap = df_district_unemployment[
    (df_district_unemployment['Demand_occupation'] == 'Registered unemployed')
    & (df_district_unemployment['District Name'] == district_selected)
    ].groupby(['District Name', 'Neighborhood Name']).sum().reset_index().rename(
    columns={'Number': 'Registered unemployed'})

fig_treemap_unemployment = px.treemap(filtered_df_district_unemployment_treemap,
                                      path=['District Name', 'Neighborhood Name'],
                                      values='Registered unemployed',
                                      color='Registered unemployed',
                                      title='Proportion of unemployed people for chosen district per neighborhood')
fig_treemap_unemployment

df_district_unemployment_gender = pd.read_csv('archive/unemployment.csv', na_values='No consta')
df_district_unemployment_gender.dropna(inplace=True)
unique_districts_gender = np.sort(df_district_unemployment_gender['District Name'].unique())
district_selected_gender = st.selectbox(
    'Which district you want to show unemployment by gender information for?',
    unique_districts_gender
)

filtered_df_district_gender = \
    df_district_unemployment_gender[(df_district_unemployment_gender['Demand_occupation'] == 'Registered unemployed')
                                    & (df_district_unemployment_gender['District Name'] == district_selected_gender)
                                    & (df_district_unemployment_gender['Year'] == 2017)
                                    & (df_district_unemployment_gender['Month'] == 'January')
                                    ][['District Name', 'Gender', 'Number']].groupby(
        ['District Name', 'Gender']).sum().reset_index()
fig_pie_chart_unemployment_by_gender = px.pie(filtered_df_district_gender, values='Number', names='Gender',
                                              title='Proportion of male/female unemployed for ' +
                                                    district_selected_gender
                                                    + ' district')
fig_pie_chart_unemployment_by_gender

