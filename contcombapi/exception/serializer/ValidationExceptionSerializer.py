# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from contcombapi.exception.ValidationException import ValidationException
from contcombapi.exception.serializer.BaseExceptionSerializer import BaseExceptionSerializer
from rest_framework import serializers
from contcombapi.db.transaction import response_rollback

class ValidationExceptionSerializer(BaseExceptionSerializer):

    DEFAULT_NAME = "ValidationException"
    DEFAULT_MESSAGE = "Ocorreu erro de validação"

    name = serializers.CharField(max_length=500, default=DEFAULT_NAME)
    error_list = serializers.CharField(max_length=500, blank=False, default='')

    def raise_exception(self):
        raise ValidationException(self.init_data.get("message"), self.init_data.get("error_list"))

    @classmethod
    def response_exception(cls, error_list):
        serializer = ValidationExceptionSerializer({"message" : ValidationExceptionSerializer.DEFAULT_MESSAGE, "exception" : True, "name" : ValidationExceptionSerializer.DEFAULT_NAME, "error_list": error_list })
        return response_rollback(serializer.data)

    @classmethod
    def response_except(cls, message):
        serializer = ValidationExceptionSerializer({"message" : message, "exception" : True, "name" : ValidationExceptionSerializer.DEFAULT_NAME, "error_list" : "" })
        return response_rollback(serializer.data)
