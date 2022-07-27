import streamlit as st
from Introduction import footer

st.markdown("# Conclusion")
st.sidebar.markdown("# Conclusion")
st.markdown(footer, unsafe_allow_html=True)

st.markdown('This website will help get a statistical understanding of Barcelona City.')
st.markdown('### [Car Accidents 🚗](Car_Accidents_🚗)', unsafe_allow_html=True)
st.markdown('If you are interested in Car safety, this page is your guide to avoiding areas with high numbers of Car '
            'accidents.')
st.markdown('### [Unemployment 💼](Unemployment_💼)', unsafe_allow_html=True)
st.markdown('Are you moving to Barcelona in search for a job? This page will help you decide which district is ideal '
            'for finding a job opportunity')
st.markdown('### [Transportation 🚌](Transportation_🚌)', unsafe_allow_html=True)
st.markdown('This page is your go to guide to understand the public transport network in Barcelona')
st.markdown('### [Life Expectancy 👵 👴](Life_Excpectancy_👵_👴)', unsafe_allow_html=True)
st.markdown('Life expectancy measures can be a great way to understand the overall health conditions in a District. '
            'Use this page as a shortuct in your reasearch for the healthiest district in Barcelona')
st.markdown('### [Child Birth 👶](Child_Birth_👶)', unsafe_allow_html=True)
st.markdown('For new families, the indicator of child births in a district can be very helpful. This page will '
            'highlight the different criteria related to Child Birth in Barcelona.')
st.markdown('### [Immigration 🛬](Immigration_🛬)', unsafe_allow_html=True)
st.markdown('Homesick? Find your compatriots using the information in this page.')
st.markdown('### [Bonus 🎁](Bonus_🎁)', unsafe_allow_html=True)
st.markdown('Still not convinced to move to Barcelona? Take a peak here.')
