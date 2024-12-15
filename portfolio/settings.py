"""
Django settings for portfolio project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url 
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','127.0.0.1','portfolio-1-q4md.onrender.com','www.benserya.dev']
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ALLOWED TRANS LANGS
# <option value="?lang=ar" {% if request.GET.lang|default:'en' == 'ar' %}selected{% endif %} class="bg-[#0f172a] lateef-bold">ض</option>
#         <option value="?lang=ber" {% if request.GET.lang|default:'en' == 'ber' %}selected{% endif %} class="bg-[#0f172a]">ⵣ</option>
#         <option value="?lang=en" {% if request.GET.lang|default:'en' == 'en' %}selected{% endif %} class="bg-[#0f172a]">EN</option>
#         <option value="?lang=fr" {% if request.GET.lang|default:'en' == 'fr' %}selected{% endif %} class="bg-[#0f172a]">FR</option>
#         <option value="?lang=de" {% if request.GET.lang|default:'en' == 'de' %}selected{% endif %} class="bg-[#0f172a]">DE</option>
#         <option value="?lang=es" {% if request.GET.lang|default:'en' == 'es' %}selected{% endif %} class="bg-[#0f172a]">ES</option>
#         <option value="?lang=it" {% if request.GET.lang|default:'en' == 'it' %}selected{% endif %} class="bg-[#0f172a]">IT</option>
#         <option value="?lang=zh" {% if request.GET.lang|default:'en' == 'zh' %}selected{% endif %} class="bg-[#0f172a]">中文</option>
#         <option value="?lang=hi" {% if request.GET.lang|default:'en' == 'hi' %}selected{% endif %} class="bg-[#0f172a]">हिंदी</option>
#         <option value="?lang=ja" {% if request.GET.lang|default:'en' == 'ja' %}selected{% endif %} class="bg-[#0f172a]">日本語</option>
#         <option value="?lang=ko" {% if request.GET.lang|default:'en' == 'ko' %}selected{% endif %} class="bg-[#0f172a]">한국어</option>
#         <option value="?lang=pt" {% if request.GET.lang|default:'en' == 'pt' %}selected{% endif %} class="bg-[#0f172a]">PT</option>
#         <option value="?lang=ru" {% if request.GET.lang|default:'en' == 'ru' %}selected{% endif %} class="bg-[#0f172a]">RU</option>

ALLOWED_LANGS =[{ 'code':'ar','name':'ض'},
                { 'code':'ber','name':'ⵣ'},
                { 'code':'en','name':'EN'},
                { 'code':'fr','name':'FR'},
                { 'code':'de','name':'DE'},
                { 'code':'es','name':'ES'},
                { 'code':'it','name':'IT'},
                { 'code':'zh','name':'中文'},
                { 'code':'hi','name':'हिंदी'},
                { 'code':'ja','name':'日本語'},
                { 'code':'ko','name':'한국어'},
                { 'code':'pt','name':'PT'},
                { 'code':'ru','name':'RU'}
                ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'app'

]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',

]
CORS_ALLOW_ALL_ORIGINS = True  # Note: Allowing all origins is not recommended for production

ROOT_URLCONF = 'portfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'portfolio.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# settings.py additions
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Or your email provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')  # Use app password for Gmail


# settings.py

# Root URL Configuration
# ROOT_URLCONF = 'portfolio.urls'

# # WSGI Application Path
# WSGI_APPLICATION = 'portfolio.wsgi.application'

# # ASGI Application Path (for async support)
# ASGI_APPLICATION = 'portfolio.asgi.application'
