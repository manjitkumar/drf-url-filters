
def decorate_get_queryset(f):
    def decorated(self):
        queryset = f(self)
        query_params = self.request.query_params
        url_params = self.kwargs

        # get queryset_filters from FiltersMixin
        queryset_filters = self.get_db_filters(url_params, query_params)

        # This dict will hold filter kwargs to pass in to Django ORM calls.
        db_filters = queryset_filters['db_filters']

        # This dict will hold exclude kwargs to pass in to Django ORM calls.
        db_excludes = queryset_filters['db_excludes']

        return queryset.filter(**db_filters).exclude(**db_excludes)
    return decorated
