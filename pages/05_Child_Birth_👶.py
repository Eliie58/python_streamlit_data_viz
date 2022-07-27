import streamlit as st
import pandas as pd
import plotly.express as px
from Introduction import footer

st.markdown("# Child Birth 👶")
st.sidebar.markdown("# Child Birth 👶")
st.markdown(footer, unsafe_allow_html=True)

st.markdown("The socio-economic status of a region may change how easy or difficult it may be to have children. New "
            "families want to live in regions where birthing and raising small children is easy and widespread. This "
            "charts below will help in understanding the Child birth statistics around Barcelona.")


st.markdown('### Child Birth Distribution by District for every year')

df = pd.read_csv('archive/births.csv', na_values='No consta').dropna().groupby(
    ['Year', 'District Name', 'Gender']).sum().reset_index()

fig = px.scatter(df, x="District Name", y="Number", animation_frame="Year",
                 size="Number", color="Gender", hover_name="District Name",
                 labels={'Number': 'NUmber of Children born'},
                 title='Number of Children Born Every Year Per District in Barcelona')

st.plotly_chart(fig)
