# drf-url-filters

**drf-url-filters** is a simple django app to apply filters on drf modelviewset's
queryset in a clean, simple and configureable way. It also supports validations
on incoming query params and their values. A beautiful python package voluptouos is being used for validations on the incoming query parameters. The best part about voluptouos is you can define your own validations as per your query params requirements.

# Quick start
---
**Installation**
    
1. Download `drf-url-filters` app package from this git repo or can be isnatlled using python-pip like `pip install drf-url-filters`.

2. Add `filters` in INSTALLED_APPS in settings.py file of django project.

**How it works?**

1. Your View or ModelViewSet should inherit `FiltersMixin` from filters.mixins.FiltersMixin .

2. To apply filters using `drf-url-filters` we need to configure our view to have a dict mapping `filter_mappings` which converts incoming query parameters to query you want to make on the column name on the queryset. 

```python
# validations.py
from filters.validations import (
    CSVofIntegers,
    IntegerLike,
    DatetimeWithTZ
)

from filters.schema import base_query_param_schema

players_query_schema = base_query_param_schema.extend(
    {
        "id": IntegerLike()
        "name": unicode,
        "team_id": CSVofIntegers(),
        "install_ts" :DatetimeWithTZ(),
        "update_ts": DatetimeWithTZ(),
    }
)

# views.py
from rest_framework import viewsets
from filters.mixins import FiltersMixin
from .models import Players
from .serializers import PlayersViewSet
from .validations import players_query_schema


class PlayersViewSet(FiltersMixin, viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`,
    `retrieve`, `update` and `destroy` actions.
    """
    serializer_class = PlayersSerializer
    pagination_class = PlayersPagination
    
    # add a mapping of query_params to db_columns(queries) 
    filter_mappings = {
        'id': 'id',
        'name': 'name__icontains',
        'team_id': 'teams',  # considering a many-to-many related field
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
        query parameters in the URL.
        """
        query_params = self.request.query_params
        queryset = Players.objects.all()
        # This dict will hold filter kwargs to pass in to Django ORM calls.
        db_filters = {}
        # update filters on players queryset using FiltersMixin.get_queryset_filters
        db_filters.update(
            self.get_queryset_filters(
                query_params
            )
        )
        return queryset.filter(**db_filters)
```

With the use of `drf-url-filters` adding a new filter on a new column is as simple as adding a new key in the dict. Prohibitting a filter on particular column is same as removing a a key value mapping from the `filter_mappings` dict.
