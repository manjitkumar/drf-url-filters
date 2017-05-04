# drf-url-filters

**drf-url-filters** is a simple django app to apply filters on drf
modelviewset's queryset in a clean, simple and configurable way. It also
supports validations on incoming query params and their values. A beautiful
python package [voluptouos](https://github.com/alecthomas/voluptuous) is being
used for validations on the incoming query parameters. The best part about
voluptouos is you can define your own validations as per your query params
requirements.

# Quick start
---
**Installation**

1. Download `drf-url-filters` app package from this git repo or can be
installed using python-pip like `pip install drf-url-filters`.

2. Add `filters` in INSTALLED_APPS of settings.py file of django project.

**How it works**

1. Your View or ModelViewSet should inherit `FiltersMixin` from
`filters.mixins.FiltersMixin`.

2. To apply filters using `drf-url-filters` we need to configure our view to
have a dict mapping `filter_mappings` which converts incoming query parameters
to query you want to make on the column name on the queryset.

3. Optionally, to perform any preprocessing on the incoming values for
query params, add another dict `filter_value_transformations` which maps
incoming query parameters to functions that should be applied to the values
corresponding to them. The resultant value is used in the final filtering.

# validations.py

```python
import six

from filters.schema import base_query_params_schema
from filters.validations import (
    CSVofIntegers,
    IntegerLike,
    DatetimeWithTZ
)

# make a validation schema for players filter query params
players_query_schema = base_query_param_schema.extend(
    {
        "id": IntegerLike(),
        "name": six.text_type,  # Depends on python version
        "team_id": CSVofIntegers(),  # /?team_id=1,2,3
        "install_ts": DatetimeWithTZ(),
        "update_ts": DatetimeWithTZ(),
        "taller_than": IntegerLike(),
    }
)
```

# views.py

```python

from rest_framework import (
    viewsets,
    filters,
)

from .models import Player, Team
from .pagination import ResultSetPagination
from .serializers import PlayerSerializer, TeamSerializer
from .validations import teams_query_schema, players_query_schema
from filters.mixins import (
    FiltersMixin,
)


class PlayersViewSet(FiltersMixin, viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Player.objects.prefetch_related(
        'teams'  # use prefetch_related to minimize db hits.
    ).all()
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
        'taller_than': 'height__gte',
    }

    field_value_transformations = {
        'taller_than': lambda val: val / 30.48  # cm to ft
    }

    # add validation on filters
    filter_validation_schema = players_query_schema
```

With the use of `drf-url-filters` adding a new filter on a new column is as
simple as adding a new key in the dict. Prohibitting a filter on particular
column is same as removing a key value mapping from the `filter_mappings` dict.


# LICENSE
[MIT License](LICENSE.MD)
Copyright (c) 2016 Manjit Kumar.

# Credits
Special thanks to authors of
[voluptouos](https://github.com/alecthomas/voluptuous) and friends
[cdax](https://github.com/cdax) and [saurabhjha](https://github.com/SaurabhJha)
who encourage people to contribute into open source community.

# Support
Please [open an issue]
(https://github.com/manjitkumar/drf-url-filters/issues/new) for support.
