from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h0z+fvd(311nzbltl!d8#qio9e)hezo9j736@)688iq(7xh#ej'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

try:
    from .local import *
except ImportError:
    pass
