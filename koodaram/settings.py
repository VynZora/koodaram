"""
Django settings for koodaram project (LOCAL DEVELOPMENT).
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = 'your-secret-key-here'
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

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
    # WhiteNoise not needed for local
    # "whitenoise.middleware.WhiteNoiseMiddleware",
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
                'koodaram_app.context_processors.footer_packages',
            ],
        },
    },
]

WSGI_APPLICATION = 'koodaram.wsgi.application'

# DATABASE (SQLite for local)
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

# STATIC FILES (LOCAL)
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

# No STATIC_ROOT or WhiteNoise in local

# MEDIA FILES
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# EMAIL (print in console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# GOOGLE REVIEWS (dummy/local values)
GOOGLE_REVIEW_RATING = 4.7
GOOGLE_REVIEW_COUNT = 900
GOOGLE_REVIEW_URL = "https://www.google.com/travel/search?q=Koodaram%20camping%20reviews"

# RECAPTCHA (disable or use test keys)
RECAPTCHA_SITE_KEY = ''
RECAPTCHA_SECRET_KEY = ''

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'