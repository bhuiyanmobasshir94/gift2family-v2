import dj_database_url
"""
Django settings for graahoshop project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
# import environ
import oscar
from oscar.defaults import *
from decimal import Decimal as D

# env = environ.Env()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

location = lambda x: os.path.join(
os.path.dirname(os.path.realpath(__file__)), x)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'r3ba0g-ijf^l@y62as5x@c8uqnw*(p0ass^4g4yflqoh%31#r!'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = env.bool('DEBUG', default=True)
# DEBUG = True

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'r3ba0g-ijf^l@y62as5x@c8uqnw*(p0ass^4g4yflqoh%31#r!')
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

ALLOWED_HOSTS = ['*']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Application definition
from oscar import get_core_apps

AUTH_USER_MODEL = "user.User"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'widget_tweaks',
    'paypal',
    'oscar_accounts',
    'apps.user',
] + get_core_apps(['apps.shipping', 'apps.checkout'])

SITE_ID = 1
gettext_noop = lambda s: s
LANGUAGES = (
    ('ar', gettext_noop('Arabic')),
    ('ca', gettext_noop('Catalan')),
    ('cs', gettext_noop('Czech')),
    ('da', gettext_noop('Danish')),
    ('de', gettext_noop('German')),
    ('en-gb', gettext_noop('British English')),
    ('el', gettext_noop('Greek')),
    ('es', gettext_noop('Spanish')),
    ('fi', gettext_noop('Finnish')),
    ('fr', gettext_noop('French')),
    ('it', gettext_noop('Italian')),
    ('ko', gettext_noop('Korean')),
    ('nl', gettext_noop('Dutch')),
    ('pl', gettext_noop('Polish')),
    ('pt', gettext_noop('Portuguese')),
    ('pt-br', gettext_noop('Brazilian Portuguese')),
    ('ro', gettext_noop('Romanian')),
    ('ru', gettext_noop('Russian')),
    ('sk', gettext_noop('Slovak')),
    ('uk', gettext_noop('Ukrainian')),
    ('zh-cn', gettext_noop('Simplified Chinese')),
)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'graahoshop.urls'
from oscar import OSCAR_MAIN_TEMPLATE_DIR
from oscar_accounts import TEMPLATE_DIR as ACCOUNTS_TEMPLATE_DIR
# location2 = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', x)
# print(location2('templates'))
# print(location('static'))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR,'templates'),
            OSCAR_MAIN_TEMPLATE_DIR,
            ACCOUNTS_TEMPLATE_DIR,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'graahoshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'ATOMIC_REQUESTS': True,
    }
}

ATOMIC_REQUESTS = True
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}
# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [
#     STATIC_DIR,
# ]
# STATIC_ROOT = location('static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
THUMBNAIL_DEBUG = True
THUMBNAIL_KEY_PREFIX = 'oscar-sandbox'
OSCAR_MISSING_IMAGE_URL = 'image_not_found.jpg'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

OSCAR_SHOP_NAME = 'Gift2Family'
OSCAR_SHOP_TAGLINE = 'A trusted e-commerce'

from django.utils.translation import ugettext_lazy as _

OSCAR_DASHBOARD_NAVIGATION[1]['children'].append({
    'label': _('Shipping'),
    'url_name': 'dashboard:shipping-method-list'
})

OSCAR_DASHBOARD_NAVIGATION.append(
    {
        'label': _('Agents'),
        'icon': 'icon-group',
        'children': [
            {
                'label': _('Agents'),
                'url_name': 'agents_dashboard:agents-list',
                'access_fn': lambda user, url_name, url_args, url_kwargs: user.is_staff,
            },
            {
                'label': _('Agent Requests'),
                'url_name': 'agents_dashboard:agent-request-view',
                'access_fn': lambda user, url_name, url_args, url_kwargs: user.is_staff,
            },
            {
                'label': _('Agent Interest Rate'),
                'url_name': 'agents_dashboard:agent-interest-rate',
                'access_fn': lambda user, url_name, url_args, url_kwargs: user.is_staff,
            },
        ]
    })

OSCAR_DASHBOARD_NAVIGATION.append(
    {
        'label': _('Admin'),
        'icon': 'icon-dashboard',
        'url_name': 'admin:login',
        'access_fn': lambda user, url_name, url_args, url_kwargs: user.is_staff,
    })

OSCAR_DASHBOARD_NAVIGATION.append(
    {
        'label': _('Accounts'),
        'icon': 'icon-globe',
        'children': [
            {
                'label': _('Accounts'),
                'url_name': 'accounts-list',
            },
            {
                'label': _('Transfers'),
                'url_name': 'transfers-list',
            },
            {
                'label': _('Deferred income report'),
                'url_name': 'report-deferred-income',
            },
            {
                'label': _('Profit/loss report'),
                'url_name': 'report-profit-loss',
            },
        ]
    })

OSCAR_DEFAULT_CURRENCY = 'USD'
ACCOUNTS_UNIT_NAME = 'Wallet'
ACCOUNTS_UNIT_NAME_PLURAL = 'Wallets'
ACCOUNTS_MIN_LOAD_VALUE = D('20.00')
ACCOUNTS_MAX_ACCOUNT_VALUE = D('5000.00')

# try:
#     from settings_local import *
# except ImportError:
#     pass


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'oscar.checkout': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'accounts': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'DEBUG',
        },
    }
}

ACCOUNTS_REDEMPTIONS_NAME = 'Redemptions'
ACCOUNTS_LAPSED_NAME = 'Lapsed accounts'
ACCOUNTS_BANK_NAME = 'Bank'
ACCOUNTS_UNPAID_SOURCES = 'Unpaid source'

# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_HSTS_SECONDS
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE =  True
# CSRF_COOKIE_SECURE = True
# X_FRAME_OPTIONS =  'DENY'


# Heroku: Update database configuration from $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

OSCAR_HOMEPAGE = '/catalogue/'

OSCAR_ACCOUNTS_DASHBOARD_ITEMS_PER_PAGE = 30
