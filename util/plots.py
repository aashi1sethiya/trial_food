""" 
This module produces the plots in the app. 

Reference: 
1) Plotly colors: https://plotly.com/python/builtin-colorscales/

"""

import streamlit as st
import plotly.express as px  # pip install plotly-express
import plotly.graph_objects as go  # other graph objects


def donut_chart_carbon(labels, values):
    """Donut chart for CO2 emissions of different ingredients.

    Args:
        labels (array): Ingrdients
        values (array): CO2 emissions (kg CO2eq) based on whole recipe amounts.

    Returns:
        fig: plotly object.
    """
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                direction="clockwise",
                hole=0.5,
                marker_colors=px.colors.sequential.RdBu,
                sort=True,
            )
        ]
    )

    annotations = []
    annotations.append(
        dict(
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            xanchor="center",
            yanchor="middle",
            text="<b>CO2e OF<br> Ingredients (kg)</b>",
            font=dict(family="Arial", size=14),
            showarrow=False,
        )
    )

    fig.update_traces(
        textposition="inside",
        textinfo="label+percent",
        showlegend=True,
    )

    fig.update_layout(
        annotations=annotations,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",  # transparrent background
        plot_bgcolor="rgba(0,0,0,0)",  # transparrent background
    )
    return fig


def gauge_chart_carbon(value_per_100g, value_per_recipe, nServings):
    """Gauge chart for carbon label of dish per 100g.

    Args:
        value_per_100g (float): Total CO2 emissions per 100g of recipe.
        value_per_recipe (float): Total CO2 emissions for whole recipe.
        nServings (str): Number of servings.

    Returns:
        fig : plotly object.
    """
    daily_food_CO2_budget = 2.72  # based on LiveLCA threshold
    fig = go.Figure(
        go.Indicator(
            domain={"x": [0, 1], "y": [0, 1]},
            value=value_per_100g,
            title={
                "text": f"CO2e total: {value_per_recipe:.0f} kg <br> Servings: {nServings}",
                "font": {"size": 18},
            },
            mode="gauge+number",  # gauge+number+delta
            # delta = {'reference': 1},
            name="kg CO2e / 100g",
            gauge={
                "axis": {"range": [None, 3]},
                "steps": [
                    {"range": [0, 0.4], "color": "lightgreen"},
                    {"range": [0.4, 1.4], "color": "lightsalmon"},
                    {"range": [1.4, 3], "color": "crimson"},
                ],  # Swedish meat GHG emissions traffic light system
                "bar": {"color": "#CCCCCC"},
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 2.9,
                },
            },
        )
    )

    annotations = []
    annotations.append(
        dict(
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.0,
            xanchor="center",
            yanchor="bottom",
            text=f"<b>kg CO2e / 100g <br> You can consume {daily_food_CO2_budget/value_per_100g*100:.0f} g of this dish <br> to exhaust your daily food CO2e budget.</b>",
            font=dict(family="Arial", size=14),
            showarrow=False,
        )
    )

    fig.update_layout(
        annotations=annotations,
        margin=dict(l=20, r=20, t=25, b=20),
        paper_bgcolor="rgba(0,0,0,0)",  # transparrent background
        plot_bgcolor="rgba(0,0,0,0)",  # transparrent background
    )

    return fig


def gauge_chart_carbon_multidish(value_per_custom_amount):
    """Gauge chart for carbon label of dish per serving or custom amount.

    Args:
        value_per_serving (float): Total CO2 emissions for whole recipe.

    Returns:
        fig : plotly object.
    """
    max_CO2 = st.session_state["max_CO2"]
    daily_food_CO2_budget = st.session_state["daily_food_CO2_budget"]
    fig = go.Figure(
        go.Indicator(
            domain={"x": [0, 1], "y": [0, 1]},
            value=value_per_custom_amount,
            title={"text": f"CO2e per serving:", "font": {"size": 18}},
            mode="gauge+number",  # gauge+number+delta
            # delta = {'reference': 1},
            name="kg CO2e / serving",
            gauge={
                "axis": {"range": [None, max_CO2]},
                "steps": [
                    {"range": [0, daily_food_CO2_budget * 0.5], "color": "lightgreen"},
                    {
                        "range": [
                            daily_food_CO2_budget * 0.5,
                            daily_food_CO2_budget * 0.9,
                        ],
                        "color": "lightsalmon",
                    },
                    {
                        "range": [daily_food_CO2_budget * 0.9, max_CO2],
                        "color": "crimson",
                    },
                ],  # Daily food CO2 budget traffic light system
                "bar": {"color": "#CCCCCC"},
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": daily_food_CO2_budget,
                },
            },
        )
    )

    annotations = []
    annotations.append(
        dict(
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.1,
            xanchor="center",
            yanchor="bottom",
            text=f"<b>kg CO2e / serving <br> You have {(daily_food_CO2_budget - value_per_custom_amount):.1f} kg of food CO2e budget left today.</b>",
            font=dict(family="Arial", size=14),
            showarrow=False,
        )
    )

    fig.update_layout(
        annotations=annotations,
        margin=dict(
            autoexpand=False,
            l=40,
            r=20,
            t=50,
            b=100,
        ),
        paper_bgcolor="rgba(0,0,0,0)",  # transparrent background
        plot_bgcolor="rgba(0,0,0,0)",  # transparrent background
    )

    return fig


def donut_chart_nutrition(
    nutrient_value, rdi_value, nutrient_label, per="100g", **kwargs
):
    """Donut chart for nutrition of different ingredients.

    Args:
        nutrient_value (float): Nutrient value in dish per 100g.
        rdi_value (float): RDI value for this nutrient.
        nutrient_label (str): Name of nutrient.
        per (str, optional): Nutrient per some quantity. Defaults to 100g
        **kwargs: other arguments for the go.Pie function, like marker_colors.

    Returns:
        fig: plotly object.
    """
    values = [nutrient_value, rdi_value - nutrient_value]
    labels = [nutrient_label, nutrient_label + " left"]
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                direction="clockwise",
                hole=0.75,
                sort=False,
                **kwargs,
            )
        ]
    )

    annotations = []
    annotations.append(
        dict(
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            xanchor="center",
            yanchor="middle",
            # text= f'<b> {nutrient_value:.1f} {unit} <br> {nutrient_label} per 100g </b>', # value and label inside donut
            text=f"<b> {nutrient_label} <br> per {per} </b>",  # just label inside donut
            font=dict(family="Arial", size=14),
            showarrow=False,
        )
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        showlegend=False,
    )

    fig.update_layout(
        annotations=annotations,
        margin=dict(l=20, r=20, t=20, b=20),
        width=200,
        height=200,
        paper_bgcolor="rgba(0,0,0,0)",  # transparrent background
        plot_bgcolor="rgba(0,0,0,0)",  # transparrent background
    )
    return fig


def plot_user_CO2e(df):
    """Plot user CO2e trend.

    Args:
        df (pd.DataFrame): User's meal log dataframe.
    """
    fig = px.line(
        df, x="Datetime", y="CO2e", title="Your Food Carbon Footprint History (kgCO2e)"
    )
    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor="rgb(204, 204, 204)",
            linewidth=2,
            ticks="outside",
            tickfont=dict(
                family="Arial",
                size=12,
                color="rgb(82, 82, 82)",
            ),
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            showline=False,
            showticklabels=True,
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=40,
            r=20,
            t=100,
            b=100,
        ),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",  # transparrent background
        plot_bgcolor="rgba(0,0,0,0)",  # transparrent background
    )
    return fig


def plot_user_calories(df):
    """Plot user calories trend.

    Args:
        df (pd.DataFrame): User's meal log dataframe.
    """
    fig = px.line(
        df,
        x="Datetime",
        y="Calories",
    )
    format_plot_layout_nutrition_analytics(fig)
    return fig


def plot_user_macros(df):
    """Plot user carbs, fat, protein trend.

    Args:
        df (pd.DataFrame): User's meal log dataframe.
    """
    fig = px.line(
        df,
        x="Datetime",
        y=["Carbs","Fat","Protein"],
    )
    format_plot_layout_nutrition_analytics(fig, showlegend=True)
    return fig

def plot_user_carbs(df):
    """Plot user carbs trend.

    Args:
        df (pd.DataFrame): User's meal log dataframe.
    """
    fig = px.line(
        df,
        x="Datetime",
        y="Carbs",
    )
    format_plot_layout_nutrition_analytics(fig)
    return fig


def plot_user_fat(df):
    """Plot user fat trend.

    Args:
        df (pd.DataFrame): User's meal log dataframe.
    """
    fig = px.line(
        df,
        x="Datetime",
        y="Fat",
    )
    format_plot_layout_nutrition_analytics(fig)
    return fig


def plot_user_protein(df):
    """Plot user protein trend.

    Args:
        df (pd.DataFrame): User's meal log dataframe.
    """
    fig = px.line(
        df,
        x="Datetime",
        y="Protein",
    )
    format_plot_layout_nutrition_analytics(fig)
    return fig

def plot_user_macro_split(df, **kwargs):
    """Donut donut chart for macro split.

    Args:
        df (pd.DataFrame): User's meal log dataframe.
        **kwargs: other arguments for the go.Pie function, like marker_colors.

    Returns:
        fig: plotly object.
    """
    values = [
        df.Carbs.sum() * 4,
        df.Protein.sum() * 4,
        df.Fat.sum() * 9,
    ]  # calories from each macro
    labels = ["Carbs", "Protein", "Fat"]
    calories_total = sum(values)
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                direction="clockwise",
                hole=0.75,
                sort=False,
                **kwargs,
            )
        ],
    )

    annotations = []
    annotations.append(
        dict(
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            xanchor="center",
            yanchor="middle",
            # text= f'<b> {nutrient_value:.1f} {unit} <br> {nutrient_label} per 100g </b>', # value and label inside donut
            text=f"<b> {int(calories_total)} <br> kcal </b>",  # just label inside donut
            font=dict(family="Arial", size=14),
            showarrow=False,
        )
    )

    fig.update_traces(
        textposition="inside",
        textinfo="label+percent",
        showlegend=False,
    )

    fig.update_layout(
        annotations=annotations,
        margin=dict(l=20, r=20, t=35, b=0),
        width=300,
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",  # transparrent background
        plot_bgcolor="rgba(0,0,0,0)",  # transparrent background
    )
    return fig

def format_plot_layout_nutrition_analytics(fig, showlegend=False):
    return fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor="rgb(204, 204, 204)",
            linewidth=2,
            ticks="outside",
            tickfont=dict(
                family="Arial",
                size=12,
                color="rgb(82, 82, 82)",
            ),
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            showline=False,
            showticklabels=True,
        ),
        autosize=False,
        margin=dict(
            autoexpand=False,
            l=40,
            r=20,
            t=30,
            b=150,
        ),
        showlegend=showlegend,
        legend=dict(yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01,
                    title=""),
        paper_bgcolor="rgba(0,0,0,0)",  # transparrent background
        plot_bgcolor="rgba(0,0,0,0)",  # transparrent background
    )