import dash
from flask_caching import Cache
import plotly.io as pio
import plotly.graph_objects as go

from config import PROJECT_TITLE, IS_PROD, DATAFRAMES_DICT, USE_CACHE, CACHE_CONFIG, GENERATE_DF_DOC_FILE, MARKDOWNS_DICT
from data.df_manager import DfManager
from data.md_manager import MdManager


app = dash.Dash(
    __name__,
    title=PROJECT_TITLE,
    suppress_callback_exceptions=IS_PROD,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)

if USE_CACHE:
    cache = Cache(
        app.server,
        config=CACHE_CONFIG
    )

# Inits de DfManager object as specified in config
# Dataframes can be accessed in modules by importing DM (e.g. import DM; DM.TEST_DF)
DM = DfManager(DATAFRAMES_DICT, GENERATE_DF_DOC_FILE)
MD = MdManager(MARKDOWNS_DICT)

pio.templates['plotly'] = go.layout.Template(
    layout={
        # Background color outside graph area, should match container background as set in CSS
        'paper_bgcolor': '#fcfcfc',
        # Graph area background
        'plot_bgcolor': '#fcfcfc',
        # Font property is a dict, family, size, color, etc.
        'font': {'family': 'Helvetica, Sans-serif', 'color': '#212529'},
        'title_y': 1,
    }
)

