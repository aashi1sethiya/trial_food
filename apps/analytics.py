
from util import plots
import streamlit as st  # pip install streamlit
import pandas as pd

def main():
    df_log = pd.read_csv('./output/staff_food_log.csv')
    df_user = df_log.query("Username == @st.session_state.username")
    total_CO2 = df_user.CO2e.sum()
    col1, col2 = st.columns(2)
    with col1:
        fig_user_CO2e = plots.plot_user_CO2e(df_user)
        col1.plotly_chart(fig_user_CO2e, use_container_width=True)
    st.dataframe(df_user)