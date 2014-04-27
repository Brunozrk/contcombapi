# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from contcombapi.exception.AbstractException import AbstractException

class ObjectDoesNotExistException(AbstractException):
    
    def __init__(self, message):
        AbstractException.__init__(self, message)
