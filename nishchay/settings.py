"""
Production Ready Django Settings for Nishchay
"""

from pathlib import Path
import os


# =====================================================
# BASE DIRECTORY
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =====================================================
# SECURITY
# =====================================================

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "change-this-secret-key-in-production"
)

DEBUG = False

ALLOWED_HOSTS = [
    "nishchay.in",
    "www.nishchay.in",
    "98.85.228.253",
    "localhost",
    "127.0.0.1",
]


# =====================================================
# INSTALLED APPS
# =====================================================

INSTALLED_APPS = [

    # =================================================
    # ADMIN UI
    # =================================================

    'jazzmin',

    # =================================================
    # DJANGO APPS
    # =================================================

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # =================================================
    # THIRD PARTY APPS
    # =================================================

    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'channels',

    # =================================================
    # PROJECT APPS
    # =================================================

    'accounts.apps.AccountsConfig',
    'subscription.apps.SubscriptionConfig',
    'wallet.apps.WalletConfig',
    'roi.apps.RoiConfig',
    'ecommerce.apps.EcommerceConfig',
    'recharge.apps.RechargeConfig',
    'astrology.apps.AstrologyConfig',
    'career.apps.CareerConfig',
    'food_delivery',
    'referral',
    'ai_karma',

]


# =====================================================
# CUSTOM USER MODEL
# =====================================================

AUTH_USER_MODEL = 'accounts.User'


# =====================================================
# MIDDLEWARE
# =====================================================

MIDDLEWARE = [

    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]


# =====================================================
# ROOT URL
# =====================================================

ROOT_URLCONF = 'nishchay.urls'


# =====================================================
# TEMPLATES
# =====================================================

TEMPLATES = [

    {

        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [

            os.path.join(BASE_DIR, 'templates')

        ],

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


# =====================================================
# WSGI / ASGI
# =====================================================

WSGI_APPLICATION = 'nishchay.wsgi.application'

ASGI_APPLICATION = 'nishchay.asgi.application'


# =====================================================
# DATABASE
# =====================================================

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.sqlite3',

        'NAME': BASE_DIR / 'db.sqlite3',

    }

}


# =====================================================
# PASSWORD VALIDATION
# =====================================================

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


# =====================================================
# INTERNATIONALIZATION
# =====================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# =====================================================
# STATIC FILES
# =====================================================

STATIC_URL = '/static/'

STATICFILES_DIRS = [

    os.path.join(BASE_DIR, 'static'),

]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)

WHITENOISE_USE_FINDERS = True


# =====================================================
# MEDIA FILES
# =====================================================

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# =====================================================
# DEFAULT AUTO FIELD
# =====================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =====================================================
# DJANGO REST FRAMEWORK
# =====================================================

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ),

    'DEFAULT_PERMISSION_CLASSES': (

        'rest_framework.permissions.IsAuthenticated',

    ),

    'DEFAULT_FILTER_BACKENDS': (

        'django_filters.rest_framework.DjangoFilterBackend',

    ),

}


# =====================================================
# CHANNEL LAYERS
# =====================================================

CHANNEL_LAYERS = {

    "default": {

        "BACKEND": "channels_redis.core.RedisChannelLayer",

        "CONFIG": {

            "hosts": [("127.0.0.1", 6379)],

        },

    },

}


# =====================================================
# CORS SETTINGS
# =====================================================

CORS_ALLOWED_ORIGINS = [

    "http://nishchay.in",

    "https://nishchay.in",

    "http://www.nishchay.in",

    "https://www.nishchay.in",

]


# =====================================================
# CSRF TRUSTED ORIGINS
# =====================================================

CSRF_TRUSTED_ORIGINS = [

    "https://nishchay.in",

    "https://www.nishchay.in",

]


# =====================================================
# SECURITY HEADERS
# =====================================================

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = 'DENY'

SECURE_SSL_REDIRECT = False

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True


# =====================================================
# SESSION SECURITY
# =====================================================

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_COOKIE_AGE = 86400


# =====================================================
# LOGGING
# =====================================================

LOGGING = {

    'version': 1,

    'disable_existing_loggers': False,

}


# =====================================================
# JAZZMIN SETTINGS
# =====================================================

JAZZMIN_SETTINGS = {

    "site_title": "Nishchay Admin",

    "site_header": "Nishchay Control Panel",

    "site_brand": "Nishchay",

    "welcome_sign": "Welcome to Nishchay Dashboard",

    "show_sidebar": True,

    "navigation_expanded": True,

    "icons": {

        "accounts.User": "fas fa-users",

        "ecommerce.Product": "fas fa-box",

        "roi.ROIPlan": "fas fa-chart-line",

        "subscription.SubscriptionPlan": "fas fa-credit-card",

        "recharge.Recharge": "fas fa-mobile-alt",

        "astrology.Astrologer": "fas fa-star",

        "career.Job": "fas fa-briefcase",

    },

}


# =====================================================
# CACHE
# =====================================================

CACHES = {

    "default": {

        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",

    }

}


# =====================================================
# EMAIL CONFIGURATION
# =====================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")


# =====================================================
# FILE UPLOAD LIMITS
# =====================================================

DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760

FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760