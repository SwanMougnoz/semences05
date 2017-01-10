from semences05.settings.common import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'semences05',
        'USER': 'semences05',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

MAILS = {
    'noreply': 'mougnoz.swan@gmail.com'
}
