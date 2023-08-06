"""
Custom Filter / Search Strings for SQL and Python contexts
"""
import re
from typing import Any, List, Dict, Optional, Callable

from sqlalchemy import func, and_, or_, asc, desc, Column, types, cast

from dada_types.base import SerializableObject
from dada_types import T
import dada_text

RE_TYPE = type(re.compile(""))

FIELD_PARAM = ":param field: The field to compare against"
VALUE_PARAM = ":param value: The value to use for the comparison"
CONTEXT_PARAM = ":param context: The context to (either ``sql`` or ``py``"

# ////////////////////////////////////
# Simple Comparisons
#   - these work in both python and sql
# //////////////////////////////////////


def _gte(field: Any, value: Any, **kwargs):
    f"""
    Greater Than or Equal to
    {FIELD_PARAM}
    {VALUE_PARAM}
    :return bool
    """
    return field >= value


def _gt(field: Any, value: Any, **kwargs):
    f"""
    Greater Than
    {FIELD_PARAM}
    {VALUE_PARAM}
    :return bool
    """
    return field > value


def _lte(field: Any, value: Any, **kwargs):
    f"""
    Less Than or Equal to
    {FIELD_PARAM}
    {VALUE_PARAM}
    :return bool
    """
    return field <= value


def _lt(field: Any, value: Any, **kwargs):
    f"""
    Less Than
    {FIELD_PARAM}
    {VALUE_PARAM}
    :return bool
    """
    return field < value


def _eq(field: Any, value: Any, **kwargs):
    f"""
    Equal to
    {FIELD_PARAM}
    {VALUE_PARAM}
    :return bool
    """
    return field == value


def _neq(field: Any, value: Any, **kwargs):
    f"""
    Equal to
    {FIELD_PARAM}
    {VALUE_PARAM}
    :return bool
    """
    return field != value


# ////////////////////////////////////
# Complex Comparisons
#   - these work differently in python and sql
# //////////////////////////////////////


def _sql_array_to_string(arr):
    """
    Helper for casting sql arrays to strings.
    """
    return cast(func.array_to_string(arr, ",", ""), types.Unicode)


def _re(field: Any, value: Any, context: str = "py", is_array: bool = False, **kwargs):
    f"""
    Regular expression match
    {FIELD_PARAM}
    {VALUE_PARAM}
    {CONTEXT_PARAM}
    :return bool
    """
    if context == "sql":
        if is_array:
            field = _sql_array_to_string(field, ",", "")
            if isinstance(value, list):
                value = value[0]
        return field.op("~")(value)
    if not isinstance(value, RE_TYPE):
        value = re.compile(value)

    if is_array:
        for f in field:
            if value.search(f):
                return True
        return False

    if value.search(field):
        return True
    return False


def _lk(field: Any, value: Any, context: str = "py", is_array: bool = False, **kwargs):
    f"""
    Like match
    {FIELD_PARAM}
    {VALUE_PARAM}
    {CONTEXT_PARAM}
    :return bool
    """
    if context == "sql":
        if is_array:
            field = _sql_array_to_string(field)
            if isinstance(value, list):
                value = value[0]
        return func.lower(field).ilike(value)

    # convert this into a regex
    value = re.compile(value.replace("%", ".+"))

    if is_array:
        for f in field:
            if value.search(f):
                return True
        return False

    if value.search(field):
        return True
    return False


def _sw(field: Any, value: Any, context: str = "py", is_array: bool = False, **kwargs):
    f"""
    Startswith match
    {FIELD_PARAM}
    {VALUE_PARAM}
    {CONTEXT_PARAM}
    :return bool
    """
    if context == "sql":
        if is_array:
            field = _sql_array_to_string(field)
            if isinstance(value, list):
                value = value[0]
        return field.ilike(value + "%")

    if is_array:
        for f in field:
            if f.startswith(value):
                return True
        return False

    return field.startswith(value)


def _ew(field: Any, value: Any, context: str = "py", is_array: bool = False, **kwargs):
    f"""
    Endswith match
    {FIELD_PARAM}
    {VALUE_PARAM}
    {CONTEXT_PARAM}
    :return bool
    """
    if context == "sql":
        if is_array:
            field = _sql_array_to_string(field)
            if isinstance(value, list):
                value = value[0]
        return field.like(f"%{value}")

    if is_array:
        for f in field:
            if f.endswith(value):
                return True
        return False

    return field.endswith(value)


def _in(field: Any, value: Any, context: str = "py", is_array: bool = False, **kwargs):
    f"""
    Not in List
    {FIELD_PARAM}
    {VALUE_PARAM}
    {CONTEXT_PARAM}
    :return bool
    """
    if context == "sql":
        return field.in_(value)
    return field in value


def _bt(
    field: Any, value: List[Any], context: str = "py", is_array: bool = False, **kwargs
):
    """
    value BETWEEN low AND high;
    If the value is greater than or equal to the low value and less than or equal to the high value, the expression returns true, otherwise, it returns false.
    You can rewrite the BETWEEN operator by using the greater than or equal ( >=) or less than or equal ( <=) operators as the following statement:
    value >= low and value <= high
    """
    if context == "sql":
        if is_array:
            raise NotImplementedError("The `bt` operator does not work for SQL arrays.")
        return and_(field >= value[0], field <= value[1])

    if is_array:
        for f in field:
            if f >= value[0] and f <= value[1]:
                return True
        return False

    return field >= value[0] and field <= value[1]


def _nin(field: Any, value: Any, context: str = "py", is_array: bool = False, **kwargs):
    f"""
    Field not in list of values.
    {FIELD_PARAM}
    {VALUE_PARAM}
    {CONTEXT_PARAM}
    :return bool
    """
    if context == "sql":
        return ~field.in_(value)
    if not isinstance(value, list):
        value = [value]
    return field not in value


def _ws(field: Any, value: Any, context: str = "sql", is_array: bool = False, **kwargs):
    f"""
    Websearch match (Sql only)
    {FIELD_PARAM}
    {VALUE_PARAM}
    {CONTEXT_PARAM}
    :return bool
    """
    if context == "sql":
        if is_array:
            raise NotImplementedError("Websearch not implimented for array input")
        return func.lower(field).op("@@")(func.websearch_to_tsquery(value))
    raise NotImplementedError("Websearch not implemneted in python context")


def _fz(
    field: Any,
    value: Any,
    fuzz: float = 0.89,
    split: bool = False,
    context: str = "sql",
    is_array: bool = False,
    **kwargs,
):
    __dada_type__ = "filter_fz"
    f"""
    Fuzzy string match (python only, via jaro winkler distance
    {FIELD_PARAM}
    {VALUE_PARAM}
    {CONTEXT_PARAM}
    :param fuzz: The fuzz factor to match by (min=0, max=1)
    :param split: Whether or not to split the input values.
    :return bool
    """
    if context != "py":
        raise NotImplementedError(
            "Only python context is available for fuzzy matching currently"
        )
    if split:
        if not is_array:
            for gram in dada_text.to_tokens(field):
                if dada_text.get_jaro_distance(value, gram) >= fuzz:
                    return True
            return False
        else:
            for f in field:
                for f in dada_text.to_tokens(f):
                    if dada_text.get_jaro_distance(value, gram) >= fuzz:
                        return True
    return dada_text.get_jaro_distance(value, field) >= fuzz


# ///////////////////////////
# Library of Filter Functions
# ////////////////////////////

FILTERS = {
    "gte": {"func": _gte, "docs": _gte.__doc__},
    ">=": {"func": _gte, "docs": _gte.__doc__},
    "gt": {"func": _gt, "docs": _gt.__doc__},
    ">": {"func": _gt, "docs": _gt.__doc__},
    "lte": {"func": _lte, "docs": _lte.__doc__},
    "<=": {"func": _lte, "docs": _lte.__doc__},
    "lt": {"func": _lt, "docs": _lt.__doc__},
    "<": {"func": _lt, "docs": _lt.__doc__},
    "eq": {"func": _eq, "docs": _eq.__doc__},
    "==": {"func": _eq, "docs": _eq.__doc__},
    "neq": {"func": _neq, "docs": _neq.__doc__},
    "!=": {"func": _neq, "docs": _neq.__doc__},
    "re": {"func": _re, "docs": _re.__doc__},
    "~": {"func": _re, "docs": _re.__doc__},
    "lk": {"func": _lk, "docs": _lk.__doc__},
    "%": {"func": _lk, "docs": _lk.__doc__},
    "sw": {"func": _sw, "docs": _sw.__doc__},
    "->": {"func": _sw, "docs": _sw.__doc__},
    "ew": {"func": _ew, "docs": _ew.__doc__},
    "<-": {"func": _ew, "docs": _ew.__doc__},
    "in": {"func": _in, "list_input": True, "docs": _in.__doc__},
    "[]": {"func": _in, "list_input": True, "docs": _in.__doc__},
    "nin": {"func": _nin, "list_input": True, "docs": _nin.__doc__},
    "![]": {"func": _nin, "list_input": True, "docs": _nin.__doc__},
    "bt": {"func": _bt, "list_input": True, "docs": _bt.__doc__},
    "<>": {"func": _bt, "list_input": True, "docs": _bt.__doc__},
    "ws": {"func": _ws, "contexts": ["sql"], "docs": _ws.__doc__},
    "@": {"func": _ws, "contexts": ["sql"], "docs": _ws.__doc__},
    "fz": {"func": _fz, "contexts": ["py"], "docs": _fz.__doc__},
    "@@": {"func": _fz, "contexts": ["py"], "docs": _fz.__doc__},
}

FILTER_NAMES = list(FILTERS.keys())
FILTER_NAME_LIST = ", ".join(FILTER_NAMES)
FILTER_MATCH_CONTEXTS = ["py", "sql"]


def match(
    field: Any,
    op: str,
    value: Any,
    type: Callable = lambda x: x,
    context: str = "py",
    **kwargs,
):
    f"""
    Apply a match via different strategies / contexts
    {FIELD_PARAM}
    :param op: The operation to run. Choose from: {FILTER_NAME_LIST}
    {VALUE_PARAM}
    {CONTEXT_PARAM}
    :param type: A function to load this values type (preferably via ``dada_types.T``).
    :param kwargs: Additional keyword arguments to pass to individual matching functions
    return bool
    """
    operation = FILTERS.get(op, None)
    if not operation:
        return ValueError(
            f"Operation ``{op}`` is not supported. try from: {FILTER_NAME_LIST}"
        )

    # othter validations
    enabled_contexts = operation.get("contexts", FILTER_MATCH_CONTEXTS)
    if context not in enabled_contexts:
        return ValueError(
            f"Operation ``{op}`` is not available in context: ``{context}``"
        )

    # process lists
    has_list_input = operation.get("list_input", False)
    if has_list_input:
        if isinstance(value, list):
            value = [type(v) for v in value]
        elif isinstance(value, str):
            value = [type(v) for v in dada_text.to_list(value) if v.strip()]
        else:
            raise ValueError(f"Invalid list format for operation ``{op}``: {value}")

    else:
        value = type(value)

    # run the comparison
    return operation["func"](field, value, context, **kwargs)


# ///////////////////////////
# Core Filter String object
# ////////////////////////////


class FilterString(SerializableObject):
    """
    A filter string applies filters across sql / python
    eg:
    ```
    id3_artist_name:lk:Brian%
    id3_bpm:>=:120.0
    TODO
        val operators eg: date, month, week, now etc.
    ```
    """

    __dada_type__ = "filter"
    __dictionary__ = FILTERS
    __filter_names__ = FILTER_NAMES
    __filter_set__ = frozenset(FILTER_NAMES)

    def __init__(
        self,
        string: str,
        type: T.dada_type.py = "text",
        context: str = "py",
        **defaults: dict,
    ):
        """
        Load an validate a function string
        Optionally setting default kwargs
        :param string: A raw filter string
        :param type: A dada type name for processing input against
        :param defaults: Defaults to pass to ``match``
        """
        self.value_type = type
        self.context = context
        self.defaults = defaults
        self.raw_string = string
        self._lint(string)

    @property
    def __repr__(self):
        return self.raw_string

    @property
    def __str__(self):
        return self.raw_string

    @classmethod
    def load(
        cls,
        string: str,
        type: T.dada_type.py = "text",
        context: str = "py",
        **defaults: dict,
    ):
        """
        Load an instance of a filter string
        """
        return cls(string, value_string, context, **defaults)

    def dump(self):
        """
        dump a filter string
        """
        return self.raw_string

    def set_type(self, type: T.dada_type.py):
        """
        Set the type of this filter string.
        """
        self.value_type = type

    @property
    def __dada_type__(self) -> T.dada_type.py:
        """"""
        return self.value_type

    @property
    def dada_type(self):
        """
        Access to our type library.
        """
        return T.get(self.value_type)

    @property
    def value_is_json(self):
        """"""
        return self.dada_type.is_json

    @property
    def value_is_date(self):
        """"""
        return self.dada_type.is_date

    @property
    def value_is_num(self):
        """"""
        return self.dada_type.is_num

    @property
    def value_is_array(self):
        """"""
        return self.dada_type.is_array

    @property
    def func(self):
        """"""
        return self.op["func"]

    @property
    def has_list_input(self):
        """"""
        return self.op.get("list_input", False)

    @property
    def value(self):
        if self.has_list_input:
            return [
                self.dada_type.validate(v)
                for v in dada_text.to_list(self.filter_value)
                if v.strip()
            ]
        return self.dada_type.validate(self.filter_value)

    def _lint(self, string: str):
        """
        Parse a raw filter string
        TODO: docs here
        """
        parts = string.split(":")
        if not len(parts) >= 3:
            raise ValueError(
                f"Invalid Filter String: {string}. Must follow the format `<field>:<op>:<value>`"
            )
        self.field_name = dada_text.get_snake(parts[0])
        op_name = parts[1]
        if not op_name.strip() or op_name.lower() not in self.__filter_set__:
            raise ValueError(
                f'Invalid Filter String: {string}. Inferrred Operator: {op_name} is not supported. try from: {", ".join(self.__filter_names__)}'
            )

        # set operation
        self.op_name = op_name
        self.op = self.__dictionary__.get(self.op_name)
        # add ':' back to the value
        self.filter_value = ":".join(parts[2:])

    def match_self(self, **kwargs) -> bool:
        """
        Just interpret the string as naive filter eg:
        1>=2
        """
        return self.func(
            self.dada_type.validate(self.field_name),
            self.value,
            context="py",
            is_array=self.value_is_array,
            **kwargs,
        )

    def match(self, field_value: Any, **kwargs) -> bool:
        """
        Match against the provided value
        :param field_value: The value to match against
        """
        return self.func(
            self.dada_type.validate(field_value),
            self.value,
            context="py",
            is_array=self.value_is_array,
            **kwargs,
        )

    def match_sql(self, column: Column, **kwargs):
        """
        Get match in a sql context
        """
        return self.func(
            column, self.value, context="sql", is_array=self.value_is_array, **kwargs
        )

    def match_fields(self, fields: dict, comp="any", **kwargs) -> bool:
        """
        Match against a dictionary of fields:
            here we interpret the first part of the filter string
            to the the name of a key in a dictionary
        """
        field_value = fields.get(self.field_name, None)
        if not field_value:
            return False

        return self.func(
            self.dada_type.validate(field_value),
            self.value,
            context="py",
            is_array=self.value_is_array,
            **kwargs,
        )

    def to_dict(self) -> dict:
        """
        Render this filter string as a dictionary
        """
        return {
            "string": self.raw_string,
            "field_name": self.field_name,
            "op": self.op_name,
            "value": self.value,
            "value_is_array": self.value_is_array,
            "field_info": self.dada_type.info,
        }


class PyFilterStrings(SerializableObject):
    """
    A collection of filter strings with options to combine / apply them to dictionaries within a python condada_text.
    """

    __dada_type__ = "py_filter_array"

    def __init__(
        self, strings: List[Any], context: str = "py", combine: str = "any", **kwargs
    ):
        self.filters = []
        self.context = context
        self.combine = combine
        self.raw_strings = strings
        for s in strings:
            self.filters.append(FilterString(s, context))

    @property
    def __repr__(self):
        return "&".join(self.raw_strings)

    @property
    def __str__(self):
        return "&".join(self.raw_strings)

    @classmethod
    def load(
        cls, strings: List[Any], context: str = "py", combine: str = "any", **kwargs
    ):
        """
        Load a filter string set
        """
        filter_srings = cls(strings, context, combine, **kwargs)
        return filter_strings

    def dump(self):
        """"""
        return self.raw_strings

    def to_dict(self):
        """"""
        return {
            "name": self.object_name,
            "type": self.__dada_type__,
            "context": self.context,
            "combine": self.combine,
            "filters": [f.to_dict() for f in self.filters],
        }
