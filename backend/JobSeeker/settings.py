import os
from pathlib import Path
from decouple import config
import dj_database_url


AUTH_USER_MODEL = 'Accounts.CustomUser'

ACCOUNT_USER_MODEL_USERNAME_FIELD = None    
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default="dev-secret-docker-build-key")

DEBUG = config("DEBUG", default=False, cast=bool)

#ALLOWED_HOSTS — FINAL (Fixes OTP + Cookie Issues)
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".onrender.com",
    "arakkhajobconnect-backend.onrender.com",
    "job.arakkha.tech",
]

#Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "Jobs.apps.JobsConfig",
    "anymail",

    # custom
    'Accounts',
    'Application',
    'EmployerProfile',
    'JobSeekerProfile',
    'Notification',
    'UI',
    'legal',

    # allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",

    # third-party
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    "django_extensions",
    'ckeditor',
]

# Middleware
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'JobSeeker.middleware.RateLimitMiddleware',
]

ROOT_URLCONF = 'JobSeeker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

TEMPLATES[0]["OPTIONS"]["context_processors"] += [
    "django.template.context_processors.request",
]

WSGI_APPLICATION = 'JobSeeker.wsgi.application'

# Database (SQLite local)
# Database (SQLite local)
if DEBUG:
    # Local development (SQLite)

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

else:
    # Production (MySQL on Hostinger)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('MYSQL_DB'),
            'USER': os.getenv('MYSQL_USER'),
            'PASSWORD': os.getenv('MYSQL_PASS'),
            'HOST': os.getenv('MYSQL_HOST'),
            'PORT': os.getenv('MYSQL_PORT'),
            'OPTIONS': {
                'ssl': {'ca': os.path.join(BASE_DIR, 'ca.pem')}
            }
        }
    }


TIME_ZONE = "Asia/Yangon"
USE_TZ = True

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
USE_I18N = True

# STATIC FILES – Render Compatible
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "JobSeeker" / "static"]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email Settings
MAILERSEND_API_TOKEN = config("MAILERSEND_API_TOKEN", default="dummy-mailersend-token")

ANYMAIL = {
    "MAILERSEND_API_TOKEN": MAILERSEND_API_TOKEN,
}

EMAIL_BACKEND = "anymail.backends.mailersend.EmailBackend"

DEFAULT_FROM_EMAIL = config("MAILERSEND_FROM_EMAIL", default="dummy@example.com")
MAILERSEND_FROM_NAME = config("MAILERSEND_FROM_NAME", default="Arakkha Job Connect")




SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID', "dummy-google-client"),
            'secret':   os.getenv('GOOGLE_SECRET', "dummy-google-secret"),
            'key': ''
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online', 'prompt': 'select_account'}
    }
}


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "otp": "5/minute",
    },
}

TOKEN_MODEL = None

#CORS – FINAL FIX (Only allow frontend domain)
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://192.168.130.155:5173",
    
    # Frontend
    "https://arakkhajobconnect-1.onrender.com",

    # Backend
    "https://arakkhajobconnect.onrender.com",

    "https://job.arakkha.tech",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://192.168.130.155:5173",

    "https://job.arakkha.tech",
    "https://www.job.arakkha.tech",

    "https://arakkhajobconnect-1.onrender.com",
    "https://arakkhajobconnect.onrender.com",
]

#  Cookie settings for OTP & Login
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# IMPORTANT FIX
SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"


# Media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
