# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''
from django.contrib import admin
from contcombapi.reminder.models import Reminder

class ReminderAdmin(admin.ModelAdmin):
    
    list_display = ('date', 'vehicle', 'description')
    search_fields = ('vehicle__model__name', 'vehicle__user__name', 'description')
    
    
admin.site.register(Reminder, ReminderAdmin)
