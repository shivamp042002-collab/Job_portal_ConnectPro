from .base import *
import pymysql
pymysql.install_as_MySQLdb()

DEBUG = False

# Security settings
SECURE_BROWSER_XSS_FILTER      = True
SECURE_CONTENT_TYPE_NOSNIFF    = True
SECURE_HSTS_SECONDS            = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD            = True
SECURE_SSL_REDIRECT            = False   # Set True after HTTPS is configured
SESSION_COOKIE_SECURE          = False   # Set True after HTTPS
CSRF_COOKIE_SECURE             = False   # Set True after HTTPS
X_FRAME_OPTIONS                = 'DENY'

# CORS
CORS_ALLOWED_ORIGINS = [
    f"http://{config('EC2_IP', default='localhost')}",
    "https://yourdomain.com",
]
CORS_ALLOW_CREDENTIALS = True

# Static files served by Nginx
STATIC_ROOT = '/home/ubuntu/connectpro/staticfiles/'
MEDIA_ROOT  = '/home/ubuntu/connectpro/media/'

# Cache
CACHES = {
    'default': {
        'BACKEND':  'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'connectpro-cache',
    }
}