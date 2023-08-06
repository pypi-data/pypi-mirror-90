"""
Custom SQL Alchemy Column Types. 
These are used to distinctly identify each column within a model, allowing 
us to map it back to its python, marshamallow, sql types, and random generation functions

DO NOT import `db` into this file. Use standalone sql-alchemy types.

By using these columns throughout our models we can then automatically:
- generate different representations of the models schema
- accept input data in multiple formats in multiple contexts  (api, cli, python, graphql, sql, ui)
- perform validations in multiple contexts (api, cli, python)
- generate documentation in multiple contexts (api, cli, python, graphql, sql, ui)

"""
import re

from sqlalchemy import types, cast
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy.dialects.postgresql import ENUM, JSONB, ARRAY

# SQL Alchemy Column to Sickdb-Type Mpaping #


class TextCol(types.TypeDecorator):
    __dada_type__ = "text"
    impl = types.Unicode


# numeric columns


class SmallIntCol(types.TypeDecorator):
    __dada_type__ = "smallint"
    impl = types.SmallInteger


class IntCol(types.TypeDecorator):
    __dada_type__ = "int"
    impl = types.Integer


class BigIntCol(types.TypeDecorator):
    __dada_type__ = "bigint"
    impl = types.BigInteger


class NumCol(types.TypeDecorator):
    __dada_type__ = "num"
    impl = types.Numeric


# date + time columns

_DateTz = types.DateTime(timezone=True)


class DateTzCol(types.TypeDecorator):
    __dada_type__ = "date_tz"
    impl = _DateTz


_Date = types.DateTime(timezone=False)


class DateCol(types.TypeDecorator):
    __dada_type__ = "date"
    impl = _DateTz


_Time = types.Time(timezone=False)


class TimeCol(types.TypeDecorator):
    __dada_type__ = "time"
    impl = _Time


_TimeTz = types.Time(timezone=True)


class TimeTzCol(types.TypeDecorator):
    __dada_type__ = "time_tz"
    impl = _Time


# OTHER COLUMNS


class BinCol(types.TypeDecorator):
    __dada_type__ = "bin"
    impl = types.LargeBinary


class BoolCol(types.TypeDecorator):
    __dada_type__ = "bool"
    impl = types.Boolean


class EnumCol(types.TypeDecorator):
    __dada_type__ = "enum"
    impl = ENUM


# GEO COLUMNS


class WKTCol(types.TypeDecorator):
    __dada_type__ = "wkt"
    impl = types.Unicode


class WKBCol(types.TypeDecorator):
    __dada_type__ = "wkb"
    impl = types.Unicode  # TODO


# SEARCH COLUMNS


class SearchVectorCol(types.TypeDecorator):
    __dada_type__ = "vector"
    impl = TSVectorType


# json columns


class JSONCol(types.TypeDecorator):
    __dada_type__ = "json"
    impl = JSONB


# Special Cases

RE_HANDLE_RAW_STRING = re.compile(r"^{(.*)}$")


class EnumArrayCol(types.TypeDecorator):
    """
    Class for creating an array of enums in SQL Alchemy
    # TODO: move this somewhere else?
    """

    __dada_type__ = "enum_array"

    impl = ARRAY

    def bind_expression(self, bindvalue):
        """"""
        return cast(bindvalue, self)

    def result_processor(self, dialect, coltype):
        """"""
        super_rp = super(EnumArrayCol, self).result_processor(dialect, coltype)

        def handle_raw_string(value):
            """"""
            inner = RE_HANDLE_RAW_STRING.match(value).group(1)
            return inner.split(",") if inner else []

        def process(value):
            """"""
            if value is None:
                return None
            return super_rp(handle_raw_string(value))

        return process
