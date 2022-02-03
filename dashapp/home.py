from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

# Uncomment the next import if app or cache are needed
# If using DataManagers, import them from dashapp on this line as well
from dashapp import MD

page_name = 'home_page'

pres_card = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.H2('The philosophy of science through the lens of topic-modeling '),
                dcc.Markdown(MD.SUBTITLES, className='content-text-small'),
                ], #style={'padding': '0 3rem'}
            ),
        ], className='title-row'),

        dbc.Row([
            dbc.Col([
                dcc.Markdown(MD.PRESENTATION, className='content-text'),
            ], lg=6, ), #style={'padding': '0 3rem'}),
            dbc.Col([
                dcc.Markdown(MD.HOWTO, className='content-text'),
            ], lg=6, ),#style={'padding': '0 3rem'}),
        ], justify='between', style={'padding-bottom': '1.5rem'}),

        dbc.Row([
            dbc.Col('', lg=1),
            dbc.Col([
                dcc.Markdown(MD.REFERENCES, className='content-text-small', style={'text-align': 'left'})
            ], lg=12, ), #style={'padding': '0 3rem'})
        ], justify='left')
    ])
],  className='content-card')


home_layout = dbc.Container([
    # Jumbotron Row, delete if not needed
    dbc.Row([
       dbc.Col([
           pres_card
       ], lg=12),
    ]),

], id='home-layout', className='std-content-div', fluid=True)

