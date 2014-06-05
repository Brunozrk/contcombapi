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
from contcombapi.vehicle.serializers import SaveSerializer
from django.forms.models import model_to_dict
from contcombapi.exception.serializer.ValidationExceptionSerializer import ValidationExceptionSerializer
from contcombapi.exception.serializer.ServiceExceptionSerializer import ServiceExceptionSerializer
from contcombapi.utility import clone
from django.core.exceptions import ObjectDoesNotExist
from contcombapi.messages import error_messages
from contcombapi.supply.models import Fuel, Supply

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

            vehicle = serializer.object
            vehicle.user = request.user
            vehicle.save()

            return response_commit({"vehicle": model_to_dict(vehicle)})
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

        vehicle = Vehicle.objects.get_by_pk(request.DATA.get('car_id'))

        serializer = SaveSerializer(clone(vehicle), data=request.DATA)

        if serializer.is_valid():

            vehicle = serializer.object
            vehicle.save()

            return response_commit(model_to_dict(vehicle))

        else:
            return ValidationExceptionSerializer.response_exception(serializer.errors)

    except ObjectDoesNotExist, e:
        logger.error(e)
        return ServiceExceptionSerializer.response_exception(error_messages.get("invalid") % u"Veículo")
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
def get_by_user(request):
    try:
        response = Vehicle.objects.get_vehicles_by_user(request.user)
        
        return response_commit({'cars': response})
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
def get_vehicle_fuel_by_user(request):
    try:
        vehicles = Vehicle.objects.get_vehicles_by_user(request.user)
        fuels = Fuel.objects.all().values()
        
        return response_commit({'vehicles': vehicles, 'fuels': fuels})
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
def get_by_id(request, id_car):

    try:
        vehicle = Vehicle.objects.get_vehicle_by_id_and_user(id_car, request.user)
        
        return response_commit({"id": vehicle.pk, 
                                "model": vehicle.model.name, 
                                "motor": vehicle.motor,
                                "manufactured": vehicle.manufactured})
    
    except ObjectDoesNotExist, e:
        logger.error(e)
        return ServiceExceptionSerializer.response_exception(error_messages.get("invalid") % u"Veículo")
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
def delete(request, id_car):
    
    try:
        contact = Vehicle.objects.get(pk=id_car, user=request.user)
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
def get_models(request):
 
    try:
        models = Model.objects.filter(valid=True).values_list("name", flat=True)
         
        return response_commit({'models': models})
     
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
def get_ranking(request):
 
    try:
        ranking = list()
        vehicles = Vehicle.objects.values('model', 'manufactured', 'motor').distinct()
        for vehicle in vehicles:
            equal_vehicles = Vehicle.objects.get_equal_vehicles(vehicle.get('model'), 
                                                                vehicle.get('manufactured'),
                                                                vehicle.get('motor'))
            ranking.append({
                            "vehicle": str(Model.objects.get_by_pk(pk=vehicle.get('model'))) + " - " + str(vehicle.get('motor')) + " - " + str(vehicle.get('manufactured')),
                            "details": Supply.objects.get_detail_equal_vehicles(equal_vehicles), 
                            })
        ranking = sorted(ranking, key=lambda k: k['details']['total_average'], reverse=True) 
        return response_commit({'ranking': ranking})
     
    except Exception, e:
        logger.error(e)
        return ServiceExceptionSerializer.response_exception(e.message)

