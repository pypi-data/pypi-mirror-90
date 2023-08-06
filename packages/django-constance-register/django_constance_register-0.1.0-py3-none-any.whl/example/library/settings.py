import os
from datetime import date
from constance_register.conf import conf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_ID = 1

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hdx64#m+lnc_0ffoyehbk&7gk1&*9uar$pcfcm-%$km#p0$k=6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'library.apps.shelf',
    'library.apps.staff',
    'constance',
    'constance.backends.database',
    'constance_register',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'library.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'library.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/db.db',
    }
}

CONSTANCE_REDIS_CONNECTION = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}

CONSTANCE_ADDITIONAL_FIELDS = {
    'yes_no_null_select': [
        'django.forms.fields.ChoiceField',
        {
            'widget': 'django.forms.Select',
            'choices': ((None, "-----"), ("yes", "Yes"), ("no", "No"))
        }
    ],
    'email': ('django.forms.fields.EmailField',),
}
AUTH_USER_MODEL = 'staff.StaffUser'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
CONSTANCE_DATABASE_CACHE_BACKEND = 'default'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL)

CONSTANCE_REGISTRY = [
    'library.apps.shelf.config',
    'library.apps.staff.config'
]
conf.load()

CONSTANCE_CONFIG = {
    **conf.settings()
}
CONSTANCE_CONFIG_FIELDSETS = {
    **conf.fieldsets()
}
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
