from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from config import BASE_STORAGE_PATH
import pickle

page_name = 'mempy-coocs'
COOC_SAMPLES = pickle.load(open(BASE_STORAGE_PATH / 'cooc_6_refs_sample_dict.p', 'rb'))

WORDS_0 = sorted(['mechanism', 'understand', 'explain', 'model', 'theory', 'predict'])
WORDS_1 = sorted(list(set(w for ws in COOC_SAMPLES.keys() for w in ws)))
# WORDS_0 = sorted(list(set(w[0] for w in COOC_SAMPLES.keys())))
# WORDS_1 = sorted(list(set(w[1] for w in COOC_SAMPLES.keys())))


def cooc_select(label_text, component_id, words):
    return html.Div([
        dbc.Label(label_text, className='content-text', style={'padding-right': '0.5rem'}),

        dbc.Select(
            options=[
                {'label': w, 'value': w} for w in words
            ],
            id=component_id,
            style={'min-width': '10rem', 'max-width': '20rem'},
        )
    ], style={'margin-bottom': '1rem'})


def cooc_entry(i, d):
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.H5(f'{i+1}. {d["citation"]}')
            ]),
        ], style={'margin-bottom': '1rem'}),
        dbc.Row([
            dbc.Col([
                html.Span(f'Texte du paragraphe (paragraphe {d["para_num"]})', style={'font-weight': '700'}),
                html.Div(d['para_text'], style={'padding-top': '1rem'})
            ]),
            dbc.Col([
                html.Span('Texte de l\'abstract', style={'font-weight': '700'}),
                html.Div(d['abs_text'], style={'padding-top': '1rem'})
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                html.Hr()
            ])
        ])
    ])


coocs_card = dbc.Card([
    dbc.CardHeader([
        html.H3('Références aux cooccurrences', className='mb-3'),
        cooc_select('Mot 1: ', 'cooc-select-0', WORDS_0),
        cooc_select('Mot 2: ', 'cooc-select-1', WORDS_1),
    ], className='content-card-head'),
    dbc.CardBody([
        html.Div(id='cooc-refs-div')
    ])
],  className='content-card')


mempy_coocs_layout = dbc.Container([
    dbc.Row([
       dbc.Col([
           coocs_card
       ]),
    ]),
], className='std-content-div', fluid=True)


@callback(
    Output('cooc-refs-div', 'children'),
    [Input('cooc-select-0', 'value'),
     Input('cooc-select-1', 'value')]
)
def update_cooc_exemples(w1, w2):
    pair = tuple(sorted([w1, w2]))
    refs = COOC_SAMPLES[pair]

    return html.Div([
        cooc_entry(i, d) for i, d in enumerate(refs)
    ])

