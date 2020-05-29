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

            ## Paste a Url of a recipe site!
            First, Copy and paste the url of a recipe you would like to add to your cookbook in the app.
            Then the ingredients and instruction will be added automatically with the press of a button.
            """
        ),
    ],
    md=4,
)

column2 = dbc.Col(
    [
        dcc.Markdown('## Enter A URL Below:',
                     className='mb-5', style={'marginTop': '1em'}),
        dcc.Textarea(
            id='input-box',
            placeholder='Url please!',
            value='Url please!',
            cols=5,
            rows=2,
            maxLength=280,
            style={'width': '100%', 'marginBottom': '1.2em'}
        ),
        html.Button('Make My Recipe!', id='button', n_clicks=1, style={
            'width': '10em', 'padding': '5px', 'marginBottom': '4em'}),
        dcc.Markdown('### Recipe:',
                     style={'marginBottom': '2em'}),
        html.Div(id='prediction-label', className='lead',
                 style={'marginBottom': '3em', 'fontWeight': 'bold', 'fontSize': '20px'}),
        html.Div(id='prediction-table', style={'marginBottom': '5em'}),


    ],
    md=5,
)

column3 = dbc.Col(
    [
        dcc.Dropdown(
            options=[
                {'label': 'name', 'value': 'name'},
                {'label': 'ingredient', 'value': 'ingredient'},
                {'label': 'unit', 'value': 'unit'},
                {'label': 'instructions', 'value': 'instruction'}
            ],
            multi=True,
            value="name"


        ),



    ]
)

column4 = dbc.Col(
    [
        dcc.Dropdown(
            options=[
                {'label': 'name', 'value': 'name'},
                {'label': 'ingredient', 'value': 'ingredient'},
                {'label': 'unit', 'value': 'unit'},
                {'label': 'instructions', 'value': 'instruction'}
            ],
            multi=True,
            value="ingredient"


        ),


    ]
)

column5 = dbc.Col(
    [
        dcc.Dropdown(
            options=[
                {'label': 'name', 'value': 'name'},
                {'label': 'ingredient', 'value': 'ingredient'},
                {'label': 'unit', 'value': 'unit'},
                {'label': 'instructions', 'value': 'instruction'}
            ],
            multi=True,
            value="unit"


        ),



    ]
)


column6 = dbc.Col(
    [
        dcc.Dropdown(
            options=[
                {'label': 'name', 'value': 'name'},
                {'label': 'ingredient', 'value': 'ingredient'},
                {'label': 'unit', 'value': 'unit'},
                {'label': 'instructions', 'value': 'instructions'}
            ],
            multi=True,
            value="instructions"


        ),





    ]
)

column7 = dbc.Col(
    [
        dcc.Link(dbc.Button('Go To Feed Us A Photo!',
                            color='primary'), href='/text_photo_parser')
    ]
)

layout = dbc.Row([column1, column2]), dbc.Row(
    [column3, column4]), dbc.Row([column5, column6]), dbc.Row(column7)
