# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from __future__ import unicode_literals
from django.utils.encoding import DjangoUnicodeDecodeError
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import BaseAuthentication
import base64
from contcombapi.messages import user_messages, error_messages
from contcombapi.user.models import User


class BasicAuthentication(BaseAuthentication):
    """
    HTTP Basic authentication against username/password.
    """

    www_authenticate_realm = 'api'

    def authenticate(self, request):
        """
        Returns a `User` if a correct username and password have been supplied
        using HTTP Basic authentication.  Otherwise returns `None`.
        """
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        if type(auth) == type(''):
            # Work around django test client oddness
            auth = auth.encode(HTTP_HEADER_ENCODING)
        auth = auth.split()

        if not auth or auth[0].lower() != b'basic':
            return None

        if len(auth) != 2:
            raise exceptions.AuthenticationFailed(user_messages.get("invalid_basic_header"))

        try:
            auth_parts = base64.b64decode(auth[1]).decode(HTTP_HEADER_ENCODING).partition(':')
        except (TypeError, UnicodeDecodeError):
            raise exceptions.AuthenticationFailed(user_messages.get("invalid_basic_header"))

        try:
            userid, password = auth_parts[0], auth_parts[2]
        except DjangoUnicodeDecodeError:
            raise exceptions.AuthenticationFailed(user_messages.get("invalid_basic_header"))

        return self.authenticate_credentials(userid, password)

    def authenticate_credentials(self, userid, password):
        """
        Authenticate the userid and password against username and password.
        """
        user = User.objects.authenticate_user(userid, password)
        if user is not None:
            return (user, None)

        raise exceptions.AuthenticationFailed(error_messages.get("invalid_user_or_pass"))

    def authenticate_header(self, request):
        return 'Basic realm="%s"' % self.www_authenticate_realm


class TokenAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a=
    """
    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', '').split()

        if not auth or auth[0].lower() != "token":
            return None

        if len(auth) != 2:
            raise exceptions.AuthenticationFailed(user_messages.get("invalid_token_header"))

        return self.authenticate_credentials(auth[1])

    def authenticate_credentials(self, key):
        """
        Authenticate the token.
        """
        try:
            user = User.objects.get(token=key)
        except Exception:
            raise exceptions.AuthenticationFailed(user_messages.get("invalid token"))

        if user.is_valid_token():
            return (user, None)

        raise exceptions.AuthenticationFailed(user_messages.get("invalid_token"))

    def authenticate_header(self, request):
        return 'Token'
