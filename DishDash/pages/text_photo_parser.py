# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """

            ## Feed us a photo of a recipe, handwritten or screenshot!
            > Upload a picture of the ingredients and/or the instructions of a recipe you like (from a cookbook or even handwritten notes) and the content will be saved automatically to your cookbook. This works for several languages. Especially well for Spanish, French and English.\n
            """
        ),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select a File')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'text-align': 'center',
                'margin': '10px'
            }
        ),
        dcc.Markdown(
            """
        [Try This Sample Photo!](/assets/ingredients2.png)
        """
        ),
        html.Hr(),
        html.Div(id='output-data-upload'),

        dcc.Link(dbc.Button('Go To Name A Dish!',
                            color='primary'), href='/ingred_parser')
    ],
    style={
        'text-align': 'center'
    },
    md=12,
)

column2 = dbc.Col(
    [

    ]
)

layout = dbc.Row([column1, column2])
