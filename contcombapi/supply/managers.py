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
    
    def get_detail_equal_vehicles(self, equal_vehicles):
        total_average = 0.0
        total_average_count = 0
        fuels_details = {}
        for vehicle in equal_vehicles:
            details = self.get_details(vehicle.id, vehicle.user)
            total_average += details.get("total_average")
            total_average_count += 1 if details.get("total_average") != 0 else 0
            
            fuel = details.get('fuels_details')
            for index, value in fuel.iteritems():
                fuel_values = fuels_details.get(index, None)
                average_sum = 0.0
                count = 0
                if fuel_values is not None:
                    average_sum = fuel_values.get('average_sum', 0)
                    count = fuel_values.get('count', 0)
                fuels_details.update({
                                      index: 
                                             {"average_sum": value + average_sum,
                                              "count": count + 1}
                                      })
        
        total_average = round(total_average / total_average_count, 2) if total_average_count != 0 else 0
        
        for index, value in fuels_details.iteritems():
            fuels_details.update({index: round(value.get('average_sum') / value.get('count'), 2)})
        
        return {"count": equal_vehicles.count(),
                "total_average": total_average,
                "fuels_details": fuels_details}
        
    def get_details(self, vehicle_id, user):
        supplies = self.filter_by_user_vehicle(user, vehicle_id)
        
        liters = 0.0
        total_spending = 0.0
        total_average = 0.0
        total_average_count = 0
        fuels_details = {}

        for index in range(len(supplies)):
            current_supply = supplies[index]
            liters += current_supply.get('liters')
            total_spending += current_supply.get('total_spending') if current_supply.get('total_spending') is not None else 0

            average = current_supply.get('average')
            if average is not "":
                total_average_count += 1
                total_average += average
                
                # Fuels Details
                fuels = []
                for j_index in range((index+1), len(supplies)):
                    next_supply = supplies[j_index]
                    fuels.append(next_supply.get('fuel')) 
                    if next_supply.get('is_full') is True:
                        break
                key_dict = '/'.join(set(sorted(fuels)))
                fuel_values = fuels_details.get(key_dict, None)
                average_sum = 0.0
                count = 0
                if fuel_values is not None:
                    average_sum = fuel_values.get('average_sum')
                    count = fuel_values.get('count')
                fuels_details.update({
                                     key_dict: 
                                                {'average_sum': average + average_sum, 
                                                 'count': count + 1}
                                     })
        
        total_average = round(total_average / total_average_count, 2) if total_average_count != 0 else 0
        
        for index, value in fuels_details.iteritems():
            fuels_details.update({index: round(value.get('average_sum') / value.get('count'), 2)})

        return {"total_spending": round(total_spending, 2),
                "liters": liters,
                "total_average": total_average,
                "fuels_details": fuels_details}
        
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
                                  'liters': supply.liters,
                                  'odometer': supply.odometer,
                                  'is_full': supply.is_full,
                                  'average': average if average else "",
                                  'fuel': supply.fuel.name,
                                  'total_spending': supply.total_spending,
                                  })

        # Reverse list
        return supplies_list[::-1]
    
def calculate_average(diff_odometer, liters):
    return round((diff_odometer) / (liters), 2)
