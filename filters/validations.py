# This module is define and keep all generic type of data-validations.
import re
from voluptuous import Invalid
from django.utils.dateparse import parse_datetime, parse_date


def IntegerLike(msg=None):
    '''
    Checks whether a value is:
        - int, or
        - long, or
        - float without a fractional part, or
        - str or unicode composed only of digits
    '''
    def fn(value):
        if not (
            isinstance(value, int) or
            isinstance(value, long) or
            (isinstance(value, float) and value.is_integer()) or
            (isinstance(value, str) and value.isdigit()) or
            (isinstance(value, unicode) and value.isdigit())
        ):
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
        if not (
            isinstance(value, int) or
            isinstance(value, long) or
            (isinstance(value, float) and value.is_integer()) or
            (isinstance(value, str) and value.isalnum()) or
            (isinstance(value, unicode) and value.isalnum())
        ):
            raise Invalid(msg or (
                'Invalid input <{0}>; expected an integer'.format(value))
            )
        else:
            return value
    return fn


re_alphabets = re.compile('[A-Za-z]')
re_digits = re.compile('[0-9]')


def StrictlyAlphanumeric(msg=None):
    '''
    Checks whether a value is:
        - str or unicode, and
        - composed of both alphabets and digits
    '''
    def fn(value):
        if not (
            (isinstance(value, str) or isinstance(value, unicode)) and
            re_alphabets.search(value) and
            re_digits.search(value)
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
            if isinstance(value, unicode):
                if ',' in value:
                    value = map(
                        int, filter(
                            bool, map(
                                lambda x: x.strip(), value.split(',')
                            )
                        )
                    )
                    return value
                else:
                    return [int(value)]
        except ValueError:
            raise Invalid(
                '<{0}> is not a valid csv of integers'.format(value)
            )
    return fn
