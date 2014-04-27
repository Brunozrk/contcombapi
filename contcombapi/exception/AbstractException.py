# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

class AbstractException(Exception):
    
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        msg = '%s' % (self.message) 
        return msg.encode('utf-8', 'replace')