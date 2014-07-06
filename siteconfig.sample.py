
# Email addresses of people to notify in case of 5XX errors
ADMINS = ['admin@example.com']

# Set to `True` to enable tracebacks in HTML, turn off email error
# reports and turn on test endpoints (/all and /error)
# This should be `False` on a production server
DEBUG = False

# Mail server settings
#-----------------------------------------------------------------

# Set to `True` to use send emails via the local mail server
USE_LOCAL_MAIL = False

# The details of the remote mail server to use
# Fill these in if `USE_LOCAL_MAIL` is `False`
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'email@gmail.com'
MAIL_PASSWORD = 'Y0uRCl3VeRp455W0rD'

# The maximum size of the icon cache
# Note: this is not used by the application itself, but the
# cache management script `extra/purge_cache.py`.

# MAX_CACHE_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_CACHE_SIZE = 0  # Will cause an error! You must configure this!

# Allow users to specify icon size via the API
# If `False`, `SIZE` configured in `config.py` or in this module
# will be used regardless of what the user specifies
API_ALLOW_SIZE = True
