from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------
# SECURITY
# ----------------------------
SECRET_KEY = 'django-insecure-=@ric781vq_skkfjw*n8g$ts=ah)(owx$$ctyovurp&+qkyaw='
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# ----------------------------
# INSTALLED APPS
# ----------------------------
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your custom apps
    'accounts',
    'cart',
    'products',
    'orders',
    'reviews',
    'wishlist',

    # Third-party apps
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',

    # Allauth (for normal + social login)
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Social providers
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
]

SITE_ID = 1

# ----------------------------
# MIDDLEWARE
# ----------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # ✅ CORS middleware must come before CommonMiddleware
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # ✅ Needed for django-allauth
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'ecommerce.urls'

# ----------------------------
# TEMPLATES
# ----------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Add your templates directory if needed
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

WSGI_APPLICATION = 'ecommerce.wsgi.application'

# ----------------------------
# DATABASE
# ----------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ----------------------------
# PASSWORD VALIDATION
# ----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ----------------------------
# INTERNATIONALIZATION
# ----------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'  # ✅ better for Indian timezone
USE_I18N = True
USE_TZ = True

# ----------------------------
# STATIC & MEDIA
# ----------------------------
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ----------------------------
# ✅ REST FRAMEWORK SETTINGS
# ----------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}

# ----------------------------
# ✅ SIMPLE JWT CONFIG
# ----------------------------
SIMPLE_JWT = {
   'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ----------------------------
# ✅ CORS SETTINGS
# ----------------------------
CORS_ALLOW_ALL_ORIGINS = False  # ❌ Not recommended to keep True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# ----------------------------
# ✅ CSRF TRUSTED ORIGINS
# ----------------------------
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:3000",
]

# ----------------------------
# ✅ RAZORPAY KEYS (Test mode)
# ----------------------------
RAZORPAY_KEY_ID = "rzp_test_1234567890abcdef"
RAZORPAY_KEY_SECRET = "your_test_secret_key_here"

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # your Gmail address
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # App password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER