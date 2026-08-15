import os, environ
from pathlib import Path

from scaffold.appsConfig import getAppNames

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Uses environ to interface with environment variables
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env() 

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')
# allowed urls
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')
# for debug toolbar
INTERNAL_IPS = env.list('INTERNAL_IPS', default=['127.0.0.1'])
# CORS: Requires django-cors-headers
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOWED_ORIGINS = []
else:
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])

# for railway
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize', # Required for allauth MFA templates

    'django.forms',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.mfa', # Enables 2FA and Passkeys
    "storages",
    "django_htmx",
    "django_extensions",
    "django_cotton",
    "django_cotton_ui",
    "debug_toolbar",
    'django_filters',
    "django_tables2",
]

APPS = getAppNames()
INSTALLED_APPS += APPS

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'scaffold.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'scaffold.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": env.db(default="sqlite:///db.sqlite3")
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Kampala'
USE_I18N = True
USE_TZ = True


AUTH_USER_MODEL = "accounts.User"

# --- ALLAUTH & CUSTOM USER CONFIGURATION ---
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username' # Model has the field, but it's optional
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_LOGIN_METHODS = {'email'}  # Enforce Email-only login
ACCOUNT_EMAIL_VERIFICATION = 'none' # Options: 'mandatory', 'optional', 'none'

# --- MFA & PASSKEY CONFIGURATION ---
MFA_SUPPORTED_TYPES = ["totp", "webauthn", "recovery_codes"]
MFA_PASSKEY_LOGIN_ENABLED = True  # Allows passwordless login via WebAuthn Autofill / Button

MFA_WEBAUTHN_ALLOW_INSECURE_ORIGIN = True # Only if testing on HTTP non-localhost IPs

MFA_WEBAUTHN_RP_ID = "localhost"

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_AGE = 24 * 60 * 60


# email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT")

EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")

EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/dist/'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static/staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

USE_AZURE = env.bool('USE_AZURE')
if USE_AZURE:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.azure_storage.AzureStorage",
            "OPTIONS": {
                "connection_string": env("AZURE_CONNECTION_STRING"),
                "account_name": env("AZURE_ACCOUNT_NAME"),
                "account_key": env("AZURE_ACCOUNT_KEY"),
                "azure_container": env("AZURE_MEDIA_CONTAINER"),
                "expiration_secs": int(env("AZURE_URL_EXPIRATION_SECS")),
                "overwrite_files": True,
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.azure_storage.AzureStorage",
            "OPTIONS": {
                "connection_string": env("AZURE_CONNECTION_STRING"),
                "account_name": env("AZURE_ACCOUNT_NAME"),
                "account_key": env("AZURE_ACCOUNT_KEY"),
                "azure_container": env("AZURE_STATIC_CONTAINER"),
            },
        },
    }
else:
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
    }
