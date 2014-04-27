# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from contcombapi.authentication.authentication import BasicAuthentication
from contcombapi.contact.models import Contact
from contcombapi.contact.serializers import SaveSerializer
from contcombapi.db.transaction import response_commit
from contcombapi.decorator.Log import log
from contcombapi.decorator.Transaction import commit_or_rollback
from django.core.exceptions import ObjectDoesNotExist
from django.db.transaction import commit_manually
from django.forms.models import model_to_dict
from contcombapi.exception.serializer.ServiceExceptionSerializer import \
    ServiceExceptionSerializer
from contcombapi.exception.serializer.ValidationExceptionSerializer import \
    ValidationExceptionSerializer
from contcombapi.messages import error_messages
from contcombapi.rest.base import Renderer
from rest_framework.decorators import api_view, renderer_classes, \
    authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
import logging

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

            contact = serializer.object
            contact.user = request.user
            contact.save()

            return response_commit()
        else:
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
    
    response = Contact.objects.get_messages_by_user(request.user)
    
    return response_commit({'messages': response})


@log
@commit_manually
@commit_or_rollback
@api_view(['GET'])
@authentication_classes((BasicAuthentication,))
@permission_classes((IsAuthenticated,))
@renderer_classes(Renderer)
def get_by_id(request, id_message):
    
    response = Contact.objects.get_by_pk(pk=id_message)
    
    return response_commit(model_to_dict(response))



@log
@commit_manually
@commit_or_rollback
@api_view(['DELETE'])
@authentication_classes((BasicAuthentication,))
@permission_classes((IsAuthenticated,))
@renderer_classes(Renderer)
def delete(request, id_message):
    
    contact = Contact.objects.get(pk=id_message, user=request.user)
    contact.delete()
    
    return response_commit()
    