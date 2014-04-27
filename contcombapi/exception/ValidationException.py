# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from contcombapi.exception.AbstractException import AbstractException

class ValidationException(AbstractException):
    
    def __init__(self, message, error_list):
        AbstractException.__init__(self, message)
        self.error_list = error_list