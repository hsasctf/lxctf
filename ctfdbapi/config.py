# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

ADMIN_CREDENTIALS = ('admin', 'z1zIfR9UcQhJ0xlA')
API_SECRET = "rUCkG9QXSpsXj54FkXFFaZa4vBJtDgl2tHD1Hckg"


# Define the database - we are working with
# SQLite for this example
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')

# local
#SQLALCHEMY_DATABASE_URI = 'mysql://root:bang2gah7mae0wiegaekooleihe2yeecie8aNee2@localhost/ctf2'

#prod
#SQLALCHEMY_DATABASE_URI = 'mysql://ctf:jFOuTTlAfDgswD2r010SkEBT7iKfIwU7Z8jUN3Ya@10.38.1.2/ctf'
SQLALCHEMY_DATABASE_URI = 'mysql://ctf:tY61YwXoqXNInjBe1MVAi+z3iZt0NUYD7d9Npk2/oLk=@127.0.0.1/ctf'


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


SQLALCHEMY_ECHO = True


JSON_SORT_KEYS = False

TESTING = False # set to True FIXME
LOGIN_DISABLED = False


CTF_NAME = "HSAlbSigCTF"

API_BASE_URL = "http://127.0.0.1:5000/api/v01"  # without trailing slash
