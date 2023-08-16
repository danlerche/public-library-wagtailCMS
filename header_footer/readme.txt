Make sure sessions are enabled in your base.py file. For example:

SESSION_ENGINE = 'django.contrib.sessions.backends.file'

CACHES = {
'default': {
'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
}
}
SESSION_COOKIE_AGE = 7200
