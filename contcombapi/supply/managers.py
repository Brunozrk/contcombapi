# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''
from contcombapi.manager.BaseManager import BaseManager
from django.core.exceptions import ObjectDoesNotExist

class FuelManager(BaseManager):
    '''
        Base class for managing the operations to database
    '''

class SupplyManager(BaseManager):
    '''
        Base class for managing the operations to database
    '''
        
    def get_by_id_and_user(self, pk, user):
        try:
            return self.get(pk=pk, vehicle__user=user)
        except ObjectDoesNotExist, e:
            raise e
        
    def filter_by_user_vehicle(self, user, vehicle_id):
        supplies = self.filter(vehicle__user=user, vehicle_id=vehicle_id).order_by('odometer')
        supplies_list = list()
        last_full = ''
        liters = 0
        added = False
        for supply in supplies:
            average = ""
            if supply.is_full:
                if last_full is not '' and last_full != supply:
                    diff_odometer = supply.odometer - last_full.odometer
                    if added is False:
                        average = calculate_average(diff_odometer, supply.liters)
                    else:
                        average = calculate_average(diff_odometer, liters + supply.liters)
                    liters = 0
                    added = False
                else:
                    liters = supply.liters
                last_full = supply
            else:
                liters += supply.liters
                added = True
                
            supplies_list.append({
                                  'id': supply.id,
                                  'date': supply.date.strftime("%d/%m/%Y"),
                                  'liters': str(supply.liters) + "L",
                                  'odometer': str(supply.odometer) + " Km",
                                  'is_full': supply.is_full,
                                  'average': str(average) + " Km/L" if average else "",
                                  'fuel': supply.fuel.name
                                  })

        # Reverse list
        return supplies_list[::-1]
    
def calculate_average(diff_odometer, liters):
    return round((diff_odometer) / (liters), 2)

    
    
        
        