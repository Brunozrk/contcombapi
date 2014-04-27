# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from contcombapi.authentication.authentication import TokenAuthentication, \
    BasicAuthentication
from contcombapi.db.transaction import response_commit
from contcombapi.decorator.Log import log
from contcombapi.decorator.Transaction import commit_or_rollback
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.transaction import commit_manually
from django.forms.models import model_to_dict
from contcombapi.exception.serializer.ObjectDoesNotExistExceptionSerializer import \
    ObjectDoesNotExistExceptionSerializer
from contcombapi.exception.serializer.ServiceExceptionSerializer import \
    ServiceExceptionSerializer
from contcombapi.exception.serializer.ValidationExceptionSerializer import \
    ValidationExceptionSerializer
from contcombapi.messages import error_messages
from contcombapi.rest.base import Renderer
from rest_framework.decorators import api_view, renderer_classes, \
    authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from contcombapi.user.models import User
from contcombapi.user.serializers import SaveSerializer
from contcombapi.utility import is_valid_int_greater_zero_param, clone
from contcombapi.validators.validators import validate_required
import logging

logger = logging.getLogger(__name__)

@log
@commit_manually
@commit_or_rollback
@api_view(['POST'])
@renderer_classes(Renderer)
def save(request):

    try:

        serializer = SaveSerializer(data=request.DATA)

        if serializer.is_valid():

            user = serializer.object
            user.save()

            return response_commit({"user": model_to_dict(user, exclude=["password", "token"])})
        else:
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

        user = User.objects.get_by_pk(request.user.id)

        serializer = SaveSerializer(clone(user), data=request.DATA, partial=True)

        if serializer.is_valid():

            user = serializer.object
            user.save()

            return response_commit({"user": model_to_dict(user, exclude=["password", "token"])})

        else:
            return ValidationExceptionSerializer.response_exception(serializer.errors)

    except ObjectDoesNotExist, e:
        logger.error(e)
        return ServiceExceptionSerializer.response_exception(error_messages.get("invalid") % "Usuário")
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
def get_by_username(request, username):

    try:

        # Valid Username
        validate_required(username)
        # Find User by username to check if it exist
        user = User.objects.get_by_username(username)

        return response_commit({"user": model_to_dict(user, exclude=["password", "token"])})

    except ValidationError, e:
        return ValidationExceptionSerializer.response_exception({"username": e.messages})
    except ObjectDoesNotExist, e:
        return ObjectDoesNotExistExceptionSerializer.response_exception(error_messages.get("invalid") % "Usuário")    
    except Exception, e:
        logger.error(e)
        return ServiceExceptionSerializer.response_exception(error_messages.get("default_error"))

















@log
@commit_manually
@commit_or_rollback
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
@renderer_classes(Renderer)
def get_all(request):

    try:

        users_list = []
        for user in User.objects.all():
            user_list = {}
            user_list['user'] = model_to_dict(user, exclude=["password", "token"])
            users_list.append(user_list)

        return response_commit(users_list)

    except Exception, e:
        logger.error(e)
        return ServiceExceptionSerializer.response_exception(e.message)


@log
@commit_manually
@commit_or_rollback
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
@renderer_classes(Renderer)
def get_by_pk(request, id_user):

    try:

        # Valid ID
        try:
            is_valid_int_greater_zero_param(id_user)
        except ValidationError, e:
            return ValidationExceptionSerializer.response_exception({"id_user": e.messages})

        # Find User by ID to check if it exist
        try:
            user = User.objects.get_by_pk(id_user)
        except ObjectDoesNotExist, e:
            logger.error(e)
            return ObjectDoesNotExistExceptionSerializer.response_exception(error_messages.get("invalid") % "Usuário")

        return response_commit({"user": model_to_dict(user, exclude=["password", "token"])})

    except Exception, e:
        logger.error(e)
        return ServiceExceptionSerializer.response_exception(e)

@log
@commit_manually
@commit_or_rollback
@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
@renderer_classes(Renderer)
def delete(request, id_user):

    try:

        # Valid ID
        try:
            is_valid_int_greater_zero_param(id_user)
        except ValidationError, e:
            return ValidationExceptionSerializer.response_exception({"id_user": e.messages})

        # Find User by ID to check if it exist
        try:
            user = User.objects.get_by_pk(id_user)
        except ObjectDoesNotExist, e:
            return ServiceExceptionSerializer.response_exception(error_messages.get("invalid") % "Usuário")

        user.delete()

        return response_commit()

    except Exception, e:
        logger.error(e)
        return ServiceExceptionSerializer.response_exception(e.message)
