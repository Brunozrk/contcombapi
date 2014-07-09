# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from contcombapi.authentication.authentication import BasicAuthentication
from contcombapi.vehicle.models import Vehicle
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
from contcombapi.utility import clone, is_valid_float_greater_zero_param
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from contcombapi.messages import error_messages
from contcombapi.supply.models import Supply, Fuel
from contcombapi.supply.serializers import SaveSerializer
from contcombapi.vehicle.serializers import SaveSerializer as SaveVehicleSerializer
from contcombapi.exception.serializer.ObjectDoesNotExistExceptionSerializer import ObjectDoesNotExistExceptionSerializer
import json
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
 
    except ObjectDoesNotExist, e:
        logger.error(e)
        return ObjectDoesNotExistExceptionSerializer.response_exception(e.message)
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
        return ObjectDoesNotExistExceptionSerializer.response_exception(e.message)
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
        # Sumarry vehicle
        vehicle = Vehicle.objects.get_vehicle_by_id_and_user(id_vehicle, request.user)
        supplies = vehicle.supply_set.all().order_by('-odometer')
        odometer = supplies[0].odometer if supplies else 0

        vehicle_response = {"id": vehicle.pk, 
                           "odometer": odometer, 
                           "motor": vehicle.motor,
                           "manufactured": vehicle.manufactured}
        # Sumarry Supplies
        supplies_response = Supply.objects.get_details(id_vehicle, request.user)
        
        # Sumarry Vehicle supplies same model
        equal_vehicles = Vehicle.objects.get_equal_vehicles(vehicle.model, vehicle.manufactured, vehicle.motor)
        equal_vehicles_response = Supply.objects.get_detail_equal_vehicles(equal_vehicles)
            
        return response_commit({'vehicle': vehicle_response, 
                                'supplies': supplies_response, 
                                'equal_vehicles': equal_vehicles_response})
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
def import_old_contcomb(request):
    
    try:
        # # Please, refactor this code! :S
        
        # Save vehicle first...
        serializer = SaveVehicleSerializer(data=request.DATA)

        if serializer.is_valid():

            vehicle = serializer.object
            vehicle.user = request.user
            vehicle.save()
            
            supplies = json.loads(request.DATA.get('supplies'), strict=False)
            current_km = request.DATA.get('current_km')
            walked_km = request.DATA.get('walked_km')

            # Validations
            is_valid_float_greater_zero_param(current_km)
            is_valid_float_greater_zero_param(walked_km)

            current_odometer = float(current_km) - float(walked_km)

            # Iterate supplies...
            for supply in supplies:
                
                # Set default values...
                supply['fuel'] = Fuel.objects.get_first_fuel()
                supply['fuel_price'] = 2
                supply['vehicle'] = vehicle.id
                supply['station'] = ''
                supply['is_full'] = True

                # Set values
                last_odometer = float(supply['odometer'])
                supply['odometer'] = current_odometer

                # Save supply
                serializer = SaveSerializer(data=supply)

                if serializer.is_valid():
                    supply_obj = serializer.object
                    supply_obj.save()
                    current_odometer -=  last_odometer
                else:
                    logger.error(serializer.errors)
                    return ValidationExceptionSerializer.response_exception(serializer.errors)
                
            return response_commit({})
        else:
            logger.error(serializer.errors)
            return ValidationExceptionSerializer.response_exception(serializer.errors)

    except Exception, e:
        logger.error(e)
        return ServiceExceptionSerializer.response_exception(e.message)
    