from voluptuous import Invalid
from rest_framework.exceptions import ParseError


class FiltersMixin(object):
    """
    This viewset provides dynamically generated
    filters by applying defined filters on generic
    queryset.
    """

    def __get_queryset_filters(self, query_params, *args, **kwargs):
        """
        get url_params and query_params and make db_filters
        to filter the queryset to the finest.
        [1] ~ sign is used to negated / exclude a filter.
        """

        query_include_filter = {}
        query_exclude_filter = {}

        if getattr(self, 'filter_mappings', None) and query_params:

            include_filter = {}
            exclude_filter = {}

            for query, value in query_params.iteritems():
                # [1] ~ sign is used to exclude a filter.
                if query.startswith('~'):
                    query = query[1:]
                    exclude_filter[query] = value

                    query = self.convert_to_db_query(query, value)
                    if query is None:
                        continue

                    query_exclude_filter[query] = value

                else:
                    include_filter[query] = value

                    query = self.convert_to_db_query(query, value)
                    if query is None:
                        continue

                    query_include_filter[query] = value

            try:
                # check and raise 400_BAD_REQUEST for invalid query params
                filter_validation_schema = getattr(
                    self,
                    'filter_validation_schema',
                    base_query_params_schema
                )
                filter_validation_schema(exclude_filter)
                filter_validation_schema(include_filter)
            except Invalid as inst:
                raise ParseError(detail=inst)

        return query_include_filter, query_exclude_filter

    def __merge_query_params(url_params, query_params):
        """
        merges the url_params dict with query_params query dict and returns
        the merged dict.
        """
        url_params = {}
        for key in query_params:
            url_params[key] = query_params.get(key) # get method on query-dict works differently than on dict.
        return url_params

    def get_db_filters(self, url_params, query_params):
        """
        returns a dict with db_filters and db_excludes values which can be
        used to apply on viewsets querysets.
        """

        # merge url and query params
        query_params = self.__merge_query_params(url_params, query_params)

        # get queryset filters
        db_filters, db_excludes = self.__get_queryset_filters(query_params)

        return {
            'db_filters': db_filters,
            'db_excludes': db_excludes,
        }

    def convert_to_db_query(self, query, value):
        """
        get query which is to be ran on db. e.g. __in is not included original query
        [1] when a CSV is passed as value to a query params make a filter with 'IN' query.
        :param query: query string as mentioned in filter_mappings
        :param value: value received in query parameter
        :return: db query safe query string
        """

        validated_query = None

        if query in self.filter_mappings and value:
            validated_query = query

            # [2] multiple options is filter values will execute as `IN` query
            if isinstance(value, list) and not query.endswith('__in'):
                validated_query += '__in'

        return validated_query
