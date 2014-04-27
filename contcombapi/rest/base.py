# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from contcombapi.settings import IsBrowsableAPIRenderer
from rest_framework.renderers import JSONRenderer, JSONPRenderer, BrowsableAPIRenderer

if IsBrowsableAPIRenderer:
    Renderer = (JSONRenderer, JSONPRenderer, BrowsableAPIRenderer)
else:
    Renderer = (JSONRenderer, JSONPRenderer)
