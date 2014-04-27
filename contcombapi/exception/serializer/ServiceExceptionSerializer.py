# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from contcombapi.exception.serializer.BaseExceptionSerializer import BaseExceptionSerializer
from rest_framework import serializers
from contcombapi.db.transaction import response_rollback
from contcombapi.exception.ServiceException import ServiceException

class ServiceExceptionSerializer(BaseExceptionSerializer):
    
    DEFAULT_NAME = "ServiceException"
    
    name = serializers.CharField(max_length=500, default=DEFAULT_NAME)
    
    def raise_service_exception(self):
        raise ServiceException(self.init_data.get("message"))
    
    def raise_exception(self):
        raise ServiceException(self.init_data.get("message"))
    
    @classmethod
    def response_exception(cls, message):
        serializer = ServiceExceptionSerializer({"message" :  message, "name" : ServiceExceptionSerializer.DEFAULT_NAME, "exception" : True })
        return response_rollback(serializer.data)
    
    @classmethod
    def response_except(cls, message):
        serializer = ServiceExceptionSerializer({"message" : message, "exception" : True, "name" : ServiceExceptionSerializer.DEFAULT_NAME, "error_list" : "" })
        return response_rollback(serializer.data)