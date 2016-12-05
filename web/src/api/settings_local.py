"""
Django settings local for api project.
Used for developer debugging
"""

from settings import *

DEBUG = True

DATABASES = {
    'default': {
        'NAME': 'task_tracker',
        'ENGINE': config.get('databases', 'ENGINE'),
        'USER': 'admin',
        'PASSWORD': 'p@ssword',
        'HOST': 'localhost',
        'PORT': config.get('databases', 'port'),
    }
}
