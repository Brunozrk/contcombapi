# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from django.db.models.query import QuerySet


class BaseQuerySet(QuerySet):
    '''
        Represents a lazy database lookup for a set of objects.
    '''
