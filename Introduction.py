import streamlit as st

footer = """
<style>
footer:after {
    content : 'Created by Leonid Seniukov and Elie Yaacoub';
    display: block;
    position: relative;
    padding: 5px 0px;
    top: 3px;
}
</style>
"""

st.markdown("# Introduction")
st.sidebar.markdown("# Introduction")

st.markdown("### A new City")
st.markdown("The toughest part of moving to a new city, is understanding this city, and picking the neighborhood "
            "that we will call home, be it for the next week, month or years to come.")
st.markdown("### Barcelona")
st.markdown("To this end, we have created this website, that will help you to understand the city of Barcelona, "
            "through many different socio-economic lenses, and render your choice of neighborhood as easy and logical "
            "as possible. In the different pages, navigable through the navigation menu on the left, you will see "
            "different charts, highlighting different aspects of life in Barcelona, where you will compare your "
            "favourite districts, and figure out the best match for yourself, or your family.")
st.markdown("#### Happy House Hunting")
st.markdown(footer, unsafe_allow_html=True)
