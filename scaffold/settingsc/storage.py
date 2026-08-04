import os
from pathlib import Path
from .base import env

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATABASES = {
    "default": env.db(default="sqlite:///db.sqlite3")
}

if not DEBUG and USE_AZURE:
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

elif not DEBUG and not USE_AZURE:
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
    }

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_URL = 'static/'

