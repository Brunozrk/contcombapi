# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from contcombapi.authentication.authentication import BasicAuthentication
from contcombapi.vehicle.models import Vehicle, Model
from contcombapi.db.transaction import response_commit
from contcombapi.decorator.Log import log
from contcombapi.decorator.Transaction import commit_or_rollback
from django.db.transaction import commit_manually
from contcombapi.rest.base import Renderer
from rest_framework.decorators import api_view, renderer_classes, \
    authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
import logging
from django.forms.models import model_to_dict
from contcombapi.exception.serializer.ValidationExceptionSerializer import ValidationExceptionSerializer
from contcombapi.exception.serializer.ServiceExceptionSerializer import ServiceExceptionSerializer
from contcombapi.utility import clone
from django.core.exceptions import ObjectDoesNotExist
from contcombapi.messages import error_messages
from contcombapi.supply.models import Supply
from contcombapi.supply.serializers import SaveSerializer

logger = logging.getLogger(__name__)

@log
@commit_manually
@commit_or_rollback
@api_view(['POST'])
@authentication_classes((BasicAuthentication,))
@permission_classes((IsAuthenticated,))
@renderer_classes(Renderer)
def save(request):
 
    try:
        serializer = SaveSerializer(data=request.DATA)
 
        if serializer.is_valid():
 
            supply = serializer.object
            supply.save()
 
            return response_commit({"supply": model_to_dict(supply)})
        else:
            logger.error(serializer.errors)
            return ValidationExceptionSerializer.response_exception(serializer.errors)
 
    except Exception, e:
        logger.error(e)
        return ServiceExceptionSerializer.response_exception(e.message)
 
 
@log
@commit_manually
@commit_or_rollback
@api_view(['POST'])
@authentication_classes((BasicAuthentication,))
@permission_classes((IsAuthenticated,))
@renderer_classes(Renderer)
def update(request):
 
    try:
 
        supply = Supply.objects.get_by_pk(request.DATA.get('supply_id'))
 
        serializer = SaveSerializer(clone(supply), data=request.DATA)
 
        if serializer.is_valid():
 
            supply = serializer.object
            supply.save()
 
            return response_commit(model_to_dict(supply))
 
        else:
            return ValidationExceptionSerializer.response_exception(serializer.errors)
 
    except ObjectDoesNotExist, e:
        logger.error(e)
        return ServiceExceptionSerializer.response_exception(error_messages.get("invalid") % u"Abastecimento")
    except Exception, e:
        logger.error(e)
        return ServiceExceptionSerializer.response_exception(e.message)


@log
@commit_manually
@commit_or_rollback
@api_view(['GET'])
@authentication_classes((BasicAuthentication,))
@permission_classes((IsAuthenticated,))
@renderer_classes(Renderer)
def get_by_user_vehicle(request, id_vehicle):
    try:
        response = Supply.objects.filter_by_user_vehicle(request.user, id_vehicle)
        
        return response_commit({'supplies': response})
    except Exception, e:
        logger.error(e)
        return ServiceExceptionSerializer.response_exception(e.message)

@log
@commit_manually
@commit_or_rollback
@api_view(['GET'])
@authentication_classes((BasicAuthentication,))
@permission_classes((IsAuthenticated,))
@renderer_classes(Renderer)
def get_by_id(request, id_supply):
 
    try:
        supply = Supply.objects.get_by_id_and_user(id_supply, request.user)
         
        return response_commit(model_to_dict(supply))
     
    except ObjectDoesNotExist, e:
        logger.error(e)
        return ServiceExceptionSerializer.response_exception(error_messages.get("invalid") % u"Abastecimento")
    except Exception, e:
        logger.error(e)
        return ServiceExceptionSerializer.response_exception(e.message)
 
 
@log
@commit_manually
@commit_or_rollback
@api_view(['DELETE'])
@authentication_classes((BasicAuthentication,))
@permission_classes((IsAuthenticated,))
@renderer_classes(Renderer)
def delete(request, id_supply):
     
    try:
        contact = Supply.objects.get(pk=id_supply, vehicle__user=request.user)
        contact.delete()
         
        return response_commit()
 
    except Exception, e:
        logger.error(e)
        return ServiceExceptionSerializer.response_exception(e.message)

@log
@commit_manually
@commit_or_rollback
@api_view(['GET'])
@authentication_classes((BasicAuthentication,))
@permission_classes((IsAuthenticated,))
@renderer_classes(Renderer)
def get_summary_by_vehicle(request, id_vehicle):
    try:
        vehicle = Vehicle.objects.get_vehicle_by_id_and_user(id_vehicle, request.user)
        odometer = vehicle.supply_set.all().order_by('-odometer')[0].odometer
        vehicle_response = {"id": vehicle.pk, 
                           "odometer": odometer, 
                           "motor": vehicle.motor,
                           "manufactured": vehicle.manufactured}
        
        supplies_response = Supply.objects.get_details(id_vehicle, request.user)
        return response_commit({'vehicle': vehicle_response, 'supplies': supplies_response})
    except Exception, e:
        logger.error(e)
        return ServiceExceptionSerializer.response_exception(e.message)     
 
# @log
# @commit_manually
# @commit_or_rollback
# @api_view(['GET'])
# @authentication_classes((BasicAuthentication,))
# @permission_classes((IsAuthenticated,))
# @renderer_classes(Renderer)
# def get_models(request):
#  
#     try:
#         models = Model.objects.filter(valid=True).values_list("name", flat=True)
#          
#         return response_commit({'models': models})
#      
#     except Exception, e:
#         logger.error(e)
#         return ServiceExceptionSerializer.response_exception(e.message)
