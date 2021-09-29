from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

from dashapp import cache, DM, MD

page_name = 'diachronic_page'

diachronic_card = dbc.Card([
    dbc.Row([
        dbc.Col([
            html.H2('Diachronic Overview'),
        ]),
    ], className='title-row'),
    dbc.Row([
        dbc.Col([
            # S
            # elects:
            # Main or average
            # Journals
            # Language
        ]),
        dbc.Col([
            # Graph
        ]),
    ]),
], body=True, className='content-card')


diachronic_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            diachronic_card
        ]),
    ]),
], id='diachronic-layout', className='std-content-div', fluid=True)

