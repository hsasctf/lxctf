# Statement for enabling the development environment
import yaml

DEBUG = True

# Define the application directory
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
GLOBAL_CONFIG_PATH = os.path.join(BASE_PATH, "..", "inventories", "ctf_config.yml")
with open(GLOBAL_CONFIG_PATH, 'r') as stream:
    GLOBAL_CONFIG = yaml.safe_load(stream)


ADMIN_CREDENTIALS = ('admin', GLOBAL_CONFIG['dashboard_admin_password'])
API_SECRET = GLOBAL_CONFIG['api_secret']

SQLALCHEMY_DATABASE_URI = 'mysql://ctf:{}@127.0.0.1/ctf'.format(GLOBAL_CONFIG['db_ctf_password'])


DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = False

# Use a secure, unique and absolutely secret key for
# signing the data.
#CSRF_SESSION_KEY = "yOlod49ZuasFLDgila6Zv72XK9z0gWr9YCvceklKzfDkbM87zO"

# Secret key for signing cookies
SECRET_KEY = "ZBiSD2ZGPhbtFS52u3caUNgrZ8dv7CtS7q2E30e3"


SQLALCHEMY_ECHO = False
JSON_SORT_KEYS = False
TESTING = False # set to True FIXME
LOGIN_DISABLED = False


CTF_NAME = "HSAlbSigCTF"

API_BASE_URL = "http://127.0.0.1:5000/api/v01"  # without trailing slash
