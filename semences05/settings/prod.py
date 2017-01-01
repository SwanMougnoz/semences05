from semences05.settings.common import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'semences05',
        'USER': 'semences05',
        'PASSWORD': '<replace_password>',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
