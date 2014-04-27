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
from contcombapi.vehicle.serializers import SaveSerializer
from django.forms.models import model_to_dict
from contcombapi.exception.serializer.ValidationExceptionSerializer import ValidationExceptionSerializer
from contcombapi.exception.serializer.ServiceExceptionSerializer import ServiceExceptionSerializer

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
@api_view(['GET'])
@authentication_classes((BasicAuthentication,))
@permission_classes((IsAuthenticated,))
@renderer_classes(Renderer)
def get_by_user(request):
    
    response = Vehicle.objects.get_vehicles_by_user(request.user)
    
    return response_commit({'cars': response})