# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

import logging
import re

logger = logging.getLogger(__name__)


def log(view_func):
    '''
    Logs all requests
    '''
    def _decorated(request, *args, **kwargs):

        post_data = request.body
        post_data = re.sub(r'password=(.*?)&', 'password=****&', post_data)
        logger.debug(u'Start of the request[%s] for URL[%s] with DATA[%s].' % (request.method, request.path, post_data))

        return view_func(request, *args, **kwargs)

    return _decorated
