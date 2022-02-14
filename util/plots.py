import plotly.express as px  # pip install plotly-express
import plotly.graph_objects as go # other graph objects

# Plotly colors: https://plotly.com/python/builtin-colorscales/

def donut_chart_carbon(labels, values):
    """Donut chart for CO2 emissions of different ingredients.

    Args:
        labels (array): Ingrdients
        values (array): CO2 emissions (kg CO2eq) based on whole recipe amounts. 

    Returns:
        fig: plotly object. 
    """
    fig = go.Figure(data=[go.Pie(labels=labels,
                                 values=values,
                                 direction='clockwise',
                                 hole=.5,
                                 marker_colors=px.colors.sequential.RdBu,
                                 sort=True)])

    annotations=[]
    annotations.append(dict(xref='paper', yref='paper',
    x=0.5, y=0.5,
    xanchor= 'center',
    yanchor='middle',
    text= '<b>CO2e OF<br>INGREDIENTS (kg)</b>',
    font=dict(family="Arial", size=12),
    showarrow=False,
    ))

    fig.update_traces(
    textposition='inside',
    textinfo='label+percent',
    showlegend=True,
    )

    fig.update_layout(
        annotations=annotations
        )
    return fig

def gauge_chart_carbon(value_per_100g, value_per_recipe, nServings):
    """ Gauge chart for carbon label of dish per 100g. 

    Args:
        value_per_100g (float): Total CO2 emissions per 100g of recipe.
        value_per_recipe (float): Total CO2 emissions for whole recipe. 
        nServings (str): Number of servings.

    Returns:
        fig : plotly object. 
    """
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = value_per_100g,
        title = {'text': f"CO2e total: {value_per_recipe:.0f} kg <br> Servings: {nServings}", 'font': {'size': 18}},
        mode = "gauge+number", # gauge+number+delta
        #delta = {'reference': 1},
        name = 'kg CO2e / 100g',
        gauge = {'axis': {'range': [None, 3]},
                'steps' : [
                    {'range': [0, 0.4], 'color': "lightgreen"},
                    {'range': [0.4, 1.4], 'color': "lightsalmon"},
                    {'range': [1.4, 3], 'color': "crimson"},
                    ],
                'bar': {'color': "lightgray"},
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 2.9}}))

    annotations=[]
    annotations.append(dict(xref='paper', yref='paper',
    x=0.5, y=0.0,
    xanchor= 'center',
    yanchor='bottom',
    text= '<b>Kg CO2e / 100g </b>',
    font=dict(family="Arial", size=12),
    showarrow=False,
    ))

    fig.update_layout(
        annotations=annotations
        )

    return fig

def donut_chart_nutrition(nutrient_value, rdi_value, nutrient_label, unit, **kwargs):
    """Donut chart for CO2 emissions of different ingredients.

    Args:
        nutrient_value (float): Nutrient value in dish per 100g. 
        rdi_value (float): RDI value for this nutrient.
        nutrient_label (str): Name of nutrient.
        unit (str): unit of nutrient.
        **kwargs: other arguments for the go.Pie function, like marker_colors.

    Returns:
        fig: plotly object. 
    """
    values = [nutrient_value, rdi_value-nutrient_value]
    labels = [nutrient_label, nutrient_label+' left']
    fig = go.Figure(data=[go.Pie(labels=labels,
                                 values=values,
                                 direction='clockwise',
                                 hole=.75,
                                 sort=False,
                                 **kwargs)])

    annotations=[]
    annotations.append(dict(xref='paper', yref='paper',
    x=0.5, y=0.5,
    xanchor= 'center',
    yanchor='middle',
    text= f'<b> {nutrient_value:.1f} {unit} <br> {nutrient_label} per 100g </b>',
    font=dict(family="Arial", size=24),
    showarrow=False,
    ))

    fig.update_traces(
    textposition='inside',
    textinfo='percent',
    showlegend=False,
    )

    fig.update_layout(
        annotations=annotations
        )
    return fig