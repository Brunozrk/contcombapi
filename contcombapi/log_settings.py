# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

import os
LOG_LEVEL = 'INFO'
LOG_SHOW_SQL = False

ROOTDIR = os.path.realpath(os.path.dirname(__file__))
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
     'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'mail_admins': {
            'level': LOG_LEVEL,
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'logger': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': ROOTDIR + "/logs/loggerfile",
            'backupCount': 2,
            'formatter': 'standard',
        },
         'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['logger' if LOG_SHOW_SQL else 'null'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'authentication': {
            'handlers': ['logger'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'user': {
            'handlers': ['logger'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
    }
}
