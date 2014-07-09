# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from django.core.exceptions import ValidationError
from messages import messages
from django.utils.datetime_safe import datetime
import re


def validate_required(value):
    if value is None or value == '':
        raise ValidationError(messages.get('required'))


def validate_integer(value):
    try:
        int(value)
    except (TypeError, ValueError):
        raise ValidationError(messages.get('integer'))

def validate_float(value):
    try:
        float(value)
    except (TypeError, ValueError):
        raise ValidationError(messages.get('float'))

def validate_greater_zero(value):
    if int(value) <= 0:
        raise ValidationError(messages.get('greater_zero'))

def validate_greater_equal_zero(value):
    if int(value) < 0:
        raise ValidationError(messages.get('greater_equal_zero'))

def validate_float_greater_zero(value):
    if float(value) <= 0:
        raise ValidationError(messages.get('greater_float_zero'))

def validate_float_greater_equal_zero(value):
    if float(value) < 0:
        raise ValidationError(messages.get('greater_equal_zero'))

def validate_string(value):
    if not isinstance(value, basestring):
        raise ValidationError(messages.get('string'))


def validate_string_is_empty(value):
    if '' == value.strip():
        raise ValidationError(messages.get('required'))


def validate_string_maxsize(value, maxsize):
    if len(value.strip()) > maxsize:
        raise ValidationError(messages.get('max_length') % {'limit_value': maxsize})


def validate_string_minsize(value, minsize):
    if len(value.strip()) < minsize:
        raise ValidationError(messages.get('min_length') % {'limit_value': minsize})


def validate_boolean(value):
    if not value in ['0', '1', 'False', 'True', False, True, 'false', 'true']:
        raise ValidationError(messages.get('boolean'))


def validate_cpf(value):

    try:

        digits_cpf = [10, 9, 8, 7, 6, 5, 4, 3, 2]
        cpf = re.sub('[.-]', '', value)

        total = 0
        for i in range(9):
            total += (int(cpf[i]) * digits_cpf[i])

        mod = (total % 11)
        first_digit = 0
        if mod >= 2:
            first_digit = (11 - mod)

        digits_cpf.insert(0, 11)

        total = 0
        for i in range(10):
            total += (int(cpf[i]) * digits_cpf[i])

        mod = (total % 11)
        second_digit = 0
        if mod >= 2:
            second_digit = (11 - mod)

        if int(cpf[9]) != first_digit:
            raise ValidationError(messages.get('cpf'))

        if int(cpf[10]) != second_digit:
            raise ValidationError(messages.get('cpf'))

    except:
        raise ValidationError(messages.get('cpf'))
