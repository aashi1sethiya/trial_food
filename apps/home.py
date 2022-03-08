from ctypes import alignment
from turtle import onclick
import pandas as pd  # pip install pandas openpyxl
import numpy as np  # math operations
import json  # json file
from datetime import datetime
from time import sleep
import streamlit as st  # pip install streamlit
from streamlit_lottie import st_lottie  # pip install streamlit-lottie
from util import plots, lottie  # utility functions for graphics


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

class MealDesign:
    """A meal design class to select different dishes and set amounts.
    """
    def __init__(self,username):
        """Create a new instance of "authenticate".
        Parameters
        ----------
        username: str
            The name of the user designing the meal.
        df : pd.DataFrame
            Dishes dataframe.
        """
        self.username = username
        self.df = get_data_from_json("data/menu_edr_dishes_only.json")

    def select_dishes(self, form_name, location='main'):
        """ Select your dishes.
        Parameters
        ----------
        form_name: str
            The rendered name of the login form.
        location: str, optional
            The location of the login form i.e. main or sidebar. Defaults to main.
        Returns
        -------
        str
            Name of authenticated user.
        boolean
            The status of authentication, None: no credentials entered, False: incorrect credentials, True: correct credentials.
        """
        self.location = location
        self.form_name = form_name

        if self.location not in ['main','sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")

        if 'df_selection' not in st.session_state:
            st.session_state['df_selection'] = []
        if 'multi_dish_select' not in st.session_state:
            st.session_state['multi_dish_select'] = True
        if 'new_meal' not in st.session_state:
            st.session_state['new_meal'] = None

        if self.location == 'main':
            meal_placeholder = st.empty()
            meal_form = meal_placeholder.container()
        elif self.location == 'sidebar':
            with open('./styles/style.css') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            meal_placeholder = st.sidebar.empty()
            meal_form = meal_placeholder.container()

        meal_form.subheader(self.form_name)
        menu_item_type = meal_form.multiselect(
                "Select the dish types:",
                options=self.df["MenuItemType"].unique(),
                default=None,  # display no selections
                key='menu_item_type_key'
            )

        menu_item_name = meal_form.multiselect(
            "Select the dish names:",
            options= self.df.query("MenuItemType == @menu_item_type")["MenuItemName"].unique(),
            default = None,
            key='menu_item_name_key'
        ) 

        # Choose custom amount (g) for each dish
        custom_amount_in_grams = []
        for item in menu_item_name:
            amount_in_grams_per_serving = int(np.nansum(np.array(np.nansum(self.df.query("MenuItemName == @item")['AmountInGrams'])))/1000) # each recipe serves 1000 people
            amount = meal_form.slider(f'{item} (grams)', 0, 250, amount_in_grams_per_serving) # Default amount is serving size
            custom_amount_in_grams.append(amount)
        
        df_selection = self.df.query("MenuItemName == @menu_item_name").copy()
        df_selection['CustomAmountInGrams'] = custom_amount_in_grams

        if meal_form.button('Submit'):
            st.session_state['df_selection'] = df_selection
            st.session_state['custom_amount_in_grams'] = custom_amount_in_grams
            st.session_state['meal_placeholder'] = meal_placeholder
            st.session_state['save'] = False
        
        #print('before if empty: ', len(st.session_state['df_selection']),st.session_state['new_meal'], st.session_state['select_menu_item_type'])
        
        if len(st.session_state['df_selection']) > 0:
            # Save button
            if st.session_state['multi_dish_select']:
                st.session_state['save'] = st.sidebar.button("Save")
            if st.button('New meal'):
                # Clear the multiselect options
                del st.session_state.menu_item_type_key
                del st.session_state.menu_item_name_key
                st.session_state['new_meal'] = True
                st.session_state['df_selection'] = []
                st.session_state['multi_dish_select'] = True
                #st.session_state['meal_placeholder'].empty()
                st.experimental_rerun()

        #print('after if empty: ', len(st.session_state['df_selection']),st.session_state['new_meal'], st.session_state['select_menu_item_type'])

        return st.session_state['df_selection']

        
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
        "Select the dish types:",
        options=df["MenuItemType"].unique(),
        default=None,  # display all Location names
        key='select_menu_item_type'
    )

    st.session_state['multi_dish_select'] = st.sidebar.checkbox(
        "Multi-select", value=True
        )

    if st.session_state['multi_dish_select']:
        menu_item_name = st.sidebar.multiselect(
            "Select the dish names:",
            options= df.query("MenuItemType == @menu_item_type")["MenuItemName"].unique(),
            default = None,
            key='select_menu_item_dish'
        )

        # Choose custom amount (g) for each dish
        custom_amount_in_grams = []
        for item in menu_item_name:
            amount_in_grams_per_serving = int(np.array(np.nansum(df.query("MenuItemName == @item")['AmountInGrams'])).sum()/1000) # each recipe serves 1000 people
            amount = st.sidebar.slider(f'{item} (grams)', 0, 250, amount_in_grams_per_serving) # Default amount is serving size
            custom_amount_in_grams.append(amount)
        
        df_selection = df.query("MenuItemName == @menu_item_name").copy()
        df_selection['CustomAmountInGrams'] = custom_amount_in_grams
        st.session_state['df_selection'] = df_selection

    else: # single dish
        menu_item_name = st.sidebar.selectbox(
            "Select the dish name:",
            options=[""]
            + list(
                df.query("MenuItemType == @menu_item_type")["MenuItemName"].unique()
            ),  # add default option as empty string
            index=0,
        )
        
        df_selection = df.query("MenuItemName == @menu_item_name").copy()
        st.session_state['df_selection'] = df_selection

    #st.dataframe(df_selection) # test that the df_selection reacts to user filters

    # Save button
    if len(df_selection) > 0 and st.session_state['multi_dish_select']:
        st.session_state['ID'] = st.sidebar.text_input('Your employee ID number', '')
        # st.sidebar.markdown(f"<a style='color:#DAF2DA'> Your employee ID number is {st.session_state['ID']} </a>", unsafe_allow_html=True)
        st.session_state['save'] = st.sidebar.button(
            "Save"
            )
        if st.session_state['save']:
            save_data()
            st.sidebar.markdown("<a style='color:#DAF2DA'> Results saved. </a>", unsafe_allow_html=True)

    return df_selection



def navbar():
    """
    Navigation bar for the app. 

    Reference:
    1) Anchor tags: https://www.digitalocean.com/community/tutorials/html-target-attribute-anchor-tags
    """
    st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

    st.markdown("""
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
    """, unsafe_allow_html=True)

def title():
    # ---------------------------------------------------------------------------- #
    # Title
    # ---------------------------------------------------------------------------- #
    col1, col2, col3 = st.columns((1, 3, 1))
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


def get_carbon_label_for_dishes_per_custom_amount(df_selection):
    """Get the carbon label for selected dishes per 1 serving (default slider value),
     or per custom amounts in grams. 

    Args:
        df_selection (pd.DataFrame): Selected dish with all columns in dataframe.

    Returns:
        (tuple): A tuple of values corresponding to kg CO2e / 100g of dish, kg CO2e / recipe, number of servings.
    """
    value_per_custom_amount = (df_selection["CarbonLabelMenuItemPer100g"].values / 100 * df_selection["CustomAmountInGrams"].values).sum()
    return value_per_custom_amount

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

def get_nutrition_label_for_dishes_per_custom_amount(df_selection):
    """Get the nutrition label for selected dishes per 1 serving (default slider value),
     or per custom amounts in grams. 

    Args:
        df_selection (pd.DataFrame): Selected dish with all columns in dataframe.

    Returns:
        (tuple): A tuple of values corresponding to calories, protein, carb, fat / serving of each dish.
    """
    calories = (df_selection["NutritionLabelMenuItemPer100g.Calories"].values / 100 * df_selection["CustomAmountInGrams"].values).sum()
    carb = (df_selection["NutritionLabelMenuItemPer100g.Carbohydrate"].values / 100 * df_selection["CustomAmountInGrams"].values).sum()
    fat = (df_selection["NutritionLabelMenuItemPer100g.Fat"].values / 100 * df_selection["CustomAmountInGrams"].values).sum()
    protein = (df_selection["NutritionLabelMenuItemPer100g.Protein"] / 100 * df_selection["CustomAmountInGrams"].values).sum()

    return calories, carb, fat, protein

def meal_analysis(df_selection):
    """Displaying information of selected dish

    Args:
        df_dish (pd.DataFrame): Dish dataframe.

    Returns:
        df_selection (pd.Dataframe): Dishes selection dataframe.
    """

    # ---------------------------------------------------------------------------- #
    # Main page content
    # ---------------------------------------------------------------------------- #
    if len(df_selection) == 0:
        pass
    
    elif len(df_selection) == 1 and not st.session_state['multi_dish_select']:
        dish_name = df_selection["MenuItemName"].values[0]
        col1, col2 = st.columns([1,15])
        with col1:
            col1.title(f":egg:")
        with col2:
            col2.markdown(f"<h2 style='text-align: left; color: black; font-family:quando'> {dish_name} Impact on ... </h2>", unsafe_allow_html=True)

        #st.title(f":egg: {dish_name} Impact on ...")
        st.markdown("##")
        st.markdown("##")

        # ---------------------------------------------------------------------------- #
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

        # ---------------------------------------------------------------------------- #
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
                rdi_value=df_rdi['Energ_Kcal'].values[0],
                nutrient_label="Energy",
                per="100g",
                marker_colors=["lightsalmon", "lightgray"],
            )
            col1.plotly_chart(fig_calories_per_100g, use_container_width=True)

        with col2:
            col2.metric("Carbs", f"{carb:.1f} g", "")
            fig_carb_per_100g = plots.donut_chart_nutrition(
                nutrient_value=carb,
                rdi_value=df_rdi["Carbohydrt_(g)"].values[0],
                nutrient_label="Carbs",
                per="100g",
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
                per="100g",
                marker_colors=["crimson", "lightgray"],
            )
            col1.plotly_chart(fig_fat_per_100g, use_container_width=True)

        with col2:
            col2.metric("Protein", f"{protein:.1f} g", "")
            fig_protein_per_100g = plots.donut_chart_nutrition(
                nutrient_value=protein,
                rdi_value=df_rdi["Protein_(g)"].values[0],
                nutrient_label="Protein",
                per="100g",
                marker_colors=["green", "lightgray"],
            )
            col2.plotly_chart(fig_protein_per_100g, use_container_width=True)

    else: # multi-dish
        dish_names = df_selection["MenuItemName"].values
        col1, col2 = st.columns([1,15])
        with col1:
            col1.title(f":egg:")
        with col2:
            col2.markdown("<h1 style='text-align: left; color: black; font-size: 2em; font-family:quando'> Your Meal Impact on ... </h1>", unsafe_allow_html=True)
        st.markdown("##")
        st.markdown("##")

        # ---------------------------------------------------------------------------- #
        # ENVIRONMENT
        # ---------------------------------------------------------------------------- #
        st.subheader(f"... the Climate (GHG emissions) :factory: :deciduous_tree: ")

        st.markdown("Carbon Footprint per Serving (kg CO2e / serving):\n")
        col1, _ = st.columns(2)
        livelca_CO2_budget = 2.72 # (kg) based on LiveLCA threshold 
        st.session_state['max_CO2'] = 5.
        st.session_state['daily_food_CO2_budget'] = col1.number_input('CO2e Budget (kg)', 0., st.session_state['max_CO2'], livelca_CO2_budget) # Default amount is rdi value

        _, col2, _ = st.columns([1,3,1])
        kgCO2e_per_custom_amount = get_carbon_label_for_dishes_per_custom_amount(df_selection)
        fig_carbon_label_dish = plots.gauge_chart_carbon_multidish(kgCO2e_per_custom_amount)
        with col2:
            col2.plotly_chart(fig_carbon_label_dish, use_container_width=False) # bug if True, the gauge value moves after closing and opening sidebar 

        # store value in session state
        st.session_state['kgCO2e_per_custom_amount'] = kgCO2e_per_custom_amount

        # ---------------------------------------------------------------------------- #
        # NUTRITION
        # ---------------------------------------------------------------------------- #
        st.subheader(f"... your Health (Nutrition) :muscle: :heart:")

        calories, carb, fat, protein = get_nutrition_label_for_dishes_per_custom_amount(
            df_selection
        )

        # store value in session state
        st.session_state['calories_per_custom_amount'] = calories
        st.session_state['carb_per_custom_amount'] = carb
        st.session_state['fat_per_custom_amount'] = fat
        st.session_state['protein_per_custom_amount'] = protein
        
        df_rdi = pd.read_csv("./data/nutrition_rdi.csv")

        col1, _, col3, _ = st.columns(4)
        calories_budget = col1.number_input('Calories Budget (kcal)', 0, 3000, int(df_rdi['Energ_Kcal'].values[0])) # Default amount is rdi value
        carbs_budget = col3.number_input('Carbs Budget (g)', 0, 300, int(df_rdi['Carbohydrt_(g)'].values[0])) # Default amount is rdi value

        col1, col2 = st.columns(2)
        with col1:
            col1.metric("Energy", f"{calories:.1f} kcal", "")
            fig_calories_per_serving = plots.donut_chart_nutrition(
                nutrient_value=calories,
                rdi_value=calories_budget,
                nutrient_label="Energy",
                per="serving",
                marker_colors=["lightsalmon", "lightgray"],
            )
            col1.plotly_chart(fig_calories_per_serving, use_container_width=True)

        with col2:
            col2.metric("Carbs", f"{carb:.1f} g", "")
            fig_carb_per_serving = plots.donut_chart_nutrition(
                nutrient_value=carb,
                rdi_value=carbs_budget,
                nutrient_label="Carbs",
                per="serving",
                marker_colors=["lightblue", "lightgray"],
            )
            col2.plotly_chart(fig_carb_per_serving, use_container_width=True)

        col1, _, col3, _ = st.columns(4)
        fat_budget = col1.number_input('Fat Budget (g)', 0, 100, int(df_rdi['Lipid_Tot_(g)'].values[0])) # Default amount is rdi value
        protein_budget = col3.number_input('Protein Budget (g)', 0, 100, int(df_rdi['Protein_(g)'].values[0])) # Default amount is rdi value

        col1, col2 = st.columns(2)
        with col1:
            col1.metric("Fat", f"{fat:.1f} g", "")
            fig_fat_per_serving = plots.donut_chart_nutrition(
                nutrient_value=fat,
                rdi_value=fat_budget,
                nutrient_label="Fat",
                per="serving",
                marker_colors=["crimson", "lightgray"],
            )
            col1.plotly_chart(fig_fat_per_serving, use_container_width=True)

        with col2:
            col2.metric("Protein", f"{protein:.1f} g", "")
            fig_protein_per_serving = plots.donut_chart_nutrition(
                nutrient_value=protein,
                rdi_value=protein_budget,
                nutrient_label="Protein",
                per="serving",
                marker_colors=["green", "lightgray"],
            )
            col2.plotly_chart(fig_protein_per_serving, use_container_width=True)


def results2df():
    results = {'Datetime':pd.to_datetime(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                'username': st.session_state['username'],
                'Dishes':';'.join(st.session_state['df_selection']['MenuItemName'].values.astype(str)),
                'Amount':';'.join(st.session_state['df_selection']['CustomAmountInGrams'].values.astype(str)),
                'CO2e': st.session_state['kgCO2e_per_custom_amount'],
                'Calories':st.session_state['calories_per_custom_amount'],
                'Carb':st.session_state['carb_per_custom_amount'],
                'Fat':st.session_state['fat_per_custom_amount'],
                'Protein':st.session_state['protein_per_custom_amount'],
            }
                
    df = pd.DataFrame(results, index=[0])

    return df
    
def save_data():
    """
    Save user results to csv file. 
    """
    df = results2df()
    df.to_csv('./output/staff_food_log.csv', mode='a', header=False, index=False)
    #st.dataframe(df)
    
def main():

    # ---- LOAD DATA ----
    df = get_data_from_json("data/menu_edr_dishes_only.json")

    # ---- SIDEBAR (SELECTION) ----
    df_selection = sidebar(df)

    # ---- NAVBAR ----
    navbar()

    # # ---- MAINPAGE ----
    meal_analysis(df_selection)