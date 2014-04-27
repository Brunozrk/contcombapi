# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from authentication import BasicAuthentication
from contcombapi.decorator.Log import log
from contcombapi.decorator.Transaction import commit_or_rollback
from contcombapi.exception.serializer.ServiceExceptionSerializer import ServiceExceptionSerializer
from django.db.transaction import commit_manually
from contcombapi.rest.base import Renderer
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)


@log
@commit_manually
@commit_or_rollback
@api_view(['GET'])
@authentication_classes((BasicAuthentication,))
@permission_classes((IsAuthenticated,))
@renderer_classes(Renderer)
def generate_token(request):

    try:

        user = request.user

        if not user.has_token() or not user.is_valid_token():
            user.generate_token()
            user.save()

        return Response({"token": user.token})

    except Exception, e:
        logger.error(e)
        serializer = ServiceExceptionSerializer(message=e)
        return Response(serializer.data)
