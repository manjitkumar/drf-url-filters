# This module is define and keep all generic type of data-validations.
import sys
import numbers
from voluptuous import Invalid
from django.utils.dateparse import parse_datetime, parse_date
from django.core.exceptions import ImproperlyConfigured

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



class GenericSeparatedValidator(object):
    '''
    Creates list like validator for any voluptuous validation function
    and any custom string separator.
    Instance of the class should be passed to the schema like this:
    >>> CSVofIntegers = GenericSeparatedValidator(int, ',')
    >>> Schema({ "field": CSVofIntegers() })

    >>> CSVofIntegers = GenericSeparatedValidator(int, ',')
    >>> CSVofIntegers('1,2,3')
    [1,2,3]

    >>> WeirdSeparatedValidation = GenericSeparatedValidator(int, '^^')
    >>> WeirdSeparatedValidation('1^^2^^3')
    [1, 2, 3]

    >>> CSVofIntegerLike = GenericSeparatedValidator(IntegerLike(), ',')
    >>> CSVofIntegerLike('a,b,c')
    Traceback (most recent call last):
        ...
    voluptuous.error.Invalid: <a,b,c> is not valid set of <IntegerLike>,\
    Invalid input <a>; expected an integer
    '''

    def __init__(self, validation_function, separator=',', msg=None):
        if not isinstance(separator, basestring):
            raise ImproperlyConfigured(
                'GenericSeparatedValidator separator \
                 must be of type basestring'
                )
        self.separator = separator
        self.validation_function = validation_function
        self.msg = msg
        if sys.version_info.major == 3:
            self.value_type = validation_function.__qualname__.split('.')[0]
        else:
            self.value_type = validation_function.__name__

    def __call__(self, value):
        '''
        Checks whether a value is list of given validation_function.
        Returns list of validated values or just one valid value in
        list if there is only one element in given CSV string.
        '''
        try:
            if isinstance(value, basestring):
                if self.separator in value:
                    seperated_string_values =[item.strip() for item
                        in value.split(self.separator)]
                    values = [self.validation_function(item) for item
                        in seperated_string_values]
                else:
                    values = [self.validation_function(value)]
                return values
            else:
                raise ValueError
        except (Invalid, ValueError) as e:
            raise Invalid(self.msg or
                ('<{0}> is not valid set of <{1}>, {2}'.format(
                    value,
                    self.value_type,
                        e)))
