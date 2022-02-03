from pathlib import Path
from dotenv import load_dotenv
from os import environ

# Browser tab title
PROJECT_TITLE = 'PhilsciTopics'

# Title and subtitle to display on navbar
NAV_TITLE = 'PhilsciTopics'
NAV_SUBTITLE = 'A digital history of philosophy of science'


# Load project settings
PROJECT_PATH = Path(__file__).parent
load_dotenv(PROJECT_PATH / '.env')
LOCAL_IP = environ.get('LOCAL_IP')
IS_PROD = environ.get('IS_PROD') == 'True'
PORT = 33

# If the data is not stored in the project directory, specify the path in .env and that path instead
# BASE_STORAGE_PATH = Path(environ.get('LOCAL_STORAGE_PATH'))
BASE_STORAGE_PATH = PROJECT_PATH / 'data'

# Pickled Dataframes to be loaded in the DfManager on app init
# Keys will be added to the DfManager object as variables <DfManager>.<key>
# Values can be either a path to the df or a tuple consisting of the path and a string (markdown) describing the df
GENERATE_DF_DOC_FILE = True
DATAFRAMES_DICT = {
    'TEST_DF': (BASE_STORAGE_PATH / 'dataframes/test_data_df.p', 'A simple test dataframe'),
    'TEST_DF_2': BASE_STORAGE_PATH / 'dataframes/test_data_df.p',
    'DOCTOPICS_DF': BASE_STORAGE_PATH / 'dataframes/doctopics_df.p',
    'METADATA_DF': BASE_STORAGE_PATH / 'dataframes/metadata_df.p',
    'TOPIC_MAPPINGS_DF': BASE_STORAGE_PATH / 'dataframes/topic_mappings_df.p',
    'TOPICWORDS_DF': BASE_STORAGE_PATH / 'dataframes/topicwords_df.p',
}


# Same idea, but for markdown documents. Only paths as values, no tuples with doc.
# Temporary feature until i come up with something better
MARKDOWNS_DICT = {
    'test_md': BASE_STORAGE_PATH / 'markdowns/test_md.md',
    'METADATA': BASE_STORAGE_PATH / 'markdowns/metadata.md',
    'HOWTO': BASE_STORAGE_PATH / 'markdowns/howto.md',
    'PRESENTATION': BASE_STORAGE_PATH / 'markdowns/presentation.md',
    'REFERENCES': BASE_STORAGE_PATH / 'markdowns/references.md',
    'TOPICDETAILS': BASE_STORAGE_PATH / 'markdowns/topicdetails.md',
    'TOPICVIZ': BASE_STORAGE_PATH / 'markdowns/topicviz.md',
    'META_SUNBURST': BASE_STORAGE_PATH / 'markdowns/meta_sunburst.md',
    'SUBTITLES': BASE_STORAGE_PATH / 'markdowns/subtitles.md',
}


JOURNAL_COLORS = {
    'BJPS': '#66C5CC',
    'EJPS': '#F6CF71',
    'ERK': '#F89C74',
    'ISPS': '#DCB0F2',
    'JGPS': '#87C55F',
    'PS': '#9EB9F3',
    'SHPSA': '#FE88B1',
    'SYN': '#C9DB74',
    'en': '#F89C74',
    'de': '#F6CF71',
    'fr': '#66C5CC',
    'nl': '#DCB0F2',
}

#MD_DIRECTORIES = [
#    BASE_STORAGE_PATH / 'markdowns',
#]

# Cache config
# Specify if using cache, and which config to use for prod and test
# If using Redis, specify info in .env
# Redis config:
#   Make sure Redis package is installed (pip install redis)
#   CACHE_TYPE: RedisCache
#   CACHE_REDIS_HOST: redis server address (plain ip as str, no port)
#   CACHE_REDIS_PORT: redis server port, default is 6379
#   CACHE_REDIS_PASSWORD: redis server password
USE_CACHE = True
if USE_CACHE:
    if IS_PROD:
        CACHE_CONFIG = {
            'CACHE_TYPE': 'RedisCache',
            'CACHE_REDIS_HOST': environ.get('CACHE_REDIS_HOST'),
            'CACHE_DEFAULT_TIMEOUT': 0,
        }
    else:
        CACHE_CONFIG = {
            'CACHE_TYPE': 'SimpleCache',
            'CACHE_DEFAULT_TIMEOUT': 0,
        }
else:
    CACHE_CONFIG = None

