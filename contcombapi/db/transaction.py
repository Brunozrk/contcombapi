# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from django.db import transaction
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)


def response_commit(data=None):
    '''
        @param data:
    '''
    transaction.commit()
    logger.info(data)
    return Response(data)


def response_rollback(data=None):
    '''
        @param data:
    '''
    transaction.rollback()
    logger.error(data)
    return Response(data)
