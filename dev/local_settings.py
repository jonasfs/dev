import json
import os
import sys
from urllib.parse import urlparse
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
aws = {}
try:
    path = Path(BASE_DIR + '/env.json')

    with open(path, 'r') as stream:
            aws = json.load(stream)
except FileNotFoundError:
    pass


try:
    SECRET_KEY = aws['SECRETKEY']
except KeyError:
    SECRET_KEY = None
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


try:
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
except KeyError:
    DATABASES = None
