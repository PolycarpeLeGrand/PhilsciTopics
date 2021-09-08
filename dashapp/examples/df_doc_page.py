from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

# Import app and cache only if needed
# If using DataManagers, import them from dashapp on this line as well
# from dashapp import app, cache

from dashapp import DM

page_name = 'df_doc_page'

# Example jumbotron
# The text layout can easily be set with dbc rows and cols
# Typically uses H2 with classname jumbotron-title for title
df_doc_jumbo = dbc.Jumbotron([
    dbc.Row([
        dbc.Col([
            dcc.Markdown(DM.doc_md),
        ]),
    ])
], className='content-jumbotron')


df_doc_page_layout = dbc.Container([
    # Jumbotron Row, delete if not needed
    dbc.Row([
       dbc.Col([
           df_doc_jumbo
       ], lg=8),
    ], justify='center'),
], className='std-content-div', fluid=True)

