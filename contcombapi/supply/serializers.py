# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from contcombapi.supply.models import Supply, Fuel
from rest_framework import serializers
import logging
from contcombapi.vehicle.models import Vehicle
import datetime

logger = logging.getLogger(__name__)

class SaveSerializer(serializers.Serializer):

    vehicle = serializers.IntegerField(required=True, min_value=0)
    odometer = serializers.FloatField(required=True)
    is_full = serializers.BooleanField(required=True)
    date = serializers.CharField(required=True)
    liters = serializers.FloatField(required=True)
    fuel = serializers.IntegerField(required=True)
    station = serializers.CharField(required=False, max_length=100)
    fuel_price = serializers.FloatField(required=True)
    obs = serializers.CharField(required=False)
    
    def restore_object(self, attrs, instance=None):
        """
        Create or update a new User instance, given a dictionary
        of deserialized field values.

        Note that if we don't define this method, then deserializing
        data will simply return a dictionary of items.
        """
        if instance:
            instance.vehicle = Vehicle.objects.get_by_pk(pk=attrs['vehicle'])
            instance.odometer = attrs.get('odometer', instance.odometer)
            instance.is_full = attrs.get('is_full', instance.is_full)
            instance.date = datetime.datetime.strptime(attrs['date'], "%d/%m/%Y").date()
            instance.liters = attrs.get('liters', instance.liters)
            instance.fuel = Fuel.objects.get_by_pk(pk=attrs['fuel'])
            instance.station = attrs.get('station', instance.station)
            instance.fuel_price = attrs.get('fuel_price', instance.fuel_price)
            instance.obs = attrs.get('obs', instance.obs)

            return instance
        
        attrs['vehicle'] = Vehicle.objects.get_by_pk(pk=attrs['vehicle'])
        attrs['date'] = datetime.datetime.strptime(attrs['date'], "%d/%m/%Y").date()
        attrs['fuel'] = Fuel.objects.get_by_pk(pk=attrs['fuel'])
        supply = Supply(**attrs)
        supply.total_spending = supply.liters * supply.fuel_price
        return supply
