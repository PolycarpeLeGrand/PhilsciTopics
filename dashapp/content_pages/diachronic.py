from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px

from dashapp import cache, DM, MD

page_name = 'diachronic_page'

diachro_selects = html.Div([

    dbc.Row([
        dbc.Col([
            dbc.Label('Data type', className='content-text-small font-weight-bold'),
            dbc.RadioItems(
                options=
                [
                    {'label': 'Average', 'value': 'avg'},
                    {'label': 'Main', 'value': 'main'},
                ],
                value='avg',
                id='diachro-page-val-radio',
            ),
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Label('Journals to include', className='content-text-small font-weight-bold'),
            dbc.Checklist(
                options=[{'label': j, 'value': j} for j in DM.METADATA_DF['journal_id'].unique()],
                value=[j for j in DM.METADATA_DF['journal_id'].unique()],
                id='diachro-page-journals-checklist',
            ),
        ],),
    ], style={'margin-bottom': '1rem'}),

    dbc.Row([
        dbc.Col([
            dbc.Label('Languages to include', className='content-text-small font-weight-bold'),
            dbc.Checklist(
                options=[{'label': lang, 'value': lang} for lang in DM.METADATA_DF['lang'].unique()],
                value=[lang for lang in DM.METADATA_DF['lang'].unique()],
                id='diachro-page-lang-checklist',
            ),
            dbc.Label('Total Included Articles: ', className='content-text-small font-weight-bold',
                      style={'padding-top': '1rem'}, id='diachro-page-included-label')
        ],),
    ]),
])

diachronic_card = dbc.Card([
    dbc.Row([
        dbc.Col([
            html.H2('Diachronic Overview'),
        ]),
    ], className='title-row'),
    dbc.Row([
        dbc.Col([
            diachro_selects
        ], lg=2),
        dbc.Col([
            dbc.Spinner(dcc.Graph(id='diachro-page-histo', style={'height': '80vh'})),
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


@callback(
    Output('diachro-page-histo', 'figure'),
    [Input('diachro-page-val-radio', 'value'),
     Input('diachro-page-journals-checklist', 'value'),
     Input('diachro-page-lang-checklist', 'value'),]
)
def update_diachronic_histo(val, journals, languages):
    ordered_periods = DM.METADATA_DF['period'].sort_values(key=lambda x: x.apply(lambda y: int(y[:4]))).unique()
    ordered_topics = DM.TOPIC_MAPPINGS_DF['cluster_letter_+_topic_(id)'].sort_values().values

    if val == 'avg':
        df = DM.DOCTOPICS_DF.loc[DM.METADATA_DF['lang'].isin(languages)] \
            .loc[DM.METADATA_DF['journal_id'].isin(journals)].groupby(DM.METADATA_DF['period']).mean()
        df.columns = df.columns.map(DM.TOPIC_MAPPINGS_DF['cluster_letter_+_topic_(id)'])
        x, y, color = df.index, df.columns, None
    else:
        df = DM.METADATA_DF.loc[DM.METADATA_DF['lang'].isin(languages)] \
            .loc[DM.METADATA_DF['journal_id'].isin(journals)].groupby(['period', 'dom_topic']).size().reset_index(name='counts')
        df['counts'] = df.groupby('period')['counts'].apply(lambda x: x / x.sum())
        df['dom_topic'] = df['dom_topic'].map(DM.TOPIC_MAPPINGS_DF['cluster_letter_+_topic_(id)'])
        x, y, color = 'period', 'counts', 'dom_topic'

    fig = px.bar(df, x=x, y=y, color=color,
                 category_orders={'period': ordered_periods,
                                  'variable': ordered_topics,
                                  'dom_topic': ordered_topics},
                 color_discrete_map=DM.TOPIC_MAPPINGS_DF.set_index('cluster_letter_+_topic_(id)')[
                     'color_code_topic'].to_dict(),)
    fig.update_layout(bargap=0.0, legend_title='Topics', legend_traceorder='reversed',
                      plot_bgcolor='#fcfcfc',
                      paper_bgcolor='#fcfcfc',
                      title='Topic distributions by time periods',
                      xaxis_title='Time periods',
                      yaxis_title='Topic distributions')\
        .update_traces(marker_line_width=0.0, selector={'type': 'bar'})
    return fig


