# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from rest_framework import serializers


class BaseExceptionSerializer(serializers.Serializer):
    
    message = serializers.CharField(max_length=500, blank=False)
    exception = serializers.BooleanField(default=True)