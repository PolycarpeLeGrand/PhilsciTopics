from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px

# Uncomment the next import if app or cache are needed
# If using DataManagers, import them from dashapp on this line as well
from dashapp import cache, DM, MD

from config import JOURNAL_COLORS

page_name = 'corpus_page'

corpus_lang_select = dbc.Row([
    dbc.Col([
        dbc.Label('Include articles published in:', className='content-text'),
    ], width='auto'),
    dbc.Col([
        dbc.Checklist(
            options=[{'label': lang, 'value': lang} for lang in DM.METADATA_DF['lang'].unique()],
            # value=metadata_bar_checklist_values,
            value=[lang for lang in DM.METADATA_DF['lang'].unique()],
            id='corpus-page-bar-checklist',
            style={'padding-left': '12px'},
            inline=True,
            className='inline-input',
        ),
    ], width='auto'),
], justify='start', no_gutters=True, style={'margin-left': '4rem'})


corpus_sun_inputs = html.Div([

    dbc.Row([
        dbc.Col([
            dbc.Label('Selected Period:', id='corpus-page-sun-period', className='content-text font-weight-bold'),
            dcc.RangeSlider(
                min=0,
                max=len(DM.METADATA_DF['period'].unique()) - 1,
                value=[0, len(DM.METADATA_DF['period'].unique()) - 1],
                marks={
                    0: DM.METADATA_DF['period'].sort_values(key=lambda x: x.apply(lambda y: int(y[:4]))).unique()[0][:4],
                    len(DM.METADATA_DF['period'].unique()) - 1: DM.METADATA_DF['period'].sort_values(key=lambda x: x.apply(lambda y: int(y[:4]))).unique()[-1][-4:]
                },
                id='corpus-page-sun-slider',
                className='pl-0'
            ),
        ], lg=9),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(id='corpus-page-sun-lang', className='content-text-small'),
        ], lg=6, style={'min-width': '12rem'}),
        dbc.Col([
            dbc.Label('Total Articles: ', id='corpus-page-sun-total', className='content-text font-weight-bold'),
        ], lg=6, style={'min-width': '12rem'}),
    ], style={'margin-top': '1rem'}),
], style={'margin-top': '2rem'})


corpus_page_main_card = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col(html.H2('Exploring the Corpus')),
        ], className='title-row'),

        dbc.Row([
            dbc.Col([
                dcc.Markdown(MD.METADATA, className='content-text'),
                # corpus_lang_select,
            ], lg=3),
            dbc.Col([
                dbc.Spinner(dcc.Graph(id='corpus-page-bar')),
                corpus_lang_select,
            ], lg=9),
        ]),

        # Hr
        dbc.Row([
            dbc.Col([
                html.Hr(style={'margin': '2rem'})
            ])
        ]),

        # Sunburst section
        dbc.Row([
            dbc.Col([
                dcc.Markdown(MD.META_SUNBURST, className='content-text'),
                corpus_sun_inputs,
            ], lg=3),
            dbc.Col([
                dbc.Spinner(dcc.Graph('corpus-page-sun-graph', style={'max-width': '600px'}))#style={'height': '50vh', 'max-height': '90vw', 'width': '50vh', 'max-width': '90vw'})),
            ], lg=9, style={'padding-left': '2rem'}),
        ]),
    ])
],  className='content-card')

corpus_layout = dbc.Container([
    # Jumbotron Row, delete if not needed
    dbc.Row([
       dbc.Col([
           corpus_page_main_card
       ]),
    ]),
], id='corpus-layout', className='std-content-div', fluid=True)


@callback(
    Output('corpus-page-bar', 'figure'),
    [Input('corpus-page-bar-checklist', 'value')]
)
@cache.memoize()
def update_journals_bar(checked_values):
    df = DM.METADATA_DF[['journal_id', 'period', 'lang']]
    df = df.loc[df['lang'].isin(checked_values)]
    groups = ['journal_id', 'period']
    df = df.groupby(groups).size().reset_index(name='counts')

    ordered_periods = DM.METADATA_DF['period'].sort_values(key=lambda x: x.apply(lambda y: int(y[:4]))).unique()

    fig = px.bar(df, x='period', y='counts', color='journal_id',
                 category_orders={'period': ordered_periods},
                 color_discrete_map=JOURNAL_COLORS,)

    fig.update_layout(legend_title='Journals', xaxis_title='Time periods',
                      yaxis_title='Number of articles', title='Number of Articles by Time Periods',
                      )# paper_bgcolor='#fcfcfc')# plot_bgcolor=GRAPH_COLORS['background'], paper_bgcolor=GRAPH_COLORS['background'], font_color=GRAPH_COLORS['text'])

    show_labels = False
    if show_labels:
        label_group = df.groupby('period')['counts'].sum()
        y_offset = 0.05 * label_group.max()
        fig.update_layout(annotations=[{'x': p, 'y': n + y_offset, 'text': n, 'showarrow': False} for p, n in
              df.groupby('period')['counts'].sum().items()])

    return fig


@callback(
    [Output('corpus-page-sun-period', 'children'),
     Output('corpus-page-sun-total', 'children'),
     Output('corpus-page-sun-graph', 'figure'),
     Output('corpus-page-sun-lang', 'children'), ],
    [Input('corpus-page-sun-slider', 'value')]
)
@cache.memoize()
def update_sunburst(val):
    ordered_periods = DM.METADATA_DF['period'].sort_values(key=lambda x: x.apply(lambda y: int(y[:4]))).unique()
    beg = ordered_periods[val[0]]
    end = ordered_periods[val[1]]

    periods = ordered_periods[val[0]:val[1]+1]

    df = DM.METADATA_DF[['journal_id', 'lang']].loc[DM.METADATA_DF['period'].isin(periods)]
    lang_counts = df['lang'].value_counts()
    df = df.groupby(['journal_id', 'lang']).size().reset_index(name='counts')

    fig = px.sunburst(df, path=['journal_id', 'lang'], values='counts', color='journal_id',
                      color_discrete_map=JOURNAL_COLORS, title='Journal and Language Distributions')

    total_articles = df["counts"].sum()
    lang_md = '  \n'.join(f'{i}: {v} ({(v/total_articles)*100:.2f}%)' for i, v in lang_counts.iteritems())

    return f'Selected Period: {beg[:4]}-{end[-4:]}', f'Total Articles: {total_articles}', fig, lang_md

