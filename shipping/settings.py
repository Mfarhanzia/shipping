"""
Django settings for shipping project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import django_heroku
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k6(ca(d8=zwo5l*3)8dwj8u+nsa8-@cucv_7ew4q26-xq-u2cx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

if DEBUG == False:
    SECURE_SSL_REDIRECT = False
# SECURE_SSL_REDIRECT = True

ALLOWED_HOSTS = ['www.boltonblock.com', '*.boltonblock.com', 'boltonblock.com',
        'www.boltonblocks.com', '*.boltonblocks.com', 'boltonblocks.com', 'www.boltonbloks.com', 'boltonbloks.com',
                 '*.boltonbloks.com']

# Application definition
INSTALLED_APPS = [
    'phonenumber_field',
    'multiselectfield',
    'users',
    'order',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third-party
    'formtools',
    'crispy_forms',  # render forms as bootstrap easily
    'django.contrib.humanize',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shipping.urls'

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
                'users.context_processor.email_form'
            ],
        },
    },
]

WSGI_APPLICATION = 'shipping.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
#         'NAME': 'shipping',
#         'USER': 'root',
#         'PASSWORD': '',
#         'PORT': '3306',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'login'

# django-phonenumber
PHONENUMBER_DEFAULT_REGION = 'US'
# PHONENUMBER_DB_FORMAT = 'NATIONAL'

ENCRYPT_KEY = b'v4iU9uh5AAeU1H5cTPqWSq7JAA2ui0G29UK5uMhe8Fg='
AUTH_USER_MODEL = 'users.User'
CART_SESSION_ID = 'order'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# email credential
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "info@boltonbloks.com"
EMAIL_HOST_PASSWORD = "boltondev1PW" 
DEFAULT_FROM_EMAIL = "info@boltonbloks.com"
# DEFAULT_FROM_EMAIL = "farhan71727@gmail.com"

# Activate Django heroku
django_heroku.settings(locals())