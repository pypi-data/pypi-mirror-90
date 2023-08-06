"""
SQLAlchemy declarative compatible JSON encoder.

````python
from drizm_commons.sqla.encode import *
````
"""
import datetime
import json
from typing import Any

from sqlalchemy.ext.declarative import DeclarativeMeta


class SqlaDeclarativeEncoder(json.JSONEncoder):
    """
    A custom JSON encoder for serializing SQLAlchemy
    declarative base instances.

    Supports ISO8601 compliant datetime encoding.
    """

    datetypes = (datetime.date, datetime.datetime, datetime.timedelta)

    def default(self, o: Any) -> Any:
        # Check if the object is an SQLAlchemy declarative instance
        if isinstance(o.__class__, DeclarativeMeta):
            fields = {}

            # Get all fields of the class
            # The dunder dict of an SQLA declarative instance will
            # always contain all actual / mapped fields.
            # Its thus the best way for us to get all fields that are
            # supposedly in the database as well.
            available_fields = [
                k for k in o.__dict__.keys() if k is not "_sa_instance_state"
            ]

            for field in available_fields:
                data = self._process_column(o, field)
                fields[field] = data

            return fields

        # If it is not an SQLAlchemy object, use the default encoder
        return super(SqlaDeclarativeEncoder, self).default(o)

    def _process_column(self, o: Any, column_name: str):
        # Obtain the value of the column and check for custom encoding
        field_value = getattr(o, column_name)
        data = self.dump(field_value)

        try:  # Try JSON encoding the field
            json.dumps(data)

        except TypeError as exc:  # if it fails resort to failure hook
            data = self.handle_failure(exc, data)

        return data

    def dump(self, v: Any) -> Any:
        """ Hook for custom object deserialization. """
        if v.__class__ in self.datetypes:
            return self.serialize_datetypes_to_iso(v)

        return v

    # noinspection PyMethodMayBeStatic
    def serialize_datetypes_to_iso(self, v: datetypes) -> str:
        """ Converts datetime formats to ISO8601 compliant strings. """
        if isinstance(v, datetime.timedelta):
            return (datetime.datetime.min + v).time().isoformat()
        return v.isoformat()

    def handle_failure(self, exc: Exception, value: Any):
        """ Can be overridden to provide handling for custom fields. """
        # Simply re-raise the exception by default
        raise exc


__all__ = ["SqlaDeclarativeEncoder"]
