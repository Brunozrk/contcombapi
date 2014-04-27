# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from exception.serializer.BaseExceptionSerializer import BaseExceptionSerializer
from rest_framework import serializers
from rest_framework.response import Response
from exception.UnauthorizedServiceNowException import UnauthorizedServiceNowException

class UnauthorizedServiceNowExceptionSerializer(BaseExceptionSerializer):
    
    DEFAULT_NAME = "UnauthorizedServiceNowExceptionSerializer"
    DEFAULT_MESSAGE = "Ocorreu erro de Autenticação no Servie Now"
    
    name = serializers.CharField(max_length=500, default=DEFAULT_NAME)
    
    def raise_exception(self):
        raise UnauthorizedServiceNowException(self.init_data.get("message"))
    
    @classmethod
    def response_exception(cls, error_list):
        serializer = UnauthorizedServiceNowExceptionSerializer({"message" : UnauthorizedServiceNowExceptionSerializer.DEFAULT_MESSAGE, "exception" : True, "name" : UnauthorizedServiceNowExceptionSerializer.DEFAULT_NAME, "error_list": error_list })
        return Response(serializer.data)
