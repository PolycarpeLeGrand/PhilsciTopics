from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

# Uncomment the next import if app or cache are needed
# If using DataManagers, import them from dashapp on this line as well
from dashapp import MD

page_name = 'home_page'

pres_card = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col(html.H2('Eight journals over eight decades: a computational topic-modeling approach to contemporary philosophy of science')),
        ], className='title-row'),

        dbc.Row([
            dbc.Col([
                dcc.Markdown(MD.PRESENTATION, className='content-text'),
            ], lg=6, style={'padding': '0 3rem'}),
            dbc.Col([
                dcc.Markdown(MD.HOWTO, className='content-text'),
            ], lg=6, style={'padding': '0 3rem'}),
        ], justify='around', style={'padding-bottom': '1.5rem'}),

        dbc.Row([
            dbc.Col('', lg=1),
            dbc.Col([
                dcc.Markdown('**Related Publications:**  \n' + MD.REFERENCES, className='content-text-small', style={'text-align': 'left'})
            ], lg=12, style={'padding': '0 3rem'})
        ], justify='left')
    ])
],  className='content-card')


home_layout = dbc.Container([
    # Jumbotron Row, delete if not needed
    dbc.Row([
       dbc.Col([
           pres_card
       ], lg=10),
    ], justify='center'),

], id='home-layout', className='std-content-div', fluid=True)

