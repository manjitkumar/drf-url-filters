from .decorators import decorate_get_queryset


class MetaFiltersMixin(type):
    def __new__(cls, name, bases, dct):
        if 'get_queryset' in dct:
            dct['get_queryset'] = decorate_get_queryset(dct['get_queryset'])
        return super(MetaFiltersMixin, cls).__new__(cls, name, bases, dct)

    def __setattr__(self, attr, val):
        if attr == 'get_queryset':
            val = decorate_get_queryset(val)
        return super(MetaFiltersMixin, self).__setattr__(attr, val)
