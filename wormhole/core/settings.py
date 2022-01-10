# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure--7p@w^esv%0dz%ee57nve!h62q8xildjpav*4m-=iz!lx$sfvn"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
        "HOST": "localhost",
        "PORT": 3306,
        "USER": "",
        "PASSWORD": "",
        "NAME": "",
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

BASE_URL = "wormhole.com"
