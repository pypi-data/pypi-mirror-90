import argparse
from typing import Optional, Any, List
from marshmallow import ValidationError
from dada_types.lib import (
    # core objects
    DadaType,
    DadaTypes,
    # helper functions
    NewVal,
    NewType as NewPy,
)
from dada_types.base import SerializableObject
import dada_text

# shorthand access to our type library
T = DadaTypes()

# COLLECTION OF TYPES (PARAMETERS)


class Parameter(SerializableObject):
    """
    A class for a defining and validating input parameters for python code/cli/api/sql, etc.
    :param name: The parameter type
    """

    __abstract__ = True
    __dada_type__ = "param_def"
    name = None
    abbr = None
    type = None
    value = None
    title = None

    def __init__(
        self,
        name: T.param_name.py,
        abbr: T.name.py_optional = None,
        type: T.dada_type.py = "text",
        default: Optional[Any] = None,
        required: T.bool.py = False,
        info: T.text.py = None,
        options: T.text_array.py_optional = None,
        env_var: T.text.py_optional = None,
        sensitive: T.bool.py = False,
        example: T.text.py_optional = None,
    ):
        self.name = name or self.name
        self.abbr = abbr or self.abbr
        self.type = type or self.type or self.__dada_type__ or None  # for inheritance
        self.default = default or None
        self.required = required or False
        self.info = info or self.dada_type.info or self.object_info
        self.options = options or self.dada_type.opts
        self.env_var = env_var or None
        self.sensitive = sensitive or False
        self.example = example or None

        # set internal type var
        self.__dada_type__ = type

        # once a param in instantiated its no longer an abstraction
        self.__abstract__ = False

    def __repr__(self) -> str:
        return f"<Param={self.name}:{self.type}>"

    @property
    def cli_name(self) -> str:
        """
        Full cli name
        """
        return f"--{dada_text.get_slug(self.name)}"

    @property
    def cli_abbr(self) -> str:
        """
        Full cli name
        """
        if self.abbr is None:
            self.abbr = dada_text.get_abbr(self.name)
        return f"-{self.abbr}"

    @property
    def title(self) -> str:
        """
        Parameter title
        """
        return dada_text.get_title(self.name)

    @property
    def dada_type(self) -> str:
        """
        core type
        """
        return T.get(self.type)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
            "title": self.title,
            "info": self.info,
            "cli_abbr": self.cli_abbr,
            "cli_name": self.cli_name,
            "required": self.required,
            "default": self.default,
            "env_var": self.env_var,
            "options": self.options,
            "is_array": self.is_array,
            "is_json": self.is_json,
        }

    def validate(self, raw: Optional[Any]) -> Optional[Any]:
        """
        Turn a parameter into its python object
        """
        # validate pre serialization
        raw = self._run_validations(raw)
        try:
            value = self.dada_type.validate(raw)
        except ValidationError as e:
            raise RequestError(
                f"ERROR: {e}\nCONTEXT: {self.name} is of type {self.type} and you passed in '{raw}'"
            )

        # validate post-serialization
        value = self._run_validations(value)
        # set value
        return value

    # /////////////////////////
    # Boolean Checks
    # /////////////////////////

    @property
    def is_array(self) -> bool:
        """
        Whether or not this param is an `array`
        """
        return self.dada_type.is_array

    @property
    def is_json(self) -> bool:
        """
        Whether or not this param is a `json`
        """
        return self.dada_type.is_json

    @property
    def is_text(self) -> bool:
        """
        Whether or not this param is a `text`
        """
        return self.dada_type.is_text

    @property
    def is_int(self) -> bool:
        """
        Whether or not this param is a `int`
        """
        return self.dada_type.is_int

    @property
    def is_num(self) -> bool:
        """
        Whether or not this param is a `num`
        """
        return self.dada_type.is_num

    @property
    def is_date(self) -> bool:
        """
        Whether or not this param is a `date`
        """
        return self.dada_type.is_date

    @property
    def is_time(self) -> bool:
        """
        Whether or not this param is a `time`
        """
        return self.dada_type.is_time

    @property
    def has_default(self) -> bool:
        """
        Whether or not this param is a `num`
        """
        return self.default is not None

    @property
    def has_options(self) -> bool:
        """
        Whether or not this param is a `num`
        """
        return self.options is not None and len(self.options) > 0

    @property
    def has_env_var(self) -> bool:
        """
        Whether or not this param is a `num`
        """
        return self.env_var is not None and self.env_var in os.environ

    @property
    def option_values(self) -> List[any]:
        """
        Parsed options
        """
        if self.has_options:
            return [self.dada_type.load(opt) for opt in self.options]
        return []

    def add_to_argparser(
        self, parser: argparse.ArgumentParser
    ) -> argparse.ArgumentParser:
        """
        Add a param as an argparser argument to an an ArgumentParser
        :param parser: An ArgumentParser
        :return argparse.ArgumentParser
        """
        kwargs = dict(
            help=self.info,
            dest=self.name,
            default=self.default,
            required=self.required,
            type=self.validate,
        )
        if self.has_options:
            kwargs["choices"] = self.option_values

        # allow multiple flags for array
        if not self.is_array:
            kwargs["nargs"] = "+"

        parser.add_argument(self.cli_name, **kwargs)
        return parser

    # /////////////////////////
    # Internal Validations
    # /////////////////////////

    def _run_validations(self, value: Optional[Any]) -> Optional[Any]:
        """
        Run validation checks on a param value
        """
        if value is None or value == "":
            value = self._validate_missing(value)

        # force lists
        if self.is_array:
            value = self._validate_array(value)

        # check options
        if self.has_options:
            self._validate_options(value)
        return value

    def _validate_missing(self, raw: Optional[Any]) -> Optional[Any]:
        """
        Validate values when they are missing
        """
        value = None
        if self.required:
            raise ValueError(f"Parameter: {self.name} is required!")

        elif not self.has_default and not self.has_env_var:
            raise ValueError(
                f"Parameter: {self.name} is missing and no default or env_var is provided"
            )
        else:
            # check for defaults / env vars
            if self.has_default:
                value = self.default
            if self.has_env_var:
                value = os.getenv(self.env_var, raw)
            else:
                # default env var format
                value = os.getenv(f"DADA_LAKE_PARAM_{self.name.upper()}_VALUE", raw)

        # final check
        if not value and self.required:
            raise ValueError(f"Parameter: {self.name} is required!")
        return value

    def _validate_array(self, value: Any) -> List[Any]:
        """
        Force array types
        """
        if not isinstance(value, list):
            value = text.to_list(value)
        return value

    def _validate_options(self, value: Any) -> None:
        """
        Check if this value is value
        """
        if self.is_array:
            for val in value:
                self._validate_option(val)
        else:
            self._validate_option(value)

    def _validate_option(self, value: Optional[Any]) -> None:
        """
        Validate a single value against it's list of options
        """
        if self.is_text:
            v = str(value)
        if v not in self.options:
            raise ValidationError(
                f"{value} is not an allowed option for {self.name}. choose from: {', '.join(self.options)}"
            )


class Parameters(SerializableObject):
    """
    A collection of parameters
    TOOD: Figure out how to map this to a marshmallow schema?
    """

    __abstract__ = True

    def __init__(self, params):
        self.params = {name: Parameter(name, **param) for name, param in params.items()}
        self.__abstract__ = False

    def __repr__(self):
        """"""
        return f"<Parameters={', '.join(self.schema_strings)}>"

    @property
    def names(self):
        """"""
        return list(self.params.keys())

    def to_dict(self):
        """"""
        return {
            "name": self.object_name,
            "title": self.object_title,
            "info": self.object_info,
            "param_def": {name: self.params.get(name).to_dict() for name in self.names},
        }

    def dump(self, **params) -> dict:
        """
        strings to task parameter values
        """
        data = {
            name: self.params.get(name).dump(value) for name, value in params.items()
        }
        for name, param in self.params.items():
            if name not in data and param.has_default:
                data[name] = param.default
        return data

    def validate(self, **params) -> dict:
        """
        deserialized task paramter values
        """
        data = {
            name: self.params.get(name).validate(value)
            for name, value in params.items()
        }
        for name, param in self.params.items():
            if name not in data:
                if param.required:
                    raise ValueError(f"Parameter {name} is required")
                elif param.has_default:
                    data[name] = param.default
        return data

    def add_to_argparser(self, parser):
        """
        Add these parameters as cli arguments
        """
        for param in self.params.values():
            parser = param.add_to_argparser(parser, param)
        return parser
