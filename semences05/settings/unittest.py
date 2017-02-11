from semences05.settings.common import *

DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '::1']

COMPRESS_OFFLINE = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
