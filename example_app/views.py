from rest_framework import (
    viewsets,
    filters,
)

from .models import Player, Team
from .serializers import PlayerSerializer, TeamSerializer
from .pagination import ResultSetPagination
from .validations import teams_query_schema, players_query_schema
from filters.mixins import (
    FiltersMixin,
)


class PlayersViewSet(FiltersMixin, viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = PlayerSerializer
    pagination_class = ResultSetPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'name', 'update_ts')
    ordering = ('id',)

    # add a mapping of query_params to db_columns(queries)
    filter_mappings = {
        'id': 'id',
        'name': 'name__icontains',
        'team_id': 'teams',
        'install_ts': 'install_ts',
        'update_ts': 'update_ts',
        'update_ts__gte': 'update_ts__gte',
        'update_ts__lte': 'update_ts__lte',
    }

    # add validation on filters
    filter_validation_schema = players_query_schema

    def get_queryset(self):
        """
        Optionally restricts the queryset by filtering against
        a `name` query parameter in the URL.
        """
        query_params = self.request.query_params
        queryset = Player.objects.prefetch_related(
            'teams'  # use prefetch_related to minimize db hits.
        ).all()

        # This dict will hold filter kwargs to pass in to Django ORM calls.
        db_filters = {}

        # filters on mercant queryset
        db_filters.update(
            self.get_queryset_filters(
                query_params
            )
        )
        return queryset.filter(**db_filters)


class TeamsViewSet(FiltersMixin, viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    serializer_class = TeamSerializer
    pagination_class = ResultSetPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('id', 'name', 'update_ts')
    ordering = ('id',)

    # add a mapping of query_params to db_columns(queries)
    filter_mappings = {
        'id': 'id',
        'name': 'name__icontains',
        'player_id': 'teams',
        'install_ts': 'install_ts',
        'update_ts': 'update_ts',
        'update_ts__gte': 'update_ts__gte',
        'update_ts__lte': 'update_ts__lte',
    }

    # add validation on filters
    filter_validation_schema = teams_query_schema

    def get_queryset(self):
        """
        Optionally restricts the queryset by filtering against
        a `name` query parameter in the URL.
        """
        query_params = self.request.query_params
        queryset = Team.objects.prefetch_related(
            'players'
        ).all()

        # This dict will hold filter kwargs to pass in to Django ORM calls.
        db_filters = {}

        # filters on mercant queryset
        db_filters.update(
            self.get_queryset_filters(
                query_params
            )
        )
        return queryset.filter(**db_filters)
