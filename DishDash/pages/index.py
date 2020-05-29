# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Imports from this application
from app import app

# HEADER -> Add to Layout to include in the app
header = dbc.Col(
    [
        dcc.Markdown(
            """
        ![header](/assets/dance_hoorah.gif)
        """
        ),
    ],
    md=15,
    style={
        'textAlign': 'center',
    }
)


# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """

            ## Dishify MyDish

            With Mydish, save and create recipes with the magic of Data Science. Have a handwritten recipe in a Notebook?
            No problem, just take a photo and feed it to our app. Found a website with an interesting recipe? Copy and paste the url into our app and the
            recipe will be saved instantly. Want it to be saved in Spanish, French, or English? That can be done. MyDish will
            save time and reliably save your recipes.

            """
        ),
        dcc.Link(dbc.Button('Make A Recipe!',
                            color='primary'), href='/UrlGetter')
    ],
    md=4,
)


column2 = dbc.Col(
    [
        dcc.Markdown(
            """
        ![header](/assets/food_anime.gif)
        """

        ),
    ],
    md=50,
    style={
        'textAlign': 'center',
    }
)

# dbc.Row([header]) <- Add to layout for a header.
layout = dbc.Row([column1, column2]), dbc.Row([header])
