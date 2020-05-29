# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """

            ## Type The Name Of A Dish!
              After a user enters a recipe name this feature queries a database of recipes to find all recipes with titles
              that include words in the entered name. The ingredients are then compared across these matching recipes.
              Only those ingredients that appear in excess of 25% of recipes are returned. For each ingredient the most
              common quantity and unit associated with the ingredient are also returned.
            """
        ),
    ],
    md=4,
)

column2 = dbc.Col(
    [

    ]
)

layout = dbc.Row([column1, column2])
