# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output

# Imports from this application
from app import app, server
from pages import index, UrlGetter, text_photo_parser, ingred_parser

# Navbar docs: https://dash-bootstrap-components.opensource.faculty.ai/l/components/navbar
navbar = dbc.NavbarSimple(
    brand='MyDish',
    brand_href='/',
    children=[
        dbc.NavItem(dcc.Link('Paste A Url!',
                             href='/UrlGetter', className='nav-link')),
        dbc.NavItem(dcc.Link('Feed Us A Photo!',
                             href='/text_photo_parser', className='nav-link')),
        dbc.NavItem(dcc.Link('Name A Dish!',
                             href='/ingred_parser', className='nav-link')),
    ],
    sticky='top',
    color='light',
    light=True,
    dark=False
)


theme = {
    'dark': False,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E'
}

app.layout = html.Div(id='dark-theme-provider-demo', children=[
    html.Br(),
    daq.ToggleSwitch(
        id='daq-light-dark-theme',
        label=['Light', 'Dark'],
        style={'width': '250px', 'margin': 'auto'},
        value=False
    ),
    html.Div(
        id='dark-theme-component-demo',
        children=[
            daq.DarkThemeProvider(theme=theme, children=daq.Knob(value=6))
        ],
        style={'display': 'block', 'margin-left': 'calc(50% - 110px)'}
    )
])


@app.callback(
    Output('dark-theme-component-demo', 'children'),
    [Input('daq-light-dark-theme', 'value')]
)
def turn_dark(dark_theme):
    if(dark_theme):
        theme.update(
            dark=True
        )
    else:
        theme.update(
            dark=False
        )
    return daq.DarkThemeProvider(theme=theme, children=daq.Knob(value=6))


@app.callback(
    Output('dark-theme-provider-demo', 'style'),
    [Input('daq-light-dark-theme', 'value')]
)
def change_bg(dark_theme):
    if(dark_theme):
        return {'background-color': '#303030', 'color': 'white'}
    else:
        return {'background-color': 'white', 'color': 'black'}


# Footer docs:
# dbc.Container, dbc.Row, dbc.Col: https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
# html.P: https://dash.plot.ly/dash-html-components
# fa (font awesome) : https://fontawesome.com/icons/github-square?style=brands
# mr (margin right) : https://getbootstrap.com/docs/4.3/utilities/spacing/
# className='lead' : https://getbootstrap.com/docs/4.3/content/typography/#lead
footer = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.P(
                [

                    html.Span('MyDish', className='mr-2'),
                    html.A(html.I(className='fab fa-github-square mr-1'),
                           href='https://github.com/Lambda-School-Labs/MyDish-DS/tree/master'),

                    html.Span('Yoni Pineda', className='mr-2'),
                    html.A(html.I(className='fas fa-envelope-square mr-1'),
                           href='mailto:yonipined@icloud.com'),
                    html.A(html.I(className='fab fa-github-square mr-1'),
                           href='https://github.com/Yonipineda'),
                    html.A(html.I(className='fab fa-linkedin mr-1'),
                           href='https://www.linkedin.com/in/yoni-pineda-8a43841a3/'),

                    html.Span('Robin Srimal', className='mr-2'),
                    html.A(html.I(className='fas fa-envelope-square mr-1'),
                           href='mailto:robin.srimal@gmail.com'),
                    html.A(html.I(className='fab fa-github-square mr-1'),
                           href='https://github.com/RobinSrimal'),
                    html.A(html.I(className='fab fa-linkedin mr-1'),
                           href='https://www.linkedin.com/in/robin-srimal-a41633135/'),

                    html.Span('Neal Whitlock', className='mr-2'),
                    html.A(html.I(className='fas fa-envelope-square mr-1'),
                           href='mailto:nealwhitlock@gmail.com'),
                    html.A(html.I(className='fab fa-github-square mr-1'),
                           href='https://github.com/NealWhitlock'),
                    html.A(html.I(className='fab fa-linkedin mr-1'),
                           href='https://www.linkedin.com/in/neal-whitlock-4106951a6/'),


                ],
                className='lead'
            )
        )
    )
)

# Layout docs:
# html.Div: https://dash.plot.ly/getting-started
# dcc.Location: https://dash.plot.ly/dash-core-components/location
# dbc.Container: https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    dbc.Container(id='page-content', className='mt-4'),
    html.Hr(),
    footer
])


# URL Routing for Multi-Page Apps: https://dash.plot.ly/urls
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index.layout
    elif pathname == '/UrlGetter':
        return UrlGetter.layout
    elif pathname == '/text_photo_parser':
        return text_photo_parser.layout
    elif pathname == '/ingred_parser':
        return ingred_parser.layout
    else:
        return dcc.Markdown('## Page not found')


# Run app server: https://dash.plot.ly/getting-started
if __name__ == '__main__':
    app.run_server(debug=True)
