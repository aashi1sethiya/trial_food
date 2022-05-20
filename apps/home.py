""" 
This is the homepage of the app.
"""

import streamlit as st  # pip install streamlit
from streamlit_lottie import st_lottie  # pip install streamlit-lottie
from util import lottie  # utility functions for graphics
from util.utils import read_html
import config


def navbar():
    """
    Navigation bar for the app.

    Reference:
    1) Anchor tags: https://www.digitalocean.com/community/tutorials/html-target-attribute-anchor-tags
    """
    st.markdown(
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #544B35;">
        <a class="navbar-brand" href="/" target="_self" style='color:#DAF2DA; font-family:quando'> Our <br> Food </a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <div class="navbar-nav">
                <a class="nav-item nav-link" href="/" style='color:#DAF2DA; font-family:quando'> Design Your Meal <span class="sr-only">(current)</span> </a>
            </div>
        </div>
        </nav>
        """,
        unsafe_allow_html=True,
    )


def title():
    # ---------------------------------------------------------------------------- #
    # Title
    # ---------------------------------------------------------------------------- #
    with st.sidebar.container():
        # _, col2, col3 = st.columns([1,2,1])
        # with col2: # attempt to center (not so nice)
        lottie_welcome = lottie.load_lottiefile(
            f"{config.PATH_TO_LOTTIE}walking-avocado.json"
        )  # replace link to local lottie file
        st_lottie(
            lottie_welcome,
            speed=1,
            reverse=False,
            loop=True,
            quality="low",
            height=150,
            width=150,
            key="avo1",
        )
    with st.container():
        st.markdown(
            "<h1 style='text-align: center; color: #544B35; font-size: 2.5em; font-family:quando'> Our Food | Our Climate | Our Health </h1>",
            unsafe_allow_html=True,
        )
        st.markdown("---")


def main():
    # ---- MAINPAGE ----
    with open(f"{config.PATH_TO_HTML_CSS}home.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    with st.container():
        contents = read_html(f"{config.PATH_TO_HTML}home.html")
        st.markdown(contents, unsafe_allow_html=True)
    with st.container():
        _, col2, _ = st.columns([1, 5, 1])
        with col2:
            st.subheader("Introduction")
            st.write(
                """
            You know that our eating habits have a direct impact on the planet? About 26% of global greenhouse gas emissions is fuelled by food production [1], contributing significantly to climate change. 
		    The good news? Simple changes to our daily lives can have huge impact - like eating a more nutrient- dense plant-based diet, using less single-use plastic and reducing edible food waste, we can cut our collective greenhouse gas emissions significantly. 
		    "The Climate Diet" app helps you plan your meal at Team Dining to create delicious, nutritious and low-carbon meals, giving you the power to manage your heatlth and protect the environment!
            [1] Poore, J., & Nemecek, T. (2018). Reducing food's environmental impacts through producers and consumers. Science, 360(6392), 987-992.
            """
            )

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("About Our Health")
            st.write(
                """
            Food is a necessity that provides the energy and nutrients we need to stay healthy. 
            Carbohydrates, proteins, and fats are the main types of macronutrients in food that provide energy to support body functions and physical activities. 
            A healthy lifestyle can be attained by having adequate rest, regular exercising and eating a nutritionally balanced diet. 
            Your food choices have a direct impact not only on your health but also on the environment.
            """
            )
        with col2:
            st.subheader("About Our Climate")
            st.write(
                """
            Due to growing population and changes in consumption patterns, the demand for food rises in tandem with the rise in energy, 
            water and cropland needed for food production. Animal-based diets generally have bigger climate impact due to its associated 
            greenhouse gas emissions as compared to plant-based diets. Reducing our climate impact through low-carbon food choices will 
            also reduce climate-related risks in the long run.
            """
            )
