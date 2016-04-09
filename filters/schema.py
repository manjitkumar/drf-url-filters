from voluptuous import Schema, ALLOW_EXTRA
from .validations import (
    IntegerLike,
    DatetimeWithTZ
)

# make a base query param schema, which can be extended for api
# specific requirements.
base_query_param_schema = Schema(
        {
            'q': unicode,
            'name': unicode,
            'offset': IntegerLike(),
            'limit': IntegerLike(),
            'install_ts': DatetimeWithTZ(),
            'update_ts': DatetimeWithTZ()
        },
        extra=ALLOW_EXTRA
    )
