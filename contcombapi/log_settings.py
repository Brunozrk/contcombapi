# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from django.conf import settings
LOG_LEVEL = 'INFO'
LOG_SHOW_SQL = False

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
            'filename': settings.BASE_DIR + "/logs/loggerfile",
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
        'contcombapi.decorator': {
            'handlers': ['logger'],
            'level': LOG_LEVEL,
            'propagate': True,
        }, 
        'contcombapi.db': {
            'handlers': ['logger'],
            'level': LOG_LEVEL,
            'propagate': True,
        }, 
        'contcombapi.authentication': {
            'handlers': ['logger'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'contcombapi.user': {
            'handlers': ['logger'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'contcombapi.contact': {
            'handlers': ['logger'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'contcombapi.vehicle': {
            'handlers': ['logger'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
    }
}
