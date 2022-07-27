import streamlit as st
import pandas as pd
import random
from Introduction import footer
import plotly.graph_objects as go

colors = ['rgb(128,0,0)', 'rgb(139,0,0)', 'rgb(165,42,42)', 'rgb(178,34,34)', 'rgb(220,20,60)', 'rgb(255,0,0)',
          'rgb(255,99,71)', 'rgb(255,127,80)', 'rgb(205,92,92)', 'rgb(240,128,128)', 'rgb(233,150,122)',
          'rgb(250,128,114)', 'rgb(255,160,122)', 'rgb(255,69,0)', 'rgb(255,140,0)', 'rgb(255,165,0)', 'rgb(255,215,0)',
          'rgb(184,134,11)', 'rgb(218,165,32)', 'rgb(238,232,170)', 'rgb(189,183,107)', 'rgb(240,230,140)',
          'rgb(128,128,0)', 'rgb(255,255,0)', 'rgb(154,205,50)', 'rgb(85,107,47)', 'rgb(107,142,35)', 'rgb(124,252,0)',
          'rgb(127,255,0)', 'rgb(173,255,47)', 'rgb(0,100,0)', 'rgb(0,128,0)', 'rgb(34,139,34)', 'rgb(0,255,0)',
          'rgb(50,205,50)', 'rgb(144,238,144)', 'rgb(152,251,152)', 'rgb(143,188,143)', 'rgb(0,250,154)',
          'rgb(0,255,127)', 'rgb(46,139,87)', 'rgb(102,205,170)', 'rgb(60,179,113)', 'rgb(32,178,170)', 'rgb(47,79,79)',
          'rgb(0,128,128)', 'rgb(0,139,139)', 'rgb(0,255,255)', 'rgb(0,255,255)', 'rgb(224,255,255)', 'rgb(0,206,209)',
          'rgb(64,224,208)', 'rgb(72,209,204)', 'rgb(175,238,238)', 'rgb(127,255,212)', 'rgb(176,224,230)',
          'rgb(95,158,160)', 'rgb(70,130,180)', 'rgb(100,149,237)', 'rgb(0,191,255)', 'rgb(30,144,255)',
          'rgb(173,216,230)', 'rgb(135,206,235)', 'rgb(135,206,250)', 'rgb(25,25,112)', 'rgb(0,0,128)', 'rgb(0,0,139)',
          'rgb(0,0,205)', 'rgb(0,0,255)', 'rgb(65,105,225)', 'rgb(138,43,226)', 'rgb(75,0,130)', 'rgb(72,61,139)',
          'rgb(106,90,205)', 'rgb(123,104,238)', 'rgb(147,112,219)', 'rgb(139,0,139)', 'rgb(148,0,211)',
          'rgb(153,50,204)', 'rgb(186,85,211)', 'rgb(128,0,128)', 'rgb(216,191,216)', 'rgb(221,160,221)',
          'rgb(238,130,238)', 'rgb(255,0,255)', 'rgb(218,112,214)', 'rgb(199,21,133)', 'rgb(219,112,147)',
          'rgb(255,20,147)', 'rgb(255,105,180)', 'rgb(255,182,193)', 'rgb(255,192,203)', 'rgb(250,235,215)',
          'rgb(245,245,220)', 'rgb(255,228,196)', 'rgb(255,235,205)', 'rgb(245,222,179)', 'rgb(255,248,220)',
          'rgb(255,250,205)', 'rgb(250,250,210)', 'rgb(255,255,224)', 'rgb(139,69,19)', 'rgb(160,82,45)',
          'rgb(210,105,30)', 'rgb(205,133,63)', 'rgb(244,164,96)', 'rgb(222,184,135)', 'rgb(210,180,140)',
          'rgb(188,143,143)', 'rgb(255,228,181)', 'rgb(255,222,173)', 'rgb(255,218,185)', 'rgb(255,228,225)',
          'rgb(255,240,245)', 'rgb(250,240,230)', 'rgb(253,245,230)', 'rgb(255,239,213)', 'rgb(255,245,238)',
          'rgb(245,255,250)', 'rgb(112,128,144)', 'rgb(119,136,153)', 'rgb(176,196,222)', 'rgb(230,230,250)',
          'rgb(255,250,240)', 'rgb(240,248,255)', 'rgb(248,248,255)', 'rgb(240,255,240)', 'rgb(255,255,240)',
          'rgb(240,255,255)', 'rgb(255,250,250)', 'rgb(0,0,0)', 'rgb(105,105,105)', 'rgb(128,128,128)',
          'rgb(169,169,169)', 'rgb(192,192,192)', 'rgb(211,211,211)', 'rgb(220,220,220)', 'rgb(245,245,245)']


def get_immigration_df():
    df = pd.read_csv('archive/immigrants_by_nationality.csv', na_values='No consta').dropna()
    return df.groupby(['District Name', 'Nationality'])[['District Name', 'Nationality', 'Number']].sum().reset_index()


def plot_immigration_df(df, nationality):
    df = df[df['Nationality'] == nationality].sort_values(by=['Number'], ascending=False).reset_index(drop=False)

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=[nationality] + df['District Name'].to_list(),
            hovertemplate='Total for %{label} : %{value}'
        ),
        link=dict(
            source=[0] * len(df),  # indices correspond to labels, eg A1, A2, A1, B1, ...
            target=(df.index + 1).to_list(),
            value=df['Number'].to_list(),
            color=random.sample(colors, k=len(df)),
            hovertemplate='%{target.value} Nationals moved from %{source.label} to %{target.label}',
        ))])

    fig.update_layout(title_text=f"Distribution of {nationality} Nationals around Barcelona Districts",
                      font_size=10)
    fig.update_layout(
        height=600,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=50
        )
    )
    st.plotly_chart(fig)


st.markdown("# Immigration 🛬")
st.sidebar.markdown("# Immigration 🛬")
st.markdown(footer, unsafe_allow_html=True)

st.markdown("As an Immigrant moving to Barcelona, finding members from your same culture can make the move easier, "
            "and help you to integrate the Spanish and Barcelonian societies. Take a look at the charts below, "
            "and find out where your compatriots are residing.")

st.markdown('### Distribution of Immigrants in Barcelona')

immigration_df = get_immigration_df()

chosen_nationality = st.selectbox('What is the nationality you are interested in?',
                                  sorted(immigration_df['Nationality'].unique()))
plot_immigration_df(immigration_df, chosen_nationality)

st.markdown('### Conclusion')
st.markdown('In this Diagram, we can see the flow of Immigration from Countries to the different Districts in '
            'Barcelona. You can pick the country of your choice, and see how its nationals are distributed.')
