"""
Django settings for koodaram project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = 'your-secret-key-here'  # Replace with actual secret key
DEBUG = False

ALLOWED_HOSTS = [
    "your-domain-or-ip-here",
]

# APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'koodaram_app',
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'koodaram.urls'

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'koodaram_app.context_processors.google_reviews',
            ],
        },
    },
]

WSGI_APPLICATION = 'koodaram.wsgi.application'

# DATABASE (SQLite for now)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# INTERNATIONAL
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# STATIC FILES
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# MEDIA FILES
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # Replace with actual email
EMAIL_HOST_PASSWORD = 'your-app-password'  # Replace with actual app password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# GOOGLE REVIEWS
GOOGLE_REVIEW_RATING = 4.7
GOOGLE_REVIEW_COUNT = 900
GOOGLE_REVIEW_URL = "https://www.google.com/travel/search?q=Koodaram%20camping%20reviews"

# RECAPTCHA
RECAPTCHA_SITE_KEY = 'your-recaptcha-site-key'  # Replace with actual site key
RECAPTCHA_SECRET_KEY = 'your-recaptcha-secret-key'  # Replace with actual secret key

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'