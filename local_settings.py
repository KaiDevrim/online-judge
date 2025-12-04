"""
DMOJ local_settings.py for Docker deployment
"""
import os
from datetime import timedelta

# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'CHANGE-THIS-SECRET-KEY-IN-PRODUCTION')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE', 'dmoj'),
        'USER': os.environ.get('MYSQL_USER', 'dmoj'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD', ''),
        'HOST': os.environ.get('MYSQL_HOST', 'db'),
        'PORT': os.environ.get('MYSQL_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'sql_mode': 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION',
        },
    }
}

# Redis cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{os.environ.get("REDIS_HOST", "redis")}:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Celery
CELERY_BROKER_URL = f'redis://{os.environ.get("REDIS_HOST", "redis")}:6379/0'
CELERY_RESULT_BACKEND = f'redis://{os.environ.get("REDIS_HOST", "redis")}:6379/0'

# Internationalization
LANGUAGE_CODE = 'en-ca'
DEFAULT_USER_TIME_ZONE = 'America/Toronto'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_ROOT = '/site/static_root'
STATIC_URL = '/static/'
MEDIA_ROOT = '/site/media'
MEDIA_URL = '/media/'

# django-compressor
COMPRESS_OUTPUT_DIR = 'cache'
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']
COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'
STATICFILES_FINDERS += ('compressor.finders.CompressorFinder',)

# Email (console for now)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ADMINS = [('Admin', os.environ.get('ADMIN_EMAIL', 'admin@example.com'))]
SERVER_EMAIL = 'DMOJ <noreply@dmoj.ca>'

# DMOJ settings
SITE_NAME = os.environ.get('SITE_NAME', 'DMOJ')
SITE_LONG_NAME = os.environ.get('SITE_LONG_NAME', 'DMOJ: Modern Online Judge')
SITE_ADMIN_EMAIL = os.environ.get('SITE_ADMIN_EMAIL', 'admin@example.com')

# Bridge
BRIDGED_JUDGE_ADDRESS = [('0.0.0.0', 9999)]
BRIDGED_DJANGO_ADDRESS = [('0.0.0.0', 9998)]

# Features
ENABLE_FTS = True
BAD_MAIL_PROVIDERS = set()

# Event server
EVENT_DAEMON_USE = True
EVENT_DAEMON_POST = 'ws://wsevent:15101/'
EVENT_DAEMON_GET = 'ws://wsevent:15100/'
EVENT_DAEMON_POLL = '/channels/'

# PDF generation - Disabled
USE_SELENIUM = False
DMOJ_PDF_PROBLEM_CACHE = '/site/pdfcache'

# Problem data
DMOJ_PROBLEM_DATA_ROOT = '/problems'

# User data download
DMOJ_USER_DATA_DOWNLOAD = True
DMOJ_USER_DATA_CACHE = '/site/datacache'
DMOJ_USER_DATA_INTERNAL = '/datacache'
DMOJ_USER_DATA_DOWNLOAD_RATELIMIT = timedelta(days=1)

# Math/TeX rendering - Disabled for now
# MATHOID_URL = 'http://mathoid:10044'
# TEXOID_URL = 'http://texoid:8888'

# CDN
ACE_URL = '//cdnjs.cloudflare.com/ajax/libs/ace/1.2.3/'
JQUERY_JS = '//cdnjs.cloudflare.com/ajax/libs/jquery/2.2.4/jquery.min.js'
SELECT2_JS_URL = '//cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/js/select2.min.js'
SELECT2_CSS_URL = '//cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/css/select2.min.css'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'judge.bridge': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
