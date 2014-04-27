# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''
from contcombapi.manager.BaseManager import BaseManager
from django.forms.models import model_to_dict

class ContactManager(BaseManager):
    '''
        Base class for managing the operations to database
    '''
    
    def get_messages_by_user(self, user):
        return self.filter(user=user).values()
