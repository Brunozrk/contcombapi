# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from contcombapi.exception.AuthenticationException import AuthenticationException
from contcombapi.exception.serializer.BaseExceptionSerializer import BaseExceptionSerializer
from rest_framework import serializers
from rest_framework.response import Response

class AuthenticationExceptionSerializer(BaseExceptionSerializer):
    
    DEFAULT_NAME = "AuthenticationException"
    DEFAULT_MESSAGE = "Ocorreu erro de Autenticação"
    
    name = serializers.CharField(max_length=500, default=DEFAULT_NAME)
    
    def raise_exception(self):
        raise AuthenticationException(self.init_data.get("message"))
    
    @classmethod
    def response_exception(cls, error_list):
        serializer = AuthenticationExceptionSerializer({"message" : AuthenticationExceptionSerializer.DEFAULT_MESSAGE, "exception" : True, "name" : AuthenticationExceptionSerializer.DEFAULT_NAME, "error_list": error_list })
        return Response(serializer.data)
