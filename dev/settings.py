import os
import yaml
from urllib.parse import urlparse

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


ENV_YAML = None
with open(os.path.join(BASE_DIR, 'env.yaml'), 'r') as stream:
	ENV_YAML = yaml.load(stream, Loader=yaml.Loader)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV_YAML['SECRETKEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV_YAML['DEBUG']

FRONTEND_HOST = urlparse(ENV_YAML['FRONTENDURL']).hostname
BACKEND_HOST = urlparse(ENV_YAML['BACKENDURL']).hostname
ALLOWED_HOSTS = []
if FRONTEND_HOST not in ALLOWED_HOSTS:
	ALLOWED_HOSTS.append(FRONTEND_HOST)
if BACKEND_HOST not in ALLOWED_HOSTS:
	ALLOWED_HOSTS.append(BACKEND_HOST)


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'corsheaders',
	'rest_framework',
	'api.apps.ApiConfig',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dev.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [],
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

WSGI_APPLICATION = 'dev.wsgi.application'

# REST CONFIGS
REST_FRAMEWORK = {
	'DEFAULT_RENDERER_CLASSES': (
		'rest_framework.renderers.JSONRenderer',
		# 'rest_framework.renderers.BrowsableAPIRenderer',
	),
	'DEFAULT_PARSER_CLASSES': (
		'rest_framework.parsers.JSONParser',
	),
}

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': ENV_YAML['DBNAME'],
		'USER': ENV_YAML['DBUSER'],
		'PASSWORD': ENV_YAML['DBPASS'],
		'HOST': ENV_YAML['DBHOST'],
		'PORT': ENV_YAML['DBPORT']
	}
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': (
			'django.contrib.auth.password_validation'
			+ 'UserAttributeSimilarityValidator'
		),
	},
	{
		'NAME': (
			'django.contrib.auth.password_validation.MinimumLengthValidator'
		),
	},
	{
		'NAME': (
			'django.contrib.auth.password_validation.CommonPasswordValidator'
		),
	},
	{
		'NAME': (
			'django.contrib.auth.password_validation.NumericPasswordValidator'
		),
	},
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# CORS
CSRF_TRUSTED_ORIGINS = (
	tuple(ALLOWED_HOSTS)
)

# CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
	tuple(ALLOWED_HOSTS)
)

CORS_ALLOW_CREDENTIALS = True
