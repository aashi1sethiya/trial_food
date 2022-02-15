# @Website:  https://ikitcheng.github.io
# @YouTube:  https://youtube.com/c/chinamatt
# @Project:  Food carbon and nutrition Dashboard w/ Streamlit

# TODO:
# Add relative daily CO2e food budget and how much of 100g of the dish uses up.
# Add nutrition data with some kind of rounded chart showing actual values per 100g, and also as a % of the RDI value.

from ctypes import alignment
import pandas as pd  # pip install pandas openpyxl
import numpy as np  # math operations
import json  # json file
import streamlit as st  # pip install streamlit
from streamlit_lottie import st_lottie  # pip install streamlit-lottie
from util import plots, lottie  # utility functions for graphics

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Our Food Impact", page_icon=":egg:", layout="wide")

# ---- READ JSON data ----
@st.cache
def get_data_from_json(path_to_json):
    data = load_json(path_to_json)
    df = pd.json_normalize(data)
    return df


def load_json(path_to_file):
    with open(path_to_file, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data


def sidebar(df):
    """Sidebar for data selection.

    Args:
        df (pd.DataFrame): Dishes dataframe.

    Returns:
        df_selection (pd.Dataframe): Dishes selection dataframe.
    """
    with open('./styles/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    st.sidebar.header("Please Filter Here:")
    menu_item_type = st.sidebar.multiselect(
        "Select the dish type:",
        options=df["MenuItemType"].unique(),
        default=df["MenuItemType"].unique(),  # display all Location names
    )

    menu_item_name = st.sidebar.selectbox(
        "Select the dish name:",
        options=[""]
        + list(
            df.query("MenuItemType == @menu_item_type")["MenuItemName"].unique()
        ),  # add default option as empty string
        index=0,
    )

    df_selection = df.query("MenuItemName == @menu_item_name")

    # st.dataframe(df_selection) # test that the df_selection reacts to user filters
    return df_selection


def get_carbon_footprint_for_dish_ingredients(df_selection):
    """Get the carbon footprint for each ingredient in the recipe (for plot in pie chart).

    Args:
        df_selection (pd.DataFrame): Selected dish with all columns in dataframe.

    Returns:
        (tuple): A tuple of values corresponding to the ingrdient and its carbon footprint (based on recipe amount).
    """
    labels = list(
        zip(
            df_selection["RawIngredientsEngSimple"].values[0],
            df_selection["RawIngredientsChinese"].values[0],
        )
    )
    values = df_selection["CarbonFootprint"].values[0]
    descending_ix = np.array(values).argsort()[
        ::-1
    ]  # sort values from largest to smallest
    values = np.array(values)[descending_ix]
    labels = np.array(labels)[descending_ix]
    return labels, values


def get_carbon_label_for_dish_per_100g(df_selection):
    """Get the carbon label for selected dish per 100g.

    Args:
        df_selection (pd.DataFrame): Selected dish with all columns in dataframe.

    Returns:
        (tuple): A tuple of values corresponding to kg CO2e / 100g of dish, kg CO2e / recipe, number of servings.
    """
    value_per_100g = df_selection["CarbonLabelMenuItemPer100g"].values[0]
    value_per_recipe = df_selection["CarbonLabelMenuItem"].values[0]
    nServings = df_selection["AmountServings"].values[0]
    return value_per_100g, value_per_recipe, nServings


def get_nutrition_label_for_dish_per_100g(df_selection):
    """Get the nutrition label for selected dish per 100g.

    Args:
        df_selection (pd.DataFrame): Selected dish with all columns in dataframe.

    Returns:
        (tuple): A tuple of values corresponding to calories, protein, carb, fat / 100g of dish.
    """
    calories = df_selection["NutritionLabelMenuItemPer100g.Calories"].values[0]
    carb = df_selection["NutritionLabelMenuItemPer100g.Carbohydrate"].values[0]
    fat = df_selection["NutritionLabelMenuItemPer100g.Fat"].values[0]
    protein = df_selection["NutritionLabelMenuItemPer100g.Protein"].values[0]

    return calories, carb, fat, protein


def main_page(df_selection):
    """Main page displaying information of selected dish

    Args:
        df_dish (pd.DataFrame): Dish dataframe.

    Returns:
        df_selection (pd.Dataframe): Dishes selection dataframe.
    """

    # Title
    # ---------------------------------------------------------------------------- #
    col1, col2 = st.columns((1, 4))
    with col1:
        lottie_welcome = lottie.load_lottiefile(
            "./lottiefiles/walking-avocado.json"
        )  # replace link to local lottie file
        st_lottie(
            lottie_welcome,
            speed=1,
            reverse=False,
            loop=True,
            quality="low",
            height=150,
            width=200,
            key="welcome",
        )
    with col2:
        st.write("\n")
        st.write("\n")
        st.markdown(
            "<h1 style='text-align: center; color: #544B35; font-size: 3em'> Our Food | Our Climate | Our Health </h1>",
            unsafe_allow_html=True,
        )
    st.markdown("---")

    if len(df_selection) == 0:
        pass

    else:
        dish_name = df_selection["MenuItemName"].values[0]
        st.title(f":egg: {dish_name} Impact on ...")
        st.markdown("##")
        st.markdown("##")

        # ENVIRONMENT
        # ---------------------------------------------------------------------------- #
        st.subheader(f"... the Climate (GHG emissions) :factory: :deciduous_tree: ")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("Ingredients: Carbon pie (whole recipe)\n")
            labels, values = get_carbon_footprint_for_dish_ingredients(df_selection)
            fig_ingredients_carbon = plots.donut_chart_carbon(labels, values)
            col1.plotly_chart(fig_ingredients_carbon, use_container_width=True)

        with col2:
            st.markdown("Carbon Footprint per 100g (kg CO2e / 100g):\n")
            (
                value_per_100g,
                value_per_recipe,
                nServings,
            ) = get_carbon_label_for_dish_per_100g(df_selection)
            fig_carbon_label_dish = plots.gauge_chart_carbon(
                value_per_100g, value_per_recipe, nServings
            )
            col2.plotly_chart(fig_carbon_label_dish, use_container_width=True)

        # NUTRITION
        # ---------------------------------------------------------------------------- #
        st.subheader(f"... your Health (Nutrition) :muscle: :heart:")

        calories, carb, fat, protein = get_nutrition_label_for_dish_per_100g(
            df_selection
        )
        df_rdi = pd.read_csv("./data/nutrition_rdi.csv")

        col1, col2 = st.columns(2)
        with col1:
            col1.metric("Energy", f"{calories:.1f} kcal", "")
            fig_calories_per_100g = plots.donut_chart_nutrition(
                nutrient_value=calories,
                rdi_value=df_rdi["Energ_Kcal"].values[0],
                nutrient_label="Energy",
                unit="kcal",
                marker_colors=["lightsalmon", "lightgray"],
            )
            col1.plotly_chart(fig_calories_per_100g, use_container_width=True)

        with col2:
            col2.metric("Carbs", f"{carb:.1f} g", "")
            fig_carb_per_100g = plots.donut_chart_nutrition(
                nutrient_value=carb,
                rdi_value=df_rdi["Carbohydrt_(g)"].values[0],
                nutrient_label="Carbs",
                unit="g",
                marker_colors=["lightblue", "lightgray"],
            )
            col2.plotly_chart(fig_carb_per_100g, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            col1.metric("Fat", f"{fat:.1f} g", "")
            fig_fat_per_100g = plots.donut_chart_nutrition(
                nutrient_value=fat,
                rdi_value=df_rdi["Lipid_Tot_(g)"].values[0],
                nutrient_label="Fat",
                unit="g",
                marker_colors=["crimson", "lightgray"],
            )
            col1.plotly_chart(fig_fat_per_100g, use_container_width=True)

        with col2:
            col2.metric("Protein", f"{protein:.1f} g", "")
            fig_protein_per_100g = plots.donut_chart_nutrition(
                nutrient_value=protein,
                rdi_value=df_rdi["Protein_(g)"].values[0],
                nutrient_label="Protein",
                unit="g",
                marker_colors=["green", "lightgray"],
            )
            col2.plotly_chart(fig_protein_per_100g, use_container_width=True)

        # ---- HIDE STREAMLIT STYLE ----
        hide_st_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    header {visibility: hidden;}
                    </style>
                    """
        st.markdown(hide_st_style, unsafe_allow_html=True)


def main():

    df = get_data_from_json("data/menu_edr_dishes_only.json")
    # df_menu = get_data_from_json('data/menu_edr.json')[
    #     ['menu_type',
    #     'number_of_dishes',
    #     'number_of_unique_ingredients',
    #     'ingredients_unique_chi'
    #     ]]

    # ---- SIDEBAR ----
    df_selection = sidebar(df)

    # # ---- MAINPAGE ----
    main_page(df_selection)


if __name__ == "__main__":
    main()
