# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''
from django.contrib import admin
from contcombapi.supply.models import Supply, Fuel

class FuelAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'name')
    #search_fields = ('vehicle__model__name', 'vehicle__user__name', 'description')
    
class SupplyAdmin(admin.ModelAdmin):
    
    list_display = ('date', 'vehicle', 'odometer', 'liters', 'fuel', 'fuel_price', 'total_spending', 'station', 'is_full')
    search_fields = ('vehicle__model__name', 'odometer', 'liters', 'fuel__name', 'fuel_price', 'total_spending', 'station')
    
    
admin.site.register(Supply, SupplyAdmin)
admin.site.register(Fuel, FuelAdmin)