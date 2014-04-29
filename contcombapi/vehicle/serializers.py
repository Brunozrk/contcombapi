# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from rest_framework import serializers
from datetime import date
from contcombapi.vehicle.models import Vehicle, Model
import logging

logger = logging.getLogger(__name__)

class SaveSerializer(serializers.Serializer):

    model = serializers.CharField(min_length=3, max_length=100, required=True)
    motor = serializers.CharField(min_length=3, max_length=100, required=True)
    manufactured = serializers.IntegerField(min_value=1970, max_value=(date.today().year + 1))
    
    def restore_object(self, attrs, instance=None):
        """
        Create or update a new User instance, given a dictionary
        of deserialized field values.

        Note that if we don't define this method, then deserializing
        data will simply return a dictionary of items.
        """
        if instance:
            # Update existing instance
            model = attrs.get('model', instance.model)
            if type(model) is int:
                instance.model = model
            else:
                instance.model, _ = Model.objects.get_or_create(name=model.upper())
            instance.motor = attrs.get('motor', instance.motor)
            instance.manufactured = attrs.get('manufactured', instance.manufactured)

            return instance
        
        model, _ = Model.objects.get_or_create(name=attrs['model'].upper())
        attrs["model"] = model
        vehicle = Vehicle(**attrs)
        return vehicle
