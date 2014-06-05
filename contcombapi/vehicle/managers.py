# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''
from contcombapi.manager.BaseManager import BaseManager
from django.core.exceptions import ObjectDoesNotExist

class ModelManager(BaseManager):
    '''
        Base class for managing the operations to database
    '''
    

class VehicleManager(BaseManager):
    '''
        Base class for managing the operations to database
    '''
    
    def get_vehicles_by_user(self, user):
        return self.filter(user=user).values('id', 'model__name', 'motor', 'manufactured')
    
    def get_vehicle_by_id_and_user(self, pk, user):
        try:
            return self.get(pk=pk, user=user)
        except ObjectDoesNotExist, e:
            raise e

    #def get_equal_vehicles(self, vehicle):
    #    return self.filter(model=vehicle.model, manufactured=vehicle.manufactured, motor=vehicle.motor)

    def get_equal_vehicles(self, model, manufactured, motor):
        return self.filter(model=model, manufactured=manufactured, motor=motor)
