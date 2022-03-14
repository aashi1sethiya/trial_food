""" 
This is the homepage of the app.
"""

import streamlit as st  # pip install streamlit
from streamlit_lottie import st_lottie  # pip install streamlit-lottie
from util import lottie  # utility functions for graphics
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
    col1, col2, col3 = st.columns((1, 3, 1))
    with col1:
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
            width=200,
            key="avo1",
        )
    with col2:
        st.write("\n")
        st.write("\n")
        st.markdown(
            "<h1 style='text-align: left; color: #544B35; font-size: 2.5em; font-family:quando'> Our Food | Our Climate | Our Health </h1>",
            unsafe_allow_html=True,
        )

    st.markdown("---")


def main():
    # ---- MAINPAGE ----
    st.markdown(
        "<h1 style='text-align: left; color: #544B35; font-size: 2.5em; font-family:quando'> Welcome </h1>",
        unsafe_allow_html=True,
    )
