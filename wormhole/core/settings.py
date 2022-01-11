from os import environ

from dotenv import dotenv_values

config = {**dotenv_values(".env"), **environ}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config["DEBUG"]

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = ["wormhole.core"]

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

ROOT_URLCONF = "wormhole.core.urls"

WSGI_APPLICATION = "wormhole.core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": config["MYSQL_HOST"],
        "PORT": config["MYSQL_PORT"],
        "USER": config["MYSQL_USER"],
        "PASSWORD": config["MYSQL_PASSWORD"],
        "NAME": config["MYSQL_DB"],
        "OPTIONS": {
            "charset": "utf8",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

BASE_URL = config["BASE_URL"]
