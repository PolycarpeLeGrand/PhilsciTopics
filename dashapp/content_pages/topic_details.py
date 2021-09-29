from dash import Dash, dcc, html, Input, Output, State, callback
import dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from dashapp import cache, DM, MD

page_name = 'topic_details'

wordcloud_div = html.Div([
    html.Img(src='assets/wordclouds/wc_topic_0.png',
             style={'width': '100%', 'border': 'solid', 'border-width': '1px'},
             id='topics-details-page-wordcloud'),
])

word_vert_radios = html.Div([
    dbc.RadioItems(
        labelClassName="btn btn-secondary radio-button",
        labelCheckedClassName="active",
        options=[
            {"label": "Option 1", "value": 1},
            {"label": "Option 2", "value": 2},
            {"label": "Option 3", "value": 3},
        ],
        value=1,
        inline=False,
        inputStyle={'display': 'none'},  # Removes the radio circle thing so it looks like a button
        labelStyle={'width': '8rem', 'margin-left': '-1rem', 'text-align': 'left'},
        className='radio-button',
        id='topic-details-page-words-radio'
    ),
])

top_words_table_div = html.Div([
    dash_table.DataTable(
        columns=[
            {'name': '', 'id': 'num_col'},
            {'name': 'Word', 'id': 'word_col'},
            {'name': 'Weight', 'id': 'weight_col'},
        ],
        id='topic-details-page-words-table',
        cell_selectable=False,
        row_selectable='single',
        style_cell={'height': '2rem', 'padding': '0 0.5rem'},
        style_header={'border': 'none', 'background': '#318e7d', 'text-align': 'center'},
        css=[{'selector': '.dash-table-container', 'rule': 'font-family: inherit'}, ]
    )
])

word_details_div = html.Div([
    dbc.Row([
        dbc.Col([
            # word_vert_radios
            top_words_table_div
        ], width='auto', style={'padding': '0'}),
        dbc.Col([
            html.Div([
                html.Div('Weight distribution across topics',
                         style={'height': '2rem', 'background': '#318e7d',
                                'display': 'flex', 'justify-content': 'center',
                                'align-items': 'center', 'border-bottom': '1px solid rgb(211, 211, 211)'}),
                dcc.Graph(id='topic-details-page-word-pie',
                          style={'width': '24rem', 'height': '24rem', 'border': '1px solid rgb(211, 211, 211)',
                                 'border-top': 'none'})
            ])
        ], width='auto', style={'padding': '0'}),
    ],
        style={'border': '2px solid rgb(211, 211, 211)', 'width': 'fit-content'}
    ),
])

citations_control_div = html.Div([

    dbc.Row([

        dbc.Col([
            dbc.Label('Include Periods: ', className='content-text-small font-weight-bold',
                      id='topic-details-page-periods-label'),
            dcc.RangeSlider(
                min=0,
                max=len(DM.METADATA_DF['period'].unique()) - 1,
                value=[0, len(DM.METADATA_DF['period'].unique()) - 1],
                marks={
                    0: DM.METADATA_DF['period'].sort_values(key=lambda x: x.apply(lambda y: int(y[:4]))).unique()[0][
                       :4],
                    len(DM.METADATA_DF['period'].unique()) - 1:
                        DM.METADATA_DF['period'].sort_values(key=lambda x: x.apply(lambda y: int(y[:4]))).unique()[-1][
                        -4:]
                },
                id='topic-details-page-periods-slider',
                className='pl-0'
            )
        ],)
    ], style={'margin-bottom': '1rem'}),

    dbc.Row([
        dbc.Col([
            dbc.Label('Journals to include', className='content-text-small font-weight-bold'),
            dbc.Checklist(
                options=[{'label': j, 'value': j} for j in DM.METADATA_DF['journal_id'].unique()],
                value=[j for j in DM.METADATA_DF['journal_id'].unique()],
                id='topic-details-page-journals-checklist',
            ),
        ],),
    ], style={'margin-bottom': '1rem'}),

    dbc.Row([
        dbc.Col([
            dbc.Label('Languages to include', className='content-text-small font-weight-bold'),
            dbc.Checklist(
                options=[{'label': lang, 'value': lang} for lang in DM.METADATA_DF['lang'].unique()],
                value=[lang for lang in DM.METADATA_DF['lang'].unique()],
                id='topic-details-page-lang-checklist',
            ),
            dbc.Label('Total Included Articles: ', className='content-text-small font-weight-bold',
                      style={'padding-top': '1rem'}, id='topic-details-page-included-label')
        ],),
    ]),
])

citations_table_div = html.Div([
    dash_table.DataTable(
        columns=[
            {'name': '', 'id': 'rank'},
            {'name': 'Weight', 'id': 'weight'},
            {'name': '', 'id': 'art_id'},
            {'name': 'Citation', 'id': 'citation'},
        ],
        id='topic-details-page-citations-table',
        cell_selectable=False,
        row_selectable='single',
        style_cell={'height': '2.5rem', 'padding': '0 0.5rem'},
        style_header={'border': 'none', 'background': '#318e7d', 'text-align': 'center'},
        style_data={
            'whiteSpace': 'normal',
        },
        css=[
                {'selector': '.dash-table-container', 'rule': 'font-family: inherit'},
            ],
        style_cell_conditional=[
            {'if': {'column_id': 'citation'}, 'textAlign': 'left', 'maxWidth': '800px'},
            {'if': {'column_id': 'art_id'}, 'display': 'none'},
        ],
    )
])

citations_details_div = html.Div([
    dbc.Row([
        dbc.Col([
            # word_vert_radios
            citations_table_div
        ], width='auto', style={'padding': '0'}),
        dbc.Col([
            html.Div([
                html.Div('Article topic distribution',
                         style={'height': '2.5rem', 'background': '#318e7d',
                                'display': 'flex', 'justify-content': 'center',
                                'align-items': 'center'}),
                dcc.Graph(id='topic-details-page-citations-pie',
                          style={'width': '25rem', 'height': '25rem'})
            ])
        ], width='auto', style={'padding': '0', 'background': 'rgb(241, 241, 241)'}),
    ],
        style={'border': '2px solid rgb(211, 211, 211)', 'width': 'fit-content'}
    ),
], style={'margin-top': '5rem'})

topic_details_card = dbc.Card([
    dbc.Row([
        dbc.Col([
            html.H2('Topic Details'),
        ]),
    ], className='title-row'),

    dbc.Row([
        dbc.Col([
            dcc.Markdown(MD.TOPICDETAILS, className='content-text'),
            dbc.Select(
                options=[
                    {'label': v, 'value': t} for t, v in
                    DM.TOPIC_MAPPINGS_DF['cluster_letter_+_topic_(id)'].sort_values().iteritems()
                ],
                value=DM.TOPIC_MAPPINGS_DF['cluster_letter_+_topic_(id)'].sort_values().index[0],
                id='topic-details-page-topic-select'
            ),
        ], lg=6),
        dbc.Col([
            # dcc.Graph(figure=make_words_topics_barchart())
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            wordcloud_div
        ], lg=6, style={'margin-right': '2rem'}),
        dbc.Col([
            word_details_div
        ], lg='auto'),
    ], style={'margin-top': '2rem'}),

    dbc.Row([
        dbc.Col([
            html.Hr(style={'margin': '2rem'})
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Markdown(
                'Top articles for the selected topic. Use the controls to select which periods, journals and languages to include.',
                className='content-text')
        ], lg=6),
    ]),

    dbc.Row([
        dbc.Col([
            citations_control_div,
        ], lg=2),
        dbc.Col([
            citations_details_div
        ], lg='auto'),
    ]),

], body=True, className='content-card')

# Line/pointplots of word weights per topic (top 1000, 5000?) to see weight diminution

topic_details_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            topic_details_card
        ]),
    ]),
], id='topic-details-layout', className='std-content-div', fluid=True)


@callback(
    [Output('topic-details-page-words-table', 'data'),
     Output('topics-details-page-wordcloud', 'src'),
     Output('topic-details-page-words-table', 'selected_rows')],
    [Input('topic-details-page-topic-select', 'value')]
)
def update_topic(topic):
    words = DM.TOPICWORDS_DF.loc[topic].nlargest(12).to_frame().reset_index()
    words['num_col'] = [f'{i + 1}.' for i in words.index]
    words.columns = ['word_col', 'weight_col', 'num_col']
    words['weight_col'] = words['weight_col'].map(lambda x: f'{x:.4f}')

    # return [{'label': f'{i+1}. {w}', 'value': w} for i, w in enumerate(words)], words[0], f'assets/wordclouds/wc_{topic}.png'
    return words.to_dict('records'), f'assets/wordclouds/wc_{topic}.png', [0]


def make_words_topics_fig(word=None):
    words = DM.TOPICWORDS_DF.loc['topic_0'].nlargest(10)
    # print(words)

    # df = DM.TOPICWORDS_DF[words.index]
    # print(DM.TOPICWORDS_DF.sum(axis=1))
    # word = words.index[0]

    # print(DM.TOPICWORDS_DF)

    df = DM.TOPICWORDS_DF[word].to_frame(name='values')
    df['topics'] = df.index.map(DM.TOPIC_MAPPINGS_DF['cluster_letter_+_topic_(id)'].to_dict())

    fig = px.pie(df, values='values', names='topics', color='topics',
                 color_discrete_map=DM.TOPIC_MAPPINGS_DF.set_index('cluster_letter_+_topic_(id)')[
                     'color_code_topic'].to_dict(),
                 title=word)

    fig.update_traces(textposition='inside', texttemplate='%{label} <br>%{value:.5f}')
    fig.update_layout(paper_bgcolor='rgb(241, 241, 241)', showlegend=False, title=f'"{word}" topic weights',
                      margin={'l': 0, 'r': 0, 't': 52, 'b': 12})
    '''
    fig = go.Figure()
    for t in df.index:
        fig.add_trace(go.Bar(
            y=df.columns,
            x=df.loc[t],
            name=t,
            orientation='h',
            marker=dict(
                color='rgba(246, 78, 139, 0.6)',
                # line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
            )
        ))

    fig.update_layout(barmode='stack')
    '''
    # fig = px.bar(df, x=df.columns, y=df.index)

    return fig


@callback(
    [Output('topic-details-page-word-pie', 'figure'),
     Output('topic-details-page-words-table', 'style_data_conditional')],
    [Input('topic-details-page-words-table', 'selected_rows')],
    [State('topic-details-page-words-table', 'data')]
)
def update_word_details(rows, data):
    word = data[rows[0]]['word_col']
    cond_style = [
        {'if': {'row_index': rows[0]}, 'backgroundColor': '#f1f1f1', }
    ]
    return make_words_topics_fig(word), cond_style


@callback(
    [Output('topic-details-page-periods-label', 'children'),
     Output('topic-details-page-included-label', 'children'),
     Output('topic-details-page-citations-table', 'data'),
     Output('topic-details-page-citations-table', 'selected_rows')],
    [Input('topic-details-page-periods-slider', 'value'),
     Input('topic-details-page-journals-checklist', 'value'),
     Input('topic-details-page-lang-checklist', 'value'),
     Input('topic-details-page-topic-select', 'value')]
)
@cache.memoize()
def update_topic_details_citations(periods, journals, languages, topic):
    ordered_periods = DM.METADATA_DF['period'].sort_values(key=lambda x: x.apply(lambda y: int(y[:4]))).unique()
    included_periods = ordered_periods[periods[0]:periods[1] + 1]

    df = DM.METADATA_DF.loc[DM.METADATA_DF['lang'].isin(languages)] \
        .loc[DM.METADATA_DF['journal_id'].isin(journals)] \
        .loc[DM.METADATA_DF['period'].isin(included_periods)]

    tot_articles = len(df)

    top_articles = DM.DOCTOPICS_DF.loc[df.index][topic].nlargest(10)
    df = df.loc[top_articles.index]
    df['weight'] = top_articles.values
    df['weight'] = df['weight'].map(lambda x: f'{x:.4f}')
    df['rank'] = [f'{i+1}.' for i in range(len(df))]
    df['art_id'] = df.index

    df = df[['citation', 'weight', 'rank', 'art_id']]

    return f'Include Periods: {ordered_periods[periods[0]][:4]} to {ordered_periods[periods[1]][-4:]}', \
           f'Total Included Articles: {tot_articles}', \
           df.to_dict('records'), \
           [0]
           #citations_children


def make_citation_topics_fig(article=None):
    #words = DM.TOPICWORDS_DF.loc['topic_0'].nlargest(10)
    # print(words)

    # df = DM.TOPICWORDS_DF[words.index]
    # print(DM.TOPICWORDS_DF.sum(axis=1))
    # word = words.index[0]

    # print(DM.TOPICWORDS_DF)

    #df = DM.TOPICWORDS_DF[word].to_frame(name='values')
    #df['topics'] = df.index.map(DM.TOPIC_MAPPINGS_DF['cluster_letter_+_topic_(id)'].to_dict())

    df = DM.DOCTOPICS_DF.loc[article].to_frame(name='values')
    print(df)
    df['topics'] = df.index.map(DM.TOPIC_MAPPINGS_DF['cluster_letter_+_topic_(id)'].to_dict())
    print(df)

    fig = px.pie(df, values='values', names='topics', color='topics',
                 color_discrete_map=DM.TOPIC_MAPPINGS_DF.set_index('cluster_letter_+_topic_(id)')[
                     'color_code_topic'].to_dict())

    fig.update_traces(textposition='inside', texttemplate='%{label} <br>%{value:.5f}')
    fig.update_layout(paper_bgcolor='rgb(241, 241, 241)', showlegend=False,
                      margin={'l': 0, 'r': 0, 't': 52, 'b': 12})

    return fig


@callback(
    [Output('topic-details-page-citations-pie', 'figure'),
     Output('topic-details-page-citations-table', 'style_data_conditional')],
    [Input('topic-details-page-citations-table', 'selected_rows')],
    [State('topic-details-page-citations-table', 'data')]
)
def update_citations_details(rows, data):
    art_id = data[rows[0]]['art_id']
    cond_style = [
        {'if': {'row_index': rows[0]}, 'backgroundColor': '#f1f1f1', }
    ]
    return make_citation_topics_fig(art_id), cond_style
