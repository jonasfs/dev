import json
import os
from urllib.parse import urlparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = BASE_DIR + '/env.json'
aws = {}

with open(path, 'r') as stream:
	aws = json.load(stream)

SECRET_KEY = aws['SECRETKEY']
DEBUG = False
ALLOWED_HOSTS = []
ALLOWED_HOSTS.append('127.0.0.1')
try:
	ALLOWED_HOSTS.append(urlparse(aws['FRONTENDURL']).hostname)
except (KeyError, AttributeError) as e:
	pass

try:
	ALLOWED_HOSTS.append(urlparse(aws['BACKENDURL']).hostname)
except (KeyError, AttributeError) as e:
	pass


DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': aws['DBNAME'],
		'USER': aws['DBUSER'],
		'PASSWORD': aws['DBPASS'],
		'HOST': aws['DBHOST'],
		'PORT': 5432,
	}
}
