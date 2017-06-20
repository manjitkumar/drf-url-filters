import six
from voluptuous import Invalid
from rest_framework.exceptions import ParseError

from .metaclasses import MetaFiltersMixin
from .schema import base_query_params_schema


@six.add_metaclass(MetaFiltersMixin)
class FiltersMixin(object):
    '''
    This viewset provides dynamically generated
    filters by applying defined filters on generic
    queryset.
    '''

    def __get_queryset_filters(self, query_params, *args, **kwargs):
        '''
        get url_params and query_params and make db_filters
        to filter the queryset to the finest.
        [1] ~ sign is used to negated / exclude a filter.
        [2] when a CSV is passed as value to a query params make a filter
            with 'IN' query.
        '''

        filters = []
        excludes = []

        if getattr(self, 'filter_mappings', None) and query_params:
            filter_mappings = self.filter_mappings
            value_transformations = getattr(self, 'filter_value_transformations', {})

            try:
                # check and raise 400_BAD_REQUEST for invalid query params
                filter_validation_schema = getattr(
                    self,
                    'filter_validation_schema',
                    base_query_params_schema
                )
                query_params = filter_validation_schema(query_params)
            except Invalid as inst:
                raise ParseError(detail=inst)

            iterable_query_params = (
                query_params.iteritems() if six.PY2 else query_params.items()
            )

            for query, value in iterable_query_params:
                # [1] ~ sign is used to exclude a filter.
                is_exclude = '~' in query
                if query in self.filter_mappings and value:
                    query_filter = filter_mappings[query]
                    transform_value = value_transformations.get(query, lambda val: val)
                    transformed_value = transform_value(value)
                    # [2] multiple options is filter values will execute as `IN` query
                    if isinstance(value, list) and not query_filter.endswith('__in'):
                        query_filter += '__in'
                    if is_exclude:
                        excludes.append((query_filter, transformed_value))
                    else:
                        filters.append((query_filter, transformed_value))

        return dict(filters), dict(excludes)

    def __merge_query_params(self, url_params, query_params):
        '''
        merges the url_params dict with query_params query dict and returns
        the merged dict.
        '''
        url_params = {}
        for key in query_params:
            url_params[key] = query_params.get(key) # get method on query-dict works differently than on dict.
        return url_params

    def get_db_filters(self, url_params, query_params):
        '''
        returns a dict with db_filters and db_excludes values which can be
        used to apply on viewsets querysets.
        '''

        # merge url and query params
        query_params = self.__merge_query_params(url_params, query_params)

        # get queryset filters
        db_filters = self.__get_queryset_filters(query_params)[0]
        db_excludes = self.__get_queryset_filters(query_params)[1]

        return {
            'db_filters': db_filters,
            'db_excludes': db_excludes,
        }

    def get_queryset(self):
        # Defined here to handle the case where the viewset
        # does not override get_queryset
        # (and hence the metaclass would not have been
        # able to decorate it with the filtering logic.)

        return super(FiltersMixin, self).get_queryset()
