# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from django.db import transaction
from rest_framework.response import Response


def response_commit(data=None):
    '''
        @param data:
    '''
    transaction.commit()
    return Response(data)


def response_rollback(data=None):
    '''
        @param data:
    '''
    transaction.rollback()
    return Response(data)
