# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

import copy
from validators.validators import validate_required, validate_integer, \
    validate_greater_zero, validate_greater_equal_zero, validate_string_is_empty, \
    validate_string_maxsize, validate_string_minsize, validate_boolean
import re
from contcombapi.validators.validators import validate_float,\
    validate_float_greater_zero

def is_valid_required_param(param):
    '''Checks if the parameter is valid.

    @param param: Value to be validated.

    @raise ValidationError: If there is validation error in the field
    '''
    validate_required(param)


def is_valid_int_param(param, required=True):
    '''Checks if the parameter is a valid integer value.

    @param param: Value to be validated.

    @raise ValidationError: If there is validation error in the field
    '''
    if required:
        validate_required(param)

    validate_integer(param)


def is_valid_int_greater_zero_param(param, required=True):
    '''Checks if the parameter is a valid integer value and greater than zero.

    @param param: Value to be validated.

    @raise ValidationError: If there is validation error in the field
    '''
    if required:
        validate_required(param)

    validate_integer(param)

    validate_greater_zero(param)


def is_valid_float_greater_zero_param(param, required=True):
    '''Checks if the parameter is a valid float value and greater than zero.

    @param param: Value to be validated.

    @raise ValidationError: If there is validation error in the field
    '''
    if required:
        validate_required(param)

    validate_float(param)

    validate_float_greater_zero(param)


def is_valid_int_greater_equal_zero_param(param):
    '''Checks if the parameter is a valid integer value and greater and equal than zero.

    @param param: Value to be validated.

    @raise ValidationError: If there is validation error in the field
    '''
    validate_integer(param)

    validate_greater_equal_zero(param)


def is_valid_string_maxsize(param, maxsize, required=True):
    '''Checks if the parameter is a valid string and his size is less than maxsize.
    If the parameter maxsize
    If the parameter required is True than the string can not be None

    @param param: Value to be validated.
    @param maxsize: Max size of the value to be validated.
    @param required: Check if the value can be None

    @raise ValidationError: If there is validation error in the field
    '''

    if required:
        validate_required(param)

    validate_string_is_empty(param)

    validate_string_is_empty(param)

    validate_string_maxsize(param, maxsize)


def is_valid_string_minsize(param, minsize, required=True):
    '''Checks if the parameter is a valid string and his size is more than minsize.
    If the parameter minsize
    If the parameter required is True than the string can not be None

    @param param: Value to be validated.
    @param minsize: Min size of the value to be validated.
    @param required: Check if the value can be None

    @raise ValidationError: If there is validation error in the field
    '''

    if required:
        validate_required(param)

    validate_string_is_empty(param)

    validate_string_is_empty(param)

    validate_string_minsize(param, minsize)


def is_valid_boolean_param(param, required=True):
    '''Checks if the parameter is a valid boolean.

    @param param: Value to be validated.

    @raise ValidationError: If there is validation error in the field
    '''

    if required:
        validate_required(param)

    validate_boolean(param)


def clone(obj):
    '''Clone the object

    @param obj: object to be cloned

    @return object cloned.
    '''
    return copy.copy(obj)


def check_regex(string, regex):
    '''
        Check if the string matches the regex.
        If does not, returns False.

        @param string: String
        @param regex: the regular expression

        @return the match
    '''
    pattern = re.compile(regex)
    return pattern.match(string) is not None
