# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from db.transaction import response_rollback
from exception.ObjectDoesNotExistException import \
    ObjectDoesNotExistException
from exception.serializer.BaseExceptionSerializer import \
    BaseExceptionSerializer
from rest_framework import serializers

class ObjectDoesNotExistExceptionSerializer(BaseExceptionSerializer):
   
    DEFAULT_NAME = "ObjectDoesNotExistException"    
            
    name = serializers.CharField(max_length=500, default=DEFAULT_NAME)   
    
    def raise_exception(self):
        raise ObjectDoesNotExistException(self.init_data.get("message"))
    
    @classmethod
    def response_exception(cls, message):
        serializer = ObjectDoesNotExistExceptionSerializer({"message" :  message, "name" : ObjectDoesNotExistExceptionSerializer.DEFAULT_NAME, "exception" : True })
        return response_rollback(serializer.data)
    
    @classmethod
    def response_except(cls, message):
        serializer = ObjectDoesNotExistExceptionSerializer({"message" : message, "name" :ObjectDoesNotExistExceptionSerializer.DEFAULT_NAME , "exception" : True,  "error_list" : "" })
        return response_rollback(serializer.data)