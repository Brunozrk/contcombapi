# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''
from contcombapi.manager.BaseManager import BaseManager

class VehicleManager(BaseManager):
    '''
        Base class for managing the operations to database
    '''
    
    def get_vehicles_by_user(self, user):
        return self.filter(user=user).values('id', 'model__name', 'motor', 'manufactured')
