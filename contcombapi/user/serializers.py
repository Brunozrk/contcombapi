# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from contcombapi.user.models import User
from rest_framework import serializers
from contcombapi.messages import user_messages
from contcombapi.validators.messages import email_messages
from django.core.exceptions import ObjectDoesNotExist
import hashlib


class SaveSerializer(serializers.Serializer):

    username = serializers.CharField(min_length=3, max_length=100, required=True)
    name = serializers.CharField(min_length=3, max_length=100, required=True)
    email = serializers.EmailField(max_length=100, required=True, error_messages=email_messages)
    password = serializers.CharField(min_length=6, max_length=100, required=True)
    confirm_password = serializers.CharField(min_length=6, max_length=100, required=True)

    def validate_confirm_password(self, attrs, source):
        if not self.object:
            password = attrs['password']
            confirm_password = attrs[source]
    
            if password != confirm_password:
                raise serializers.ValidationError(user_messages.get("invalid_confirm_password"))
        return attrs

    def validate_username(self, attrs, source):
        username = attrs[source]
        # When updating, should not validate 'username' for same user, set 'None' when is insert
        user_id = self.object.id if self.object else None
        try:
            user = User.objects.get_by_username(username)
            if user.id != user_id:
                raise serializers.ValidationError(user_messages.get("duplicated_username") % username)
        except ObjectDoesNotExist:
            pass

        return attrs

    def restore_object(self, attrs, instance=None):
        """
        Create or update a new User instance, given a dictionary
        of deserialized field values.

        Note that if we don't define this method, then deserializing
        data will simply return a dictionary of items.
        """
        if instance:
            # Update existing instance
            instance.username = attrs.get('username', instance.username)
            instance.name = attrs.get('name', instance.name)

            return instance

        # Remove because isn't in the model
        del attrs['confirm_password']

        user = User(**attrs)
        user.password = hashlib.md5(user.password).hexdigest()

        return user
