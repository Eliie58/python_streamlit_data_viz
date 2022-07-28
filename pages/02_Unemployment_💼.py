import streamlit as st
import pandas as pd
import plotly.express as px
from Introduction import footer

st.markdown("# Unemployment 💼")
st.sidebar.markdown("# Unemployment 💼")
st.markdown(footer, unsafe_allow_html=True)


def get_path(focus):
    if focus == 'Gender':
        return ['Gender', 'District Name']
    else:
        return ['District Name', 'Gender']


def get_sunburst_df(df, year):
    # Make a copy of the original dataframe
    df_copy = df.copy()
    # We only care about Registered Unemployed people
    df_copy = df_copy[df_copy['Demand_occupation'] == 'Registered unemployed']
    # Filter by year
    df_copy = df_copy[df_copy['Year'] == year]
    # Group by Gender and District, to get yearly data, instead of monthly data
    df_copy = df_copy.groupby(['Gender', 'District Name'])[['Gender', 'District Name', 'Number']].sum().reset_index()
    # Get the average Monthly Unemployment numbers
    df_copy['Number'] = (df_copy['Number'] / 12).astype(int)
    return df_copy


def get_trend_over_time_df(df):
    # Make a copy of the original dataframe
    df_copy = df.copy()
    # We only care about Registered Unemployed people
    df_copy = df_copy[df_copy['Demand_occupation'] == 'Registered unemployed']
    # Group by Year, month and District
    df_copy = df_copy.groupby(['Year', 'Month', 'District Name'])[['Year', 'Month', 'District Name', 'Number']].sum() \
        .drop(columns=['Year']).reset_index()

    month_labels = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05',
                    'June': '06', 'July': '07', 'August': '08', 'September': '09',
                    'October': '10', 'November': '11', 'December': '12'}
    # Add a new column to use for Sorting
    df_copy['Year'] = df_copy['Year'].map(str) + '-' + df_copy['Month'].map(month_labels)
    return df_copy.sort_values('Year').rename(columns={'Number': 'Registered unemployed'})


def get_treemap_df(df, district, is_proportional):
    # Make a copy of the original dataframe
    df_copy = df.copy()
    # We only care about Registered Unemployed people
    df_copy = df_copy[df_copy['Demand_occupation'] == 'Registered unemployed']
    # Filter by district
    df_copy = df_copy[df_copy['District Name'] == district]
    # Group By Year and Neighborhood Name
    df_copy = df_copy.groupby(['Year', 'Neighborhood Name'])[
        ['Year', 'Neighborhood Name', 'Number']].sum().drop(columns=['Year']).reset_index()
    # Get the average Unemployment Number per Month
    df_copy['Number'] = (df_copy['Number'] / 12).astype(int)
    if is_proportional:
        # Get population dataframe and filter by district
        pop_df = pd.read_csv('archive/population.csv')
        pop_df = pop_df[pop_df['District.Name'] == district]
        # Merge treemap with population Information
        df_copy = df_copy.merge(pop_df, left_on=['Neighborhood Name', 'Year'], right_on=['Neighborhood.Name', 'Year'],
                                how='inner')
        df_copy['Registered unemployed'] = (df_copy['Number_x'] * 100 / df_copy['Number_y'])
    else:
        df_copy = df_copy.rename(columns={'Number': 'Registered unemployed'})
    return df_copy


def get_treemap_path(district, includes_year):
    if includes_year:
        return [px.Constant(district), 'Neighborhood Name', 'Year']
    else:
        return [px.Constant(district), 'Neighborhood Name']


st.markdown("Unemployment rates can differ greatly from one district to another, based on multiple factors, "
            "including transportation networks, distance to financial and governmental centers, "
            "type of neighborhoods (housing, business, ...). In the following charts you can compare the Unemployment "
            "numbers, and find the best fit for you.")

st.markdown('### Unemployment By Gender and District')

df_district_unemployment = pd.read_csv('archive/unemployment.csv', na_values='No consta')
df_district_unemployment.dropna(inplace=True)

left_col, right_col = st.columns(2)

with left_col:
    st.markdown('Choose the main focus of the Sunburst Chart. When you choose gender, you will see the overall '
                'Unemployment statistics by Gender, and for each gender, the distribution per District. However '
                'choosing District, will switch the order of the plot.')
    focus_on = st.radio("Focus on:", ["Gender", "District"])

with right_col:
    st.markdown('Choose the year that you want to see more information about')
    year_radio = st.radio("Year:", df_district_unemployment['Year'].unique())

sunburst_df = get_sunburst_df(df_district_unemployment, year_radio)
sunburst_fig = px.sunburst(sunburst_df, path=get_path(focus_on), values='Number', color_continuous_scale='RdBu',
                           title=f'Unemployment distribution Per {focus_on} for {year_radio}')
sunburst_fig.update_traces(textinfo="label+percent entry")
st.plotly_chart(sunburst_fig)

st.markdown('### Unemployment trends Over time')

trend_over_time_df = get_trend_over_time_df(df_district_unemployment)

fig_district_unemployment = px.line(trend_over_time_df, x='Year', y='Registered unemployed', color='District Name',
                                    title='Number of unemployed people by district through time')

st.plotly_chart(fig_district_unemployment)

st.markdown('### Unemployment Distribution by Neighborhood')
district_selected = st.selectbox(
    'Which district you want to display unemployment information by neighborhood for?',
    sorted(df_district_unemployment['District Name'].unique())
)

left_col, right_col = st.columns(2)

with left_col:
    proportional = st.checkbox('Proportional to Population')

with right_col:
    include_year = st.checkbox('Include Year')

treemap_df = get_treemap_df(df_district_unemployment, district_selected, proportional)

treemap_fig = px.treemap(treemap_df,
                         path=get_treemap_path(district_selected, include_year), values='Registered unemployed',
                         title='Proportion of unemployed people for chosen district per neighborhood')
treemap_fig.update_traces(root_color="lightgrey")
treemap_fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
st.plotly_chart(treemap_fig)

st.markdown('### Conclusion')
st.markdown('From the First chart, we can see there is an advantage to residing in a District with low Numbers of '
            'Unemployment, such as "Les Corts", and it''s advisable to stay away from other districts with high '
            'Unemployment Rates, such as "Sant Marti"')
st.markdown('The "Unemployment trends Over time" chart helps us see the downward trend of Unemployment throughout the '
            'city. As opposed to the previous chart, we can see that "Sant Marti" is the district with the fastest '
            'decline in Unemployment Numbers, which can indicate a booming market.')
st.markdown('Finally, using the "Unemployment Distribution by Neighborhood" Treemap, we can dive into the '
            'Neighborhood level, after locking down a preferred District.')
