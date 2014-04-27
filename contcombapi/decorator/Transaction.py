# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from django.db import transaction
import logging
import re

logger = logging.getLogger(__name__)


def commit_or_rollback(view_func):
    '''
    Commit or Rollback
    '''
    def _decorated(request, *args, **kwargs):

        result = view_func(request, *args, **kwargs)

        if '"exception": true'  in result.rendered_content:
            transaction.rollback()

        else:
            transaction.commit()

            post_data = request.body
            post_data = re.sub(r'password=(.*?)&', 'password=****&', post_data)

            if 'delete' in request.path or 'update' in request.path or 'save' in request.path:
                logger.info(u'End of the request[%s] for URL[%s] with DATA[%s].' % (request.method, request.path, post_data))

        return result

    return _decorated
