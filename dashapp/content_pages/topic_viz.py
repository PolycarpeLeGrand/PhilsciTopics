from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Uncomment the next import if app or cache are needed
# If using DataManagers, import them from dashapp on this line as well
from dashapp import cache, DM, MD

page_name = 'topic_viz'

# TODO
# Ajouter le nombre total de points/articles selon les settings
# Details sur clic d'un point
# Enlever les etiquettes des axes

text_controls_div = html.Div([

    #dbc.Row([
    #    dbc.Col(
    #        dcc.Markdown(MD.TOPICVIZ, className='content-text')
    #    )
    #], style={'margin-bottom': '2rem'}),

    dbc.Row([
        dbc.Col([
            dbc.Label('Representation type', className='content-text-small font-weight-bold'),
            dbc.RadioItems(
                options=[
                    {'label': '3 Dimensions T-SNE', 'value': 3},
                    {'label': '2 Dimensions T-SNE', 'value': 2},
                ],
                value=3,
                id='topic-viz-page-dimensions-checklist',
                style={'margin-left': '0rem'}
            )
        ], width=6),

        dbc.Col([
            dbc.Label('Include Periods: ', className='content-text-small font-weight-bold',
                      id='topic-viz-page-periods-label'),
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
                id='topic-viz-page-periods-slider',
                className='pl-0'
            )
        ], width=6)
    ], style={'margin-bottom': '2rem'}),

    dbc.Row([
        dbc.Col([
            dbc.Label('Journals to include', className='content-text-small font-weight-bold'),
            dbc.Checklist(
                options=[{'label': j, 'value': j} for j in DM.METADATA_DF['journal_id'].unique()],
                value=[j for j in DM.METADATA_DF['journal_id'].unique()],
                id='topic-viz-page-journals-checklist',
            ),
        ], width=6),
        dbc.Col([
            dbc.Label('Languages to include', className='content-text-small font-weight-bold'),
            dbc.Checklist(
                options=[{'label': lang, 'value': lang} for lang in DM.METADATA_DF['lang'].unique()],
                value=[lang for lang in DM.METADATA_DF['lang'].unique()],
                id='topic-viz-page-lang-checklist',
            ),
            dbc.Label('Total Included Articles: ', className='content-text-small font-weight-bold',
                      style={'padding-top': '2rem'}, id='topic-viz-page-included-label')
        ], width=6),
    ]),
])

article_details_div = html.Div([
    dbc.Row([
        dbc.Col([
            # Author date
            html.H4('Click a point on the graph to see article details', id='topic-viz-page-details-head'),
            # Full citation collapse
            html.Span('Title: ', className='content-text-small font-weight-bold'),
            html.Span(className='content-text-small', id='topic-viz-page-details-title'),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            html.Span('Journal: ', className='content-text-small font-weight-bold'),
            html.Span(className='content-text-small', id='topic-viz-page-details-journal'),
            html.Br(),
            html.Span('Language: ', className='content-text-small font-weight-bold'),
            html.Span(className='content-text-small', id='topic-viz-page-details-lang'),
        ], lg=6),
        dbc.Col([
            html.Span('Period: ', className='content-text-small font-weight-bold'),
            html.Span(className='content-text-small', id='topic-viz-page-details-period'),
            html.Br(),
            html.Span('Tokens: ', className='content-text-small font-weight-bold'),
            html.Span(className='content-text-small', id='topic-viz-page-details-tokens'),
        ], lg=6),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='topic-viz-page-details-pie')
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            html.Span('Full citation: ', className='content-text-small font-weight-bold'),
            html.Span(id='topic-viz-page-details-citation', className='content-text-small'),
        ]),
    ])
])

'''
    dbc.Row([
        dbc.Col(
            dbc.Button('Show Full Citation', id='topic-viz-page-details-button', color='link')
        ),
    ]),


    dbc.Row(
        dbc.Col(
            dbc.Collapse(
                dbc.Card(
                    'No article selected',
                    id='topic-viz-page-details-citation',
                    body=True,
                    className='content-text-small'
                ),
                id='topic-viz-page-details-collapse',
                is_open=False
            ),
        ),
    ),
'''

topic_main_card = dbc.Card([
    dbc.Row([
        dbc.Col(
            html.H2('Topic Visualizations')
        )
    ], className='title-row'),

    dbc.Row([
        dbc.Col([
            dcc.Markdown(MD.TOPICVIZ, className='content-text')
        ], lg=6, style={'margin-bottom': '2rem'}),
    ]),

    dbc.Row([
        dbc.Col([
            text_controls_div,
            html.Hr(style={'margin': '2rem'}),
            article_details_div
        ], lg=4, className='mt-5'),
        dbc.Col([
            dbc.Spinner(dcc.Graph(id='topic-viz-page-scatter', style={'height': '90vh', 'max-height': '100vw'})),
        ])
    ]),

    dbc.Row([
        dbc.Col([

        ]),
    ]),

], className='content-card', body=True)

topic_viz_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            topic_main_card
        ]),
    ]),
], id='topic-viz-layout', className='std-content-div', fluid=True)


def make_topicsviz_2d_scatter(df):
    ordered_topics = DM.TOPIC_MAPPINGS_DF['cluster_letter_+_topic_(id)'].sort_values().values
    df['dom_topic_name'] = df['dom_topic'].map(DM.TOPIC_MAPPINGS_DF['cluster_letter_+_topic_(id)'])
    fig = px.scatter(df, x='tsne_2d_x', y='tsne_2d_y', title='Documents-Topics Scatterplot', color='dom_topic_name',
                     color_discrete_map=DM.TOPIC_MAPPINGS_DF.set_index('cluster_letter_+_topic_(id)')[
                         'color_code_topic'].to_dict(),
                     hover_name=df.apply(lambda x: f'{x["author"]}, ({x["year"]})', axis=1),
                     hover_data={
                         'Title': df['title'].map(lambda x: x if len(x) < 60 else x[:60] + '...'),
                         'Main Topic': df['dom_topic_name'],
                         'Category': df['dom_topic_name'].map(DM.TOPIC_MAPPINGS_DF['cluster_name']),
                         'Journal': df['journal_id'],
                         'Period': df['period'],
                         'Language': df['lang'],
                         'tsne_2d_x': False,
                         'tsne_2d_y': False,
                         'dom_topic': False,
                         'dom_topic_name': False},
                     custom_data=[df.index],
                     category_orders={'dom_topic_name': ordered_topics})
    # color_discrete_sequence=px.colors.qualitative.Dark24, )
    fig.update_traces(marker={'size': 3})
    fig.update_layout(legend_title='Topics', legend_itemsizing='constant', paper_bgcolor='#fcfcfc') \
        .update_xaxes(range=[-100, 100]).update_yaxes(range=[-110, 110])
    return fig


# TODO et probs
# Dans l'autre version, on ajoute la colonne cluster_letter_+_topic_(id) a TOPIC_MAPPINGS_DF dans index, eto n reindex dessus
# Ca fait bcp de trouble, par exemple en settant color_discrete_map
# Pour l'instant on contourne le probleme en preprocessant le df avant de produire le graph mais il faudrait edit le df de base


def make_topicsviz_3d_scatter(df):
    df['dom_topic_name'] = df['dom_topic'].map(DM.TOPIC_MAPPINGS_DF['cluster_letter_+_topic_(id)'])
    ordered_topics = DM.TOPIC_MAPPINGS_DF['cluster_letter_+_topic_(id)'].sort_values().values
    fig = px.scatter_3d(df, x='tsne_3d_x', y='tsne_3d_y', z='tsne_3d_z', title='Documents-Topics Scatterplot',
                        color='dom_topic_name',
                        color_discrete_map=DM.TOPIC_MAPPINGS_DF.set_index('cluster_letter_+_topic_(id)')[
                            'color_code_topic'].to_dict(),
                        hover_name=df.apply(lambda x: f'{x["author"]} ({x["year"]})', axis=1),
                        hover_data={
                            'Title': df['title'].map(lambda x: x if len(x) < 60 else x[:60] + '...'),
                            'Main Topic': df['dom_topic_name'],
                            'Category': df['dom_topic_name'].map(DM.TOPIC_MAPPINGS_DF['cluster_name']),
                            'Journal': df['journal_id'],
                            'Period': df['period'],
                            'Language': df['lang'],
                            'tsne_3d_x': False,
                            'tsne_3d_y': False,
                            'tsne_3d_z': False,
                            'dom_topic': False,
                            'dom_topic_name': False},
                        custom_data=[df.index],
                        category_orders={'dom_topic_name': ordered_topics})
    # color_discrete_sequence=px.colors.qualitative.Dark24, )
    fig.update_traces(marker={'size': 2})
    fig.update_layout(legend_title='Topics', legend_itemsizing='constant', paper_bgcolor='#fcfcfc')
    # fig.update_scenes(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False)

    return fig


@callback(
    [Output('topic-viz-page-periods-label', 'children'),
     Output('topic-viz-page-scatter', 'figure'),
     Output('topic-viz-page-included-label', 'children')],
    [Input('topic-viz-page-dimensions-checklist', 'value'),
     Input('topic-viz-page-periods-slider', 'value'),
     Input('topic-viz-page-journals-checklist', 'value'),
     Input('topic-viz-page-lang-checklist', 'value')]
)
@cache.memoize()
def update_topic_viz_graph(n_dims, periods, journals, languages):
    ordered_periods = DM.METADATA_DF['period'].sort_values(key=lambda x: x.apply(lambda y: int(y[:4]))).unique()
    included_periods = ordered_periods[periods[0]:periods[1] + 1]

    df = DM.METADATA_DF.loc[DM.METADATA_DF['lang'].isin(languages)] \
        .loc[DM.METADATA_DF['journal_id'].isin(journals)] \
        .loc[DM.METADATA_DF['period'].isin(included_periods)]

    fig = make_topicsviz_2d_scatter(df) if int(n_dims) == 2 else make_topicsviz_3d_scatter(df)

    return f'Include Periods: {ordered_periods[periods[0]][:4]} to {ordered_periods[periods[1]][-4:]}', \
           fig, \
           f'Total Included Articles: {len(df)}'


@callback(
    [Output('topic-viz-page-details-head', 'children'),
     Output('topic-viz-page-details-title', 'children'),
     Output('topic-viz-page-details-journal', 'children'),
     Output('topic-viz-page-details-period', 'children'),
     Output('topic-viz-page-details-lang', 'children'),
     Output('topic-viz-page-details-tokens', 'children'),
     Output('topic-viz-page-details-pie', 'figure'),
     Output('topic-viz-page-details-citation', 'children')],
    [Input('topic-viz-page-scatter', 'clickData')], prevent_initial_call=True
)
def update_topicsvix_article_details(click_data):
    article_id = click_data['points'][0]['customdata'][0]
    article_data = DM.METADATA_DF.loc[article_id]

    head = f'Selected Article: {article_data["author"]} ({article_data["year"]})'
    title = article_data['title']
    journal = article_data['journal_id']
    lang = article_data['lang']
    period = article_data['period']
    tokens = article_data['n_token']
    citation = article_data['citation']

    # print(article_data)
    # print(DM.TOPIC_MAPPINGS_DF.loc[article_data[]])
    '''
    top_topics = DM.DOCTOPICS_DF.loc[article_id].nlargest(10)
    topic_divs = [
        html.Div(
            f'{DM.TOPIC_MAPPINGS_DF.loc[topic]["cluster_letter_+_topic_(id)"]} - {weight:.4f}',
            className='content-text-small',
            style={'color': DM.TOPIC_MAPPINGS_DF.loc[topic]['color_code_topic']}
        ) for topic, weight in top_topics.items()
    ]
    '''
    top_topics = DM.DOCTOPICS_DF.loc[article_id].sort_values(ascending=False).to_frame(name='values')
    top_topics['topics'] = top_topics.index.map(DM.TOPIC_MAPPINGS_DF['cluster_letter_+_topic_(id)'].to_dict())
    print(top_topics)
    fig = px.pie(top_topics,
                 values='values',
                 names='topics',
                 color='topics',
                 title='Topic Distribution',
                 color_discrete_map=DM.TOPIC_MAPPINGS_DF.set_index('cluster_letter_+_topic_(id)')[
                     'color_code_topic'].to_dict()
                 )

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(paper_bgcolor='#fcfcfc', showlegend=False)

    return head, title, journal, period, lang, tokens, fig, citation

'''
@callback(
    Output('topic-viz-page-details-collapse', 'is_open'),
    [Input('topic-viz-page-details-button', 'n_clicks')],
    [State('topic-viz-page-details-collapse', 'is_open')]
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
'''

