
from filters.schema import base_query_param_schema
from filters.validations import (
    CSVofIntegers,
    IntegerLike,
    DatetimeWithTZ
)

# make a validation schema for players filter query params
players_query_schema = base_query_param_schema.extend(
    {
        "id": IntegerLike(),
        "name": unicode,
        "team_id": CSVofIntegers(),  # /?team_id=1,2,3
        "install_ts": DatetimeWithTZ(),
        "update_ts": DatetimeWithTZ(),
    }
)

teams_query_schema = base_query_param_schema.extend(
    {
        "id": IntegerLike(),
        "name": unicode,
        "player_id": CSVofIntegers(),  # /?player_id=1,2,3
        "install_ts": DatetimeWithTZ(),
        "update_ts": DatetimeWithTZ(),
    }
)
