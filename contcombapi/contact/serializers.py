# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from contcombapi.contact.models import Contact
from rest_framework import serializers


class SaveSerializer(serializers.Serializer):

    message = serializers.CharField(required=True)

    def restore_object(self, attrs, instance=None):
        """
        Create or update a new Contact instance, given a dictionary
        of deserialized field values.

        Note that if we don't define this method, then deserializing
        data will simply return a dictionary of items.
        """
        if instance:
            # Update existing instance
            instance.message = attrs.get('message', instance.message)

            return instance

        contact = Contact(**attrs)

        return contact
