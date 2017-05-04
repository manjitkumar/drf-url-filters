# This module is define and keep all generic type of data-validations.
import sys
import numbers
from functools import partial
from voluptuous import Invalid
from django.utils.dateparse import parse_datetime, parse_date

from .utils import csv_validator

# Forward compatibility with Python 3.x
if sys.version_info.major == 3:
    basestring = str


def IntegerLike(msg=None):
    '''
    Checks whether a value is:
        - int, or
        - long, or
        - float without a fractional part, or
        - str or unicode composed only of digits
    '''
    def fn(value):
        if not any([
            isinstance(value, numbers.Integral),
            (isinstance(value, float) and value.is_integer()),
            (isinstance(value, basestring) and value.isdigit())
        ]):
            raise Invalid(msg or (
                'Invalid input <{0}>; expected an integer'.format(value))
            )
        else:
            return value
    return fn


def Alphanumeric(msg=None):
    '''
    Checks whether a value is:
        - int, or
        - long, or
        - float without a fractional part, or
        - str or unicode composed only of alphanumeric characters
    '''
    def fn(value):
        if not any([
            isinstance(value, numbers.Integral),
            (isinstance(value, float) and value.is_integer()),
            (isinstance(value, basestring) and value.isalnum())
        ]):
            raise Invalid(msg or (
                'Invalid input <{0}>; expected an integer'.format(value))
            )
        else:
            return value
    return fn


def StrictlyAlphanumeric(msg=None):
    '''
    Checks whether a value is:
        - str or unicode, and
        - composed of both alphabets and digits
    '''
    def fn(value):
        if not (
            isinstance(value, basestring) and
            value.isalnum() and not
            value.isdigit() and not
            value.isalpha()
        ):
            raise Invalid(msg or (
                'Invalid input <{0}>; expected an integer'.format(value))
            )
        else:
            return value
    return fn


def DatetimeWithTZ(msg=None):
    '''
    Checks whether a value is :
        - a valid castable datetime object with timezone.
    '''
    def fn(value):
        try:
            date = parse_datetime(value) or parse_date(value)
            if date is not None:
                return date
            else:
                raise ValueError
        except ValueError:
            raise Invalid('<{0}> is not a valid datetime.'.format(value))
    return fn


def CSVofIntegers(msg=None):
    '''
    Checks whether a value is list of integers.
    Returns list of integers or just one integer in
    list if there is only one element in given CSV string.
    '''
    def fn(value):
        try:
            if isinstance(value, basestring):
                if ',' in value:
                    value = list(map(
                        int, filter(
                            bool, list(map(
                                lambda x: x.strip(), value.split(',')
                            ))
                        )
                    ))
                    return value
                else:
                    return [int(value)]
            else:
                raise ValueError
        except ValueError:
            raise Invalid(
                '<{0}> is not a valid csv of integers'.format(value)
            )
    return fn


def CSVOfModelChoices(msg=None, EXISTING_CHOICES=None):
    '''
    Check whether a value is present in the existing model
    choices
    '''
    def fn(value):
        try:
            msg = '<{0}> is not valid model choice or CSV of model choices'.format(
                value
            )
            if isinstance(value, unicode) and ',' in value:
                states = [s.strip() for s in value.split(',')]
                for state in states:
                    if not any(state in choice for choice in EXISTING_CHOICES):
                        raise Invalid(msg)
                return states
            else:
                return value
        except:
            raise Invalid(msg)
return fn


CSVofAlphanumeric = partial(
    csv_validator,
    validator=Alphanumeric,
    invalid_msg='is not a valid csv of alphanumeric characters'
)

CSVofStrictlyAlphanumeric = partial(
    csv_validator,
    validator=StrictlyAlphanumeric,
    invalid_msg='is not a valid csv of alphanumeric characters'
)
