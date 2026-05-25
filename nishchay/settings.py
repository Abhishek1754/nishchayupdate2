"""
Django settings for nishchay project.
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

SECRET_KEY = 'django-insecure-b83uho$bx8v0-4oh4!83y4=tlbq#&++0&c(wlh9e(=1k)#q4ti'

DEBUG = True

ALLOWED_HOSTS = [

    '*',

]


# =====================================================
# INSTALLED APPS
# =====================================================

INSTALLED_APPS = [

    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # THIRD PARTY

    'rest_framework',

    'rest_framework_simplejwt',

    'corsheaders',

    'django_filters',

    'channels',

    # PROJECT APPS

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

TIME_ZONE = 'UTC'

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

    'DEFAULT_FILTER_BACKENDS': (

        'django_filters.rest_framework.DjangoFilterBackend',

    ),

}


# =====================================================
# CHANNELS + REDIS
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

CORS_ALLOW_ALL_ORIGINS = True


# =====================================================
# CSRF TRUSTED ORIGINS
# =====================================================

CSRF_TRUSTED_ORIGINS = [

    'http://127.0.0.1:8000',

    'http://localhost:8000',

]


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