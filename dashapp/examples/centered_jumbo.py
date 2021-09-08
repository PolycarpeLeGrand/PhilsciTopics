from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc

# Import app and cache only if needed
#from dashapp import app, cache


page_name = 'centered_jumbo'

# Example jumbotron
# The text layout can easily be set with dbc rows and cols
# Typically uses H2 with classname jumbotron-title for title
centered_jumbo = dbc.Jumbotron([
    dbc.Row([
        dbc.Col([
            html.H2('Phidash Home page', className='jumbotron-title')
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.P('Project text description', className='content-text')
        ]),
    ])
], className='content-jumbotron')



# Page layout holding the different components
# Name should be changed to <page_name>_layout and id to <page-name> (should be done automatically if using template)
#
# Useful notes:
#   Use <width> param to specify col width. True will expand, 'auto' fit to content, and 1-12 span a fixed number of
#       grid columns.
#   Alternatively (recommanded), use <lg> to specify width on large screens and leave auto on mobile / small.
#   Use <no_gutters=True> to remove spacing between columns
#   Use <align> to set vertical alignment of cols within a row. Can be used on Row to set for all children or on Col to
#       override the Row setting. Values: 'start', 'center', 'end'
#   Use <justify> to set the horizontal alignment within a row. Values: 'start', 'center', 'end', 'between', 'around'
centered_jumbo_layout = dbc.Container([
    # Jumbotron Row, delete if not needed
    dbc.Row([
       dbc.Col([
           centered_jumbo
       ], lg=8),
    ], justify='center'),

], id='centered-jumbo-layout', className='std-content-div', fluid=True)

