import unittest
from nose2.tools.such import helper
from voluptuous import Invalid
from django.core.exceptions import ImproperlyConfigured
from filters import validations

INT = 1
LONG = long(INT)
INT_FLOAT = float(INT)
INT_STR = str(INT)
INT_UNICODE = unicode(INT)
ALNUM_STR = "hello123"
ALNUM_UNICODE = unicode(ALNUM_STR)
NON_INT_FLOAT = 1.5
NON_INT_STR = str(NON_INT_FLOAT)
NON_INT_UNICODE = unicode(NON_INT_FLOAT)
NON_ALNUM_STR = "hello 123"
NON_ALNUM_UNICODE = unicode(NON_ALNUM_STR)
INT_CSV = "1,2,3"
NON_INT_CSV = "a,b,c"


class BaseValidationTestCase(object):
    def f(self, v):
        return self.base_function()(v)

    def transform_val(self, v):
        return v

    def test_valid_values(self):
        for v in self.valid_values:
            self.assertEqual(self.f(v), self.transform_val(v))

    def test_invalid_values(self):
        for v in self.invalid_values:
            self.assertRaises(Invalid, self.f, v)


class IntegerLikeTestCase(BaseValidationTestCase, unittest.TestCase):
    base_function = validations.IntegerLike
    valid_values = [
        INT, LONG, INT_FLOAT, INT_STR, INT_UNICODE
    ]
    invalid_values = [
        NON_INT_FLOAT, NON_INT_STR, ALNUM_STR, ALNUM_UNICODE,
        NON_INT_UNICODE, NON_ALNUM_STR, NON_ALNUM_UNICODE
    ]


class AlphanumericTestCase(BaseValidationTestCase, unittest.TestCase):
    base_function = validations.Alphanumeric
    valid_values = [
        INT, LONG, INT_FLOAT, INT_STR, INT_UNICODE, ALNUM_STR, ALNUM_UNICODE
    ]
    invalid_values = [
        NON_INT_FLOAT, NON_INT_STR, NON_INT_UNICODE, NON_ALNUM_STR,
        NON_ALNUM_UNICODE
    ]


class StrictlyAlphanumericTestCase(BaseValidationTestCase, unittest.TestCase):
    base_function = validations.StrictlyAlphanumeric
    valid_values = [ALNUM_STR, ALNUM_UNICODE]
    invalid_values = [
        INT, LONG, INT_FLOAT, NON_INT_FLOAT, NON_INT_STR, NON_INT_UNICODE,
        NON_ALNUM_STR, NON_ALNUM_UNICODE, INT_STR, INT_UNICODE
    ]


class CSVofIntegersTestCase(BaseValidationTestCase, unittest.TestCase):
    base_function = validations.CSVofIntegers
    transform_val = lambda self, v: map(int, v.split(","))
    valid_values = [INT_CSV, INT_STR, INT_UNICODE]
    invalid_values = [
        INT_FLOAT, ALNUM_STR, ALNUM_UNICODE, NON_INT_FLOAT, NON_INT_STR,
        NON_INT_UNICODE, NON_ALNUM_STR, NON_ALNUM_UNICODE, NON_INT_CSV,
        INT, LONG
    ]

class GenericSeparatedValidatorTestCase(unittest.TestCase):
    def test_default_separator(self):
        validator = validations.GenericSeparatedValidator(int)
        self.assertEqual(validator('1,2,3'), [1,2,3])
        self.assertRaises(Invalid, validator, 'a,b,c')
        self.assertEqual(validator('1', [1]))

    def test_custom_separator(self):
        validator = validations.GenericSeparatedValidator(int, 'mm')
        self.assertEqual(validator('1mm2mm3'), [1,2,3])
        self.assertRaises(Invalid, validator, 'ammbmmc')
        self.assertEqual(validator('1', [1]))

    def test_custom_type(self):
        validator = validations.GenericSeparatedValidator(
                        validations.IntegerLike())
        self.assertEqual(validator('1,2,3'), ['1','2','3'])
        self.assertRaises(Invalid, validator, 'a,b,c')
        self.assertEqual(validator('1', ['1']))

    def test_invalid_separator(self):
        self.assertRaises(ImproperlyConfigured, 
            validations.GenericSeparatedValidator, 12)
