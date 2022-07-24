import streamlit as st
import pandas as pd
import plotly.express as px
from Introduction import footer

st.markdown("# Immigration 🛬")
st.sidebar.markdown("# Immigration 🛬")

df_immigrants = pd.read_csv('archive/immigrants_by_nationality.csv', na_values='No consta').dropna()

st.markdown("As an Immigrant moving to Barcelona, finding members from your same culture can make the move easier, "
            "and help you to integrate the Spanish and Barcelonian societies. Take a look at the charts below, "
            "and find out where your compatriots are residing.")

chosen_nationality = st.selectbox(
    'From what nationality you want to show district distribution information?',
    df_immigrants['Nationality'].unique())

df_immigrants_by_district_and_nationality = df_immigrants[
                                                df_immigrants['Nationality'] == chosen_nationality].loc[:,
                                            ['District Name', 'Nationality', 'Number']] \
    .groupby(['District Name', 'Nationality']).sum().reset_index()
fig_pie_chart = px.pie(df_immigrants_by_district_and_nationality, values='Number', names='District Name',
                       title='Distribution of immigrants from ' + chosen_nationality + ' per district')

fig_pie_chart

st.markdown(footer, unsafe_allow_html=True)
