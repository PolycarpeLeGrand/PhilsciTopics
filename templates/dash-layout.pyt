$page_name$_layout = dbc.Container([
    # Jumbotron Row, delete if not needed
    dbc.Row([
       dbc.Col([
           # jumbotron
       ]),
    ]),

    # First card row, two columns
    dbc.Row([
        dbc.Col('card-1-children', lg=6),
        dbc.Col('card-2-children', lg=4),
    ]),
], id='$page_name$-layout', className='std-content-div', fluid=True)

$END$