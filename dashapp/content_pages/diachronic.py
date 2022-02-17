from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from dashapp import cache, DM, MD

page_name = 'diachronic_page'


def make_anim_graph(frame_duration=2000, transition_duration=1000, transition_easing='cubic-in-out'):
    df = DM.DOCTOPICS_DF.groupby(DM.METADATA_DF['period']).mean()
    d = [{'period': p, 'topic': t, 'avg_weight': w} for t in df.columns for p, w in df[t].iteritems()]
    df = pd.DataFrame.from_records(d)
    df['topic'] = df['topic'].map(DM.TOPIC_MAPPINGS_DF['cluster_letter_+_topic_(id)'])
    df = df.sort_values('topic', ascending=False)
    ordered_periods = DM.METADATA_DF['period'].sort_values(key=lambda x: x.apply(lambda y: int(y[:4]))).unique()
    fig = px.bar(df, x='topic', y='avg_weight', color='topic', animation_frame='period', text='topic',
                 category_orders={'period': ordered_periods},
                 color_discrete_map=DM.TOPIC_MAPPINGS_DF.set_index('cluster_letter_+_topic_(id)')['color_code_topic'].to_dict(),
                 range_y=[0,0.26],
                 title=f'Average topic weights for period {ordered_periods[0]}',
                 #hover_name=df['topic'],
                 hover_data={
                     'Topic': df['topic'],
                     'Average Weight': df['avg_weight'].map(lambda x: f'{x:.4f}'),
                     'Period': df['period'],
                     'topic': None,
                     'period': None,
                     'avg_weight': None,
                 })\
        .update_layout(bargap=0,
                       xaxis_title='Topics',
                       yaxis_title='Average topic weights',
                       xaxis={'categoryorder': 'array', 'categoryarray': df[df['period']==ordered_periods[0]].sort_values('avg_weight', ascending=False)['topic'].values,
                              'showticklabels': False,
                              'ticklabelposition': 'inside', 'tickangle': 90},
                       margin_t=30,
                       margin_b=10,)\
        .update_traces(textposition='inside')
    for f in fig.frames:
        f.layout.update(title=f'Average topic weights for period {f.name}',
                        xaxis={'categoryorder': 'array',
                               'categoryarray': df[df['period']==f.name].sort_values('avg_weight', ascending=False)['topic'].values,},
                        legend={'traceorder': 'normal'})
        for d in f.data:
            d['textposition'] = 'inside'

    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = frame_duration
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['easing'] = transition_easing
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = transition_duration
    fig.layout.sliders[0]['currentvalue']['prefix'] = 'Period: '
    return fig


diachro_selects = html.Div([

    dbc.Row([
        dbc.Col([
            dcc.Markdown('Explication', className='content-text'),
        ]),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Label('Sort data by', className='content-text-small font-weight-bold'),
            dbc.RadioItems(
                options=
                [
                    {'label': 'Average topic weights', 'value': 'avg'},
                    {'label': 'Proportion of articles with topic as main', 'value': 'main'},
                ],
                value='avg',
                id='diachro-page-val-radio',
            ),
        ])
    ], style={'margin-bottom': '1rem'}),

    dbc.Row([
        dbc.Col([
            dbc.Label('Journals to include', className='content-text-small font-weight-bold'),
            dbc.Checklist(
                options=[{'label': j, 'value': j} for j in DM.METADATA_DF['journal_id'].unique()],
                value=[j for j in DM.METADATA_DF['journal_id'].unique()],
                id='diachro-page-journals-checklist',
            ),
        ],),
        dbc.Col([
            dbc.Label('Languages to include', className='content-text-small font-weight-bold'),
            dbc.Checklist(
                options=[{'label': lang, 'value': lang} for lang in DM.METADATA_DF['lang'].unique()],
                value=[lang for lang in DM.METADATA_DF['lang'].unique()],
                id='diachro-page-lang-checklist',
            ),
            dbc.Label('Total included articles: ', className='content-text-small font-weight-bold',
                      style={'padding-top': '1rem'}, id='diachro-page-included-label')
        ],),
    ]),
])

animation_controls = html.Div([
    dbc.Label('Time per step (ms) (set time per step > animation time to pause between each step)'),
    dbc.Input(type='number', min=0, max=10000, step=100, value=2000, id='diachro-animation-delay-input', style={'max-width': '10rem', 'margin-bottom': '1rem'}),
    dbc.Label('Animation time (ms)'),
    dbc.Input(type='number', min=0, max=10000, step=100, value=1000, id='diachro-animation-duration-input', style={'max-width': '10rem', 'margin-bottom': '1rem'}),
    dbc.Label('Animation type:'),
    dbc.Select(
        options=[
            {'label': t, 'value': t} for t in ['cubic-in-out', 'linear', 'quad-in-out']
        ],
        value='cubic-in-out',
        id='diachro-animation-transition-select',
        style={'max-width': '10rem'})
])

diachronic_card = dbc.Card([
    dbc.Row([
        dbc.Col([
            html.H2('Exploring topic changes over time'),
        ]),
    ], className='title-row'),
    dbc.Row([
        dbc.Col([
            diachro_selects
        ], lg=3),
        dbc.Col([
            dbc.Spinner(dcc.Graph(id='diachro-page-histo', style={'height': '80vh'})),
        ], lg=9),
    ]),

    dbc.Row([
        dbc.Col(html.Hr(style={'margin': '2rem'})),
    ]),

    dbc.Row([
        dbc.Col([
            animation_controls,
        ], lg=3),
        dbc.Col([
            dbc.Spinner(dcc.Graph(id='diachro-animation-graph', style={'height': '40rem'}))
        ], lg=9),
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
    [Output('diachro-page-histo', 'figure'),
     Output('diachro-page-included-label', 'children')],
    [Input('diachro-page-val-radio', 'value'),
     Input('diachro-page-journals-checklist', 'value'),
     Input('diachro-page-lang-checklist', 'value'),]
)
@cache.memoize()
def update_diachronic_histo(val, journals, languages):
    ordered_periods = DM.METADATA_DF['period'].sort_values(key=lambda x: x.apply(lambda y: int(y[:4]))).unique()
    ordered_topics = DM.TOPIC_MAPPINGS_DF['cluster_letter_+_topic_(id)'].sort_values().values

    if val == 'avg':
        s = 'Average weight'
        df = DM.DOCTOPICS_DF.loc[DM.METADATA_DF['lang'].isin(languages)] \
            .loc[DM.METADATA_DF['journal_id'].isin(journals)]
        n_docs = len(df)
        df = df.groupby(DM.METADATA_DF['period']).mean()
        df.columns = df.columns.map(DM.TOPIC_MAPPINGS_DF['cluster_letter_+_topic_(id)'])
        x, y, color = df.index, df.columns, None
    else:
        s = 'Main topic frequency'
        df = DM.METADATA_DF.loc[DM.METADATA_DF['lang'].isin(languages)] \
            .loc[DM.METADATA_DF['journal_id'].isin(journals)]
        n_docs = len(df)
        df = df.groupby(['period', 'dom_topic']).size().reset_index(name='counts')
        df['counts'] = df.groupby('period')['counts'].apply(lambda x: x / x.sum())
        df['dom_topic'] = df['dom_topic'].map(DM.TOPIC_MAPPINGS_DF['cluster_letter_+_topic_(id)'])
        x, y, color = 'period', 'counts', 'dom_topic'

    fig = px.bar(df, x=x, y=y, color=color,
                 category_orders={'period': ordered_periods,
                                  'variable': ordered_topics,
                                  'dom_topic': ordered_topics},
                 color_discrete_map=DM.TOPIC_MAPPINGS_DF.set_index('cluster_letter_+_topic_(id)')[
                     'color_code_topic'].to_dict(),
                 )
    fig.update_layout(bargap=0.0, legend_title='Topics', legend_traceorder='reversed',
                      plot_bgcolor='#fcfcfc',
                      paper_bgcolor='#fcfcfc',
                      title='Topic distributions by time periods',
                      xaxis_title='Time periods',
                      yaxis_title=f'Topic distributions ({s})',
                      margin_t=30
                      )\
        .update_traces(marker_line_width=0.0)
    for d in fig.data:
        d['hovertemplate'] = f'Topic={d["legendgroup"]}<br>Period=%{{label}}<br>{s}=%{{value:.4f}}<extra></extra>'

    return fig, f'Total included articles: {n_docs}'


@callback(Output('diachro-animation-graph', 'figure'),
          [Input('diachro-animation-delay-input', 'value'),
           Input('diachro-animation-duration-input', 'value'),
           Input('diachro-animation-transition-select', 'value'),])
def update_anim_fig(delay, duration, animation):
    return make_anim_graph(delay, duration, animation)