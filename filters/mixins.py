from voluptuous import Invalid
from rest_framework.exceptions import ParseError


class FiltersMixin(object):
    '''
    This viewset provides dynamically generated
    filters by applying defined filters on generic
    queryset.
    '''

    def get_queryset_filters(self, query_params, *args, **kwargs):
        '''
        get url_params and query_params and make db_filters
        to filter the queryset to the finest.

        [1] when a CSV is passed as value to a query params make a filter
            with 'IN' query.
        '''

        filters = []
        if getattr(self, 'filter_mappings', None) and query_params:
            filter_mappings = self.filter_mappings

            try:
                # check and raise 400_BAD_REQUEST for invalid query params
                if getattr(self, 'filter_validation_schema', None):
                    query_params = self.filter_validation_schema(
                        self.request.query_params
                    )
                else:
                    raise Invalid('Validation is not configured for filters.')
            except Invalid as inst:
                raise ParseError(detail=inst)

            filters = []
            for query, value in query_params.items():
                if query in self.filter_mappings and value:
                    query = filter_mappings[query]
                    # [1] multiple options is filter values will execute as in query
                    if isinstance(value, list):
                        query += '__in'
                    if value:
                        filters.append((query, value))
            filters = dict(filters)
        return filters
