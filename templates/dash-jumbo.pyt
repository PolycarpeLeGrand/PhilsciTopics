# Example jumbotron
# The text layout can easily be set with dbc rows and cols
# Typically uses H2 with classname jumbotron-title for title
$jumbo_name$_jumbo = dbc.Jumbotron([
    dbc.Row([
        dbc.Col([
            html.H2('Main title spanning the whole width', className='jumbotron-title')
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            html.P('Left column text', className='content-text')
        ]),
        dbc.Col([
            html.P('Right column text', className='content-text')
        ]),
    ])
], className='content-jumbotron')

$END$