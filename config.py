from pathlib import Path
from dotenv import load_dotenv
from os import environ

# Browser tab title
PROJECT_TITLE = 'Phidash'

# Title and subtitle to display on navbar
NAV_TITLE = 'PhiDash'
NAV_SUBTITLE = 'A multipage Dash project template'


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
    'TEST_DF_2': BASE_STORAGE_PATH / 'dataframes/test_data_df.p'
}


# Same idea, but for markdown documents. Only paths as values, no tuples with doc.
# Temporary feature until i come up with something better
MARKDOWNS_DICT = {
    'test_md': BASE_STORAGE_PATH / 'markdowns/test_md.md'
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

